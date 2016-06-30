# coding: utf-8
from __future__ import unicode_literals

import wx
from wx import WXK_ESCAPE, WXK_F11, Display

from controller.ui.mixins import FrameMixin
from controller.ui.base import ViewerFrame as BaseViewerFrame

# pubsub topics:
# - viewer_frame.on_open(size, position)
# - viewer_frame.on_close

class ViewerFrame(BaseViewerFrame, FrameMixin):
    _name = 'viewer_frame'
    _parent = None
    _size = None
    _position = None

    def __init__(self, parent):
        super(ViewerFrame, self).__init__(parent)
        self._parent = parent

    def ShowSlice(self, path=None):
        self.slice.Hide()
        if path is None or self._size is None:
            return None
        width, height = self._size
        image = wx.Image(path, type=wx.BITMAP_TYPE_PNG)
        left = (width - image.GetWidth()) / 2
        top = (height - image.GetHeight()) / 2
        self.slice.SetPosition((left, top))
        self.slice.SetBitmap(image.ConvertToBitmap())
        self.slice.Show()

    def Open(self, size=None, position=None):
        if size is not None:
            self.SetSize(size)
        if position is not None:
            self.SetPosition(position)
        self.Show()
        self._size = self.GetSize()
        self._position = self.GetPosition()
        self.Pub('on_open', size=self._size, position=self._position)
        parent_display_id = Display.GetFromWindow(self._parent)
        viewer_display_id = Display.GetFromWindow(self)
        if parent_display_id != viewer_display_id:
            self._parent.SetFocus()
        else:
            self.SetFocus()

    def Close(self):
        self.Hide()
        self.Pub('on_close')

    def OnClose(self, event):
        self.Close()

    def OnKeyUp(self, event):
        keycode = event.GetKeyCode()
        if keycode in [WXK_ESCAPE, WXK_F11]:
            self.Close()
        event.Skip()
