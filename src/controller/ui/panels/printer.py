# coding: utf-8
from __future__ import unicode_literals

import wx

from controller.i18n import _
from controller.ui.mixins import FrameMixin
from controller.ui.base import PrinterPanel as BasePrinterPanel
from controller.core.printer import ListPrinters, PrinterException

class PrinterPanel(BasePrinterPanel, FrameMixin):
    _name = 'printer_panel'
    _printer = None
    _motor_on = False
    _light_on = False

    def __init__(self, parent, printer):
        super(PrinterPanel, self).__init__(parent)
        self._printer = printer

    def Setup(self):
        self.Sub('printer.on_disconnected', self.OnDisconnected)
        self.Sub('printer.on_connected', self.OnConnected)
        self.Sub('printer.on_response', self.OnResponse)
        self.Sub('printer.on_command', self.OnCommand)
        self.Sub('printer.on_print_start', self.OnPrintStart)
        self.Sub('printer.on_print_end', self.OnPrintEnd)
        self.Sub('printer.on_aborted', self.OnPrintEnd)
        self.Sub('main_frame.on_close', self.OnClose)
        self.SetButtonBitmap(self.motor_on_off, 'motor-off')
        self.SetButtonBitmap(self.light_on_off, 'light-off')
        self.SetButtonBitmap(self.lift_down, 'down')
        self.SetButtonBitmap(self.lift_up, 'up')
        self.EnableControls(False)
        self.RefreshPrintersList()

    def EnableControls(self, enable=True):
        self.motor_on_off.Enable(enable)
        self.light_on_off.Enable(enable)
        self.lift_down.Enable(enable)
        self.lift_up.Enable(enable)

    def RefreshPrintersList(self):
        self.printers.Clear()
        for name, description, harware in ListPrinters():
            self.printers.Append('%s - %s' % (name, description))
        self.printers.SetSelection(0)

    def OnRefreshClick(self, event):
        self.RefreshPrintersList()

    def GetSelectedPort(self):
        index = self.printers.GetSelection()
        label = self.printers.GetString(index)
        return label.split(' - ', 2).pop(0)

    def OnConnected(self, port, baudrate):
        self.EnableControls(True)
        self.SetButtonBitmap(self.printer_on_off, 'power-on')
        self.printer_on_off.SetToolTipString(_('Disconnect'))
        self.Log(_('Connected to %s at %i BPS'), (port, baudrate))

    def Connect(self):
        try:
            self._printer.Connect(self.GetSelectedPort())
        except PrinterException as e:
            self.Error(unicode(e))

    def OnDisconnected(self, port):
        self.EnableControls(False)
        self.SetButtonBitmap(self.printer_on_off, 'power-off')
        self.printer_on_off.SetToolTipString(_('Connect'))
        self.Log(_('Disconnected from %s'), port)

    def Disconnect(self):
        try:
            self._printer.Disconnect()
        except PrinterException as e:
            self.Error(unicode(e))

    def OnPrinterOnOffClick(self, event):
        if not self._printer.Connected():
            return self.Connect()
        port = self._printer.Port()
        response = self.Question(_('Disconnect from %s ?'), port)
        if response == wx.ID_YES:
            self.Disconnect()

    def OnMotorOnOffClick(self, event):
        if self._motor_on:
            bitmap = 'motor-off'
            self._motor_on = False
            label = _('Turn motor ON')
            self._printer.SendMotorOff()
        else:
            bitmap = 'motor-on'
            self._motor_on = True
            label = _('Turn motor OFF')
            self._printer.SendMotorOn()
        self.motor_on_off.SetLabel(label)
        self.motor_on_off.SetToolTipString(label)
        self.SetButtonBitmap(self.motor_on_off, bitmap)

    def OnLightOnOffClick(self, event):
        if self._light_on:
            bitmap = 'light-off'
            self._light_on = False
            label = _('Turn light ON')
            self._printer.SendLightOff()
        else:
            bitmap = 'light-on'
            self._light_on = True
            label = _('Turn light OFF')
            self._printer.SendLightOn()
        self.light_on_off.SetLabel(label)
        self.light_on_off.SetToolTipString(label)
        self.SetButtonBitmap(self.light_on_off, bitmap)

    def OnLiftDownClick(self, event):
        self._printer.SendLiftDown(10, 500)

    def OnLiftUpClick(self, event):
        self._printer.SendLiftUp(10, 500)

    def OnPrintStart(self):
        self.EnableControls(False)
        self.printer_on_off.Enable(False)

    def OnPrintEnd(self):
        self.EnableControls(True)
        self.printer_on_off.Enable(True)

    def OnCommand(self, name, command, args):
        if args:
            name += '(%s)' % args
        self.Log(_('---> %s: %s'), (name, command))

    def OnResponse(self, name, command, response, args):
        if args:
            name += '(%s)' % args
        self.Log(_('<--- %s: %s'), (name, response))

    def OnClose(self):
        if self._printer.Connected():
            self.Disconnect()
