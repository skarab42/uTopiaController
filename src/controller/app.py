# coding: utf-8
from __future__ import unicode_literals

import wx

from ui.frames.main import MainFrame

class App(wx.App):
    _main_frame = None

    def __init__(self):
        super(App, self).__init__(False)

    def OnInit(self):
        self._main_frame = MainFrame()
        return True
