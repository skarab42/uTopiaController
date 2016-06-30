# coding: utf-8
from __future__ import unicode_literals

from controller.core.printer import Printer as CorePrinter

# commands list:
# - relative_mode
# - motor_on
# - motor_off
# - light_on
# - light_off
# - lift_up
# - lift_down
# - wait

# pubsub topics from Printer:
# - printer.on_command_[command_name](command, args)
# - printer.on_response_[command_name](command, response, args)

# pubsub topics herited from CorePrinter:
# - printer.on_command(name, command, args)
# - printer.on_response(name, command, response, args)
# - printer.on_connect(port, baudrate)
# - printer.on_connected(port, baudrate)
# - printer.on_disconnect(port)
# - printer.on_disconnected(port)
# - printer.on_error(message)
# - printer.on_print_start()
# - printer.on_print_end()

class Printer(CorePrinter):
    _name = 'printer'
    _motor_on = False
    _light_on = False

    def Pause(self, after='lift_up'):
        super(Printer, self).Pause(after)

    def Abort(self, after='lift_up'):
        super(Printer, self).Abort(after)

    def MotorOn(self):
        return self._motor_on

    def MotorOff(self):
        return not self.MotorOn()

    def LightOn(self):
        return self._light_on

    def LightOff(self):
        return not self.LightOn()

    def SendRelativeMode(self):
        self.SendCommand('relative_mode', 'G91')

    def SendMotorOn(self):
        self.SendCommand('motor_on', 'M17 M400')

    def SendMotorOff(self):
        self.SendCommand('motor_off', 'M18 M400')

    def SendPrintStart(self):
        self.SendCommand('print_start', 'M400')

    def SendPrintEnd(self):
        self.SendCommand('print_end', 'M400')

    def SendLightOn(self):
        self.SendCommand('light_on', 'M106 M400')

    def SendLightOff(self):
        self.SendCommand('light_off', 'M107 M400')

    def SendShowSlice(self, num):
        self.SendCommand('show_slice', 'M400', num)

    def SendHideSlice(self, num):
        self.SendCommand('hide_slice', 'M400', num)

    def SendWait(self, milliseconds):
        self.SendCommand('wait', 'G4 P%i' % milliseconds)

    def SendLiftUp(self, offset, speed):
        self.SendCommand('lift_up', 'G1 Z%f F%i M400' % (offset, speed))

    def SendLiftDown(self, offset, speed):
        self.SendCommand('lift_down', 'G1 Z-%f F%i M400' % (offset, speed))

    def OnResponse(self, name, command, response, args):
        if name == 'motor_on':
            self._motor_on = True
        elif name == 'motor_off':
            self._motor_on = False
        elif name == 'light_on':
            self._light_on = True
        elif name == 'light_off':
            self._light_on = False
        elif name == 'print_start':
            self._printing.set()
            self.Pub('on_print_start')
        elif name == 'print_end':
            self._printing.clear()
            self.Pub('on_print_end')
        self.Pub('on_response_%s' % name, command=command, response=response, args=args)
        super(Printer, self).OnResponse(name, command, response, args)

    def OnCommand(self, name, command, args):
        self.Pub('on_command_%s' % name, command=command, args=args)
        super(Printer, self).OnCommand(name, command, args)
