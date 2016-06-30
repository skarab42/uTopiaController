# coding: utf-8
from __future__ import unicode_literals

import wx

from controller.i18n import _
from controller.ui.mixins import FrameMixin
from controller.ui.base import MainFrame as BaseMainFrame
from controller.ui.frames.viewer import ViewerFrame
from controller.printer import Printer
from controller.project import Project
from controller.settings import Settings

# pubsub topics:
# - main_frame.before_init
# - main_frame.after_init
# - main_frame.before_setup
# - main_frame.after_setup[panels]
# - main_frame.before_add_panel[name]
# - main_frame.after_add_panel[name, panel, args]
# - main_frame.before_setup_panel[name, panel]
# - main_frame.after_setup_panel[name, panel, result]
# - main_frame.on_close

class MainFrame(BaseMainFrame, FrameMixin):
    _name = 'main_frame'
    _viewer_frame = None
    _printer = None
    _project = None
    _settings = None
    _job = None
    _panels = []

    def __init__(self):
        self.Pub('before_init')
        super(MainFrame, self).__init__(None)
        self.Sub('printer.on_disconnected', self.OnPrinterDisconnected)
        self.Sub('printer.on_connected', self.OnPrinterConnected)
        self.sb.SetStatusText(_('Offline'), 0)
        self._viewer_frame = ViewerFrame(self)
        self._printer = Printer()
        self._project = Project()
        self._settings = Settings()
        self.Setup()
        self.Fit()
        self.Show()
        self.Pub('after_init')

    def Setup(self):
        self.Pub('before_setup')
        self.AddPanel('Printer', self._printer)
        self.AddSpacer()
        self.AddPanel('Display', self._viewer_frame)
        self.AddSpacer()
        self.AddPanel('Project', self._project)
        self.AddSpacer()
        self.AddPanel('Settings', self._settings)
        self.AddSpacer()
        self.AddPanel('Print', self._printer)
        self.Pub('after_setup', panels=self._panels)
        self.SetupPanels()

    def OnPrinterDisconnected(self, port):
        self.sb.SetStatusText(_('Offline'), 0)

    def OnPrinterConnected(self, port, baudrate):
        self.sb.SetStatusText(_('Online (%s)') % port, 0)

    def SetupPanels(self):
        for i, item in enumerate(self._panels):
            name = item[0]
            panel = item[1]
            is_setup = item[2]
            if is_setup is True:
                continue
            self._panels[i][2] = True
            setup = getattr(panel, 'Setup', None)
            if setup is None:
                continue
            self.Pub('before_setup_panel', name=name, panel=panel)
            result = setup()
            self.Pub('after_setup_panel', name=name, panel=panel, result=result)

    def AddPanel(self, name, *args):
        lname = name.lower()
        class_name = '%sPanel' % name
        module_name = 'controller.ui.panels.%s' % lname
        module = __import__(module_name, fromlist=[class_name])
        panel_class = getattr(module, class_name)
        panel_name = '%s_panel' % lname
        args = (self.main_panel,) + args
        self.Pub('before_add_panel', name=lname)
        panel = apply(panel_class, args)
        setattr(self, panel_name, panel)
        self.panels_sizer.Add(panel, 0, wx.EXPAND)
        self._panels.append([lname, panel, False])
        self.Pub('after_add_panel', name=lname, panel=panel, args=args)

    def AddSpacer(self):
        line = wx.StaticLine(self.main_panel, wx.ID_ANY, style=wx.LI_HORIZONTAL)
        self.panels_sizer.Add(line, 0, wx.EXPAND)

    def OnClose(self, event):
        if self.Question(_('Close controller ?')) == wx.ID_YES:
            self.Pub('on_close')
            self.Destroy()
