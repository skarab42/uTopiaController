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

    def SendPrintStart(self):
        self.SendCommand('print_start', 'print_start')

    def SendPrintEnd(self):
        self.SendCommand('print_end', 'print_end')

    def SendSetLiftingSpeed(self, speed):
        self.SendCommand('set_lifting_speed', 'lift 0 %i' % speed)

    def SendMotorOn(self):
        self.SendCommand('motor_on', 'motor on')

    def SendMotorOff(self):
        self.SendCommand('motor_off', 'motor off')

    def SendLightOn(self, layer=None):
        self.SendCommand('light_on', 'light on', layer)

    def SendLightOff(self, layer=None):
        self.SendCommand('light_off', 'light off', layer)

    def SendWait(self, milliseconds):
        self.SendCommand('wait', 'wait %i' % milliseconds)

    def SendLiftUp(self, offset, speed=None):
        if speed is None:
            self.SendCommand('lift_up', 'lift %.2f' % offset)
        else:
            self.SendCommand('lift_up', 'lift %.2f %i' % (offset, speed))

    def SendLiftDown(self, offset, speed=None):
        if speed is None:
            self.SendCommand('lift_down', 'lift -%.2f' % offset)
        else:
            self.SendCommand('lift_down', 'lift -%.2f %i' % (offset, speed))

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
