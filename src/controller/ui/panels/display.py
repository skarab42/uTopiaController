# coding: utf-8
from __future__ import unicode_literals

import wx

from controller.i18n import _
from controller.ui.mixins import FrameMixin
from controller.ui.base import DisplayPanel as BaseDisplayPanel

class DisplayPanel(BaseDisplayPanel, FrameMixin):
    _name = 'display_panel'
    _viewer = None
    _display = None
    _last_slice = None

    def __init__(self, parent, viewer):
        super(DisplayPanel, self).__init__(parent)
        self._viewer = viewer

    def Setup(self):
        self.Sub('viewer_frame.on_open', self.OnViewerOpened)
        self.Sub('viewer_frame.on_close', self.OnViewerClosed)
        self.Sub('printer.on_print_start', self.OnPrintStart)
        self.Sub('project_panel.on_slice', self.ShowSlice)
        self.Sub('main_frame.on_close', self.OnClose)
        self.RefreshDisplaysList()
        self.SetSelectedDisplay()

    def RefreshDisplaysList(self):
        self.displays.Clear()
        count = wx.Display.GetCount()
        for index in range(count):
            display = wx.Display(index)
            mode = display.GetCurrentMode()
            description = '%i x %i' % (mode.GetWidth(), mode.GetHeight())
            if display.IsPrimary():
                description += ' (%s)' % _('primary')
            self.displays.Append('[ %i ] %s' % (index + 1, description))
        self.displays.SetSelection(index)

    def OnRefreshClick(self, event):
        self.RefreshDisplaysList()

    def SetSelectedDisplay(self):
        display_id, geometry = self.GetSelectedDisplay()
        self._display = {
            'id': display_id,
            'num': display_id + 1,
            'left': geometry[0],
            'top': geometry[1],
            'width': geometry[2],
            'height': geometry[3]
            }

    def OnViewerOpened(self, size, position):
        self.Log(_('Viewer opened on display %i') % self._display['num'])
        self.open_close.SetToolTipString(_('Close viewer'))
        self.SetButtonBitmap(self.open_close, 'reduce')

    def OnViewerClosed(self):
        self.Log(_('Viewer closed on display %i') % self._display['num'])
        self.open_close.SetToolTipString(_('Open viewer'))
        self.SetButtonBitmap(self.open_close, 'expand')
        self.SetSelectedDisplay()

    def GetSelectedDisplay(self):
        display_id = self.displays.GetSelection()
        display = wx.Display(display_id)
        geometry = display.GetGeometry()
        return (display_id, geometry)

    def OnDisplayChange(self, event):
        if self._viewer.IsShown():
            return None
        self.SetSelectedDisplay()

    def ShowSlice(self, path=None):
        self._last_slice = path
        self._viewer.ShowSlice(path)

    def OpenViewer(self):
        size = (self._display['width'], self._display['height'])
        position = (self._display['left'], self._display['top'])
        self._viewer.Open(size, position)
        self.ShowSlice(self._last_slice)

    def CloseViewer(self):
        self._viewer.Close()
        self.SetFocus()

    def OnOpenCloseClick(self, event):
        if self._viewer.IsShown():
            self.CloseViewer()
        else:
            self.OpenViewer()

    def OnPrintStart(self):
        self.OpenViewer()
        self.ShowSlice()

    def OnClose(self):
        if self._viewer.IsShown():
            self.CloseViewer()
