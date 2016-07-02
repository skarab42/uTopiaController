# coding: utf-8
from __future__ import unicode_literals

from Queue import Queue
from threading import Event as Flag

from wx import CallAfter
from serial.tools import list_ports as list_ports
from serial import Serial, SerialException, PARITY_ODD, PARITY_NONE

from controller.i18n import _
from controller.pubsub import pubsub
from controller.core.daemon import Daemon

comports_prefixs = ['com',
                 '/dev/ttyusb',
                 '/dev/ttyacm',
                 '/dev/tty.',
                 '/dev/cu.',
                 '/dev/rfcomm']

def ListPrinters():
    comports = []
    for name, description, harware in list_ports.comports():
        for prefix in comports_prefixs:
            if name.lower().startswith(prefix):
                comports.append((name, description, harware))
    return comports

class PrinterException(Exception):
    def __init__(self, message, args=None):
        if args is not None:
            message %= args
        super(PrinterException, self).__init__(message)

class PrinterReader(Daemon):
    _printer = None

    def __init__(self, printer):
        super(PrinterReader, self).__init__()
        self._printer = printer

    def loop(self):
        line = self._printer.ReadLine()
        if line:
            CallAfter(self._printer.OnReadLine, line.strip())
            CallAfter(self._printer._waiting_response.clear)

class PrinterWriter(Daemon):
    _printer = None

    def __init__(self, printer):
        super(PrinterWriter, self).__init__()
        self._printer = printer

    def loop(self):
        if self._printer._pause.isSet():
            return None
        if self._printer._waiting_response.isSet():
            return None
        if not self._printer._commands_queue.empty():
            self._printer._waiting_response.set()
            name, command, args = self._printer._commands_queue.get()
            CallAfter(self._printer.OnCommand, name, command, args)
            CallAfter(self._printer.Write, command)

# pubsub topics:
# - printer.on_command(name, command, args)
# - printer.on_response(name, command, response, args)
# - printer.on_connect(port, baudrate)
# - printer.on_connected(port, baudrate)
# - printer.on_disconnect(port)
# - printer.on_disconnected(port)
# - printer.on_error(message)
# - printer.on_aborted()
# - printer.on_resumed()
# - printer.on_paused()

class Printer(object):
    _name = 'core_printer'
    _serial = None
    _port = None
    _baudrate = None
    _connected = False
    _timeout = 0.25
    _last_command = None
    _writer_daemon = None
    _reader_daemon = None
    _commands_queue = None
    _waiting_response = False
    _pause_after = None
    _abort_after = None
    _printing = False
    _pause = None

    def __init__(self):
        super(Printer, self).__init__()
        self._commands_queue = Queue()
        self._waiting_response = Flag()
        self._printing = Flag()
        self._pause = Flag()

    def Pub(self, topic, **kwargs):
        pubsub.publish('%s.%s' % (self._name, topic), **kwargs)

    def Sub(self, topic, callback):
        pubsub.subscribe(topic, callback)

    def Error(self, message, args=None):
        if args is not None:
            message %= args
        self.Pub('on_error', message=message)
        raise PrinterException(message)

    def Port(self):
        return self._port

    def Baudrate(self):
        return self._baudrate

    def Connected(self):
        return self._connected

    def Disconnected(self):
        return not self.Connected()

    def Paused(self):
        return self._pause.isSet()

    def Resume(self):
        self._pause.clear()
        self.Pub('on_resumed')

    def Pause(self, after=None):
        self._pause_after = after
        if not self._pause_after:
            self._pause.set()
            self.Pub('on_paused')

    def Printing(self):
        return self._printing.isSet()

    def ClearQueue(self):
        self._commands_queue = Queue()
        self._waiting_response.clear()

    def ClearPrinter(self):
        self.ClearQueue()
        self._pause.clear()
        self._printing.clear()

    def Abort(self, after=None):
        self._abort_after = after
        if not self._abort_after:
            self.ClearPrinter()
            self.Pub('on_aborted')

    def Connect(self, port, baudrate=115200):
        if self.Connected():
            self.Error(_('Printer already connected to %s.'), self._port)
        try:
            self.ClearPrinter()
            self.Pub('on_connect', port=port, baudrate=baudrate)
            # https://github.com/kliment/Printrun/blob/8c046755063025b6b582d9579bdbdc1edfbda520/printrun/printcore.py#L196
            self._serial = Serial(port=port,
                                  baudrate=baudrate,
                                  timeout=self._timeout,
                                  parity=PARITY_ODD)
            self._serial.close()
            self._serial.parity = PARITY_NONE
            self._serial.open()
            self._baudrate = self._serial.baudrate
            self._port = self._serial.port
            self._connected = True
            self._reader_daemon = PrinterReader(self)
            self._reader_daemon.start()
            self._writer_daemon = PrinterWriter(self)
            self._writer_daemon.start()
        except SerialException as e:
            self.Error(unicode(e))
        self.Pub('on_connected', port=self._port, baudrate=self._baudrate)

    def Disconnect(self):
        if self.Disconnected():
            self.Error(_('Printer already disconnected.'))
        self.ClearPrinter()
        self.Pub('on_disconnect', port=self._port)
        self._writer_daemon.stop()
        self._reader_daemon.stop()
        self._serial.close()
        self._connected = False
        self.Pub('on_disconnected', port=self._port)

    def Write(self, text, nl=True):
        if self.Disconnected():
            self.Error(_('Printer not connected.'))
        if nl:
            text += '\n'
        self._serial.write(text.encode())

    def ReadLine(self):
        return self._serial.readline()

    def OnCommand(self, name, command, args):
        self._last_command = (name, command, args)
        self.Pub('on_command', name=name, command=command, args=args)

    def OnResponse(self, name, command, response, args):
        self.Pub('on_response', name=name, command=command, response=response, args=args)

    def OnReadLine(self, response):
        if not self._last_command:
            return None
        name, command, args = self._last_command
        self.OnResponse(name, command, response, args)
        if self._pause_after == name:
            self.Pause(None)
        if self._abort_after == name:
            self.Abort(None)

    def SendCommand(self, name, command, args=None):
        self._commands_queue.put((name, command, args))
