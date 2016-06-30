# coding: utf-8
from __future__ import unicode_literals

import wx

from controller.i18n import _
from controller.pubsub import pubsub

class FrameMixin(object):
    _name = 'frame_mixin'

    def Setup(self):
        pass

    def Pub(self, topic, **kwargs):
        pubsub.publish('%s.%s' % (self._name, topic), **kwargs)

    def Sub(self, topic, callback):
        pubsub.subscribe(topic, callback)

    def Text(self, text, args=None):
        if args is not None:
            text %= args
        return text

    def Log(self, text, args=None): #TODO: real logging
        lines = self.Text(text, args).split('\n')
        print ' - %s' % lines.pop(0)
        for line in lines:
            print '   %s' % line

    def Dialog(self, title, text, args=None, style=wx.OK):
        text = self.Text(text, args)
        dialog = wx.MessageDialog(self, text, title, style)
        return dialog.ShowModal()

    def Alert(self, text, args=None):
        style = wx.OK | wx.ICON_EXCLAMATION
        return self.Dialog(_('Alert !'), text, args, style)

    def Question(self, text, args=None):
        style = wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
        return self.Dialog(_('Question ?'), text, args, style)

    def Error(self, text, args=None):
        text = _('Error : %s') % text
        self.Log(text, args)
        self.Alert(text, args)

    def SetButtonBitmap(self, button, name):
        # bitmap = wx.Bitmap('./assets/%s.png' % name)
        # button.SetBitmapLabel(bitmap)
        # button.SetBitmapFocus(bitmap)
        # button.SetBitmapHover(bitmap)
        pass
