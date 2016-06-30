# coding: utf-8
from __future__ import unicode_literals

import time

import wx

from controller.i18n import _
from controller.ui.mixins import FrameMixin
from controller.ui.base import PrintPanel as BasePrintPanel

class PrintPanel(BasePrintPanel, FrameMixin):
    _name = 'print_panel'
    _printer = None
    _timer = None
    _project = None
    _settings = None
    _elapsed_time = 0
    _estimated_time = 0

    def __init__(self, parent, printer):
        super(PrintPanel, self).__init__(parent)
        self._printer = printer
        self.Sub('project.on_loaded', self.OnProjectLoaded)
        self.Sub('settings.on_loaded', self.OnSettingsLoaded)
        self.Sub('project_panel.on_update', self.OnProjectUpdate)
        self.Sub('project_panel.on_refresh', self.OnProjectRefresh)
        self.Sub('settings_panel.on_refresh', self.OnSettingsUpdate)
        self.Sub('printer.on_print_start', self.OnPrintStart)
        self.Sub('printer.on_print_end', self.OnPrintEnd)
        self.Sub('printer.on_aborted', self.OnPrinterAborted)
        self.Sub('printer.on_resumed', self.OnPrinterResumed)
        self.Sub('printer.on_paused', self.OnPrinterPaused)
        self.Sub('printer.on_disconnected', self.OnPrinterDisconnected)
        self.Sub('main_frame.on_close', self.OnClose)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self._timer = wx.Timer(self)
        self._timer.Start(1000)
        self.ResetButtons()
        self.ResetLabels()

    def Setup(self):
        pass

    def ResetLabels(self):
        self.end_time.SetLabel('n/a')
        self.start_time.SetLabel('n/a')
        self.elapsed_time.SetLabel('n/a')
        self.estimated_time.SetLabel('n/a')

    def ResetButtons(self):
        self.start_stop.Enable()
        self.pause_resume.Disable()
        self.start_stop.SetLabel(_('Start'))
        self.pause_resume.SetLabel(_('Pause'))
        self.start_stop.SetToolTipString(_('Start'))
        self.pause_resume.SetToolTipString(_('Pause'))

    def OnProjectLoaded(self, project):
        self._project = project

    def EstimateTime(self):
        first_layers_time = 0
        first_layers_count = 0
        group1 = self._settings.Get('layersGroup.1')
        group2 = self._settings.Get('layersGroup.2')
        group3 = self._settings.Get('layersGroup.3')
        layers_number = self._project.GetSetting('layersNumber')
        exposure_time = self._project.GetSetting('exposureTime')
        lifting_speed = self._project.GetSetting('liftingSpeed')
        lifting_height = self._project.GetSetting('liftingHeight')
        lifting_offset = self._project.GetSetting('liftingOffset')
        if group1['enable']:
            first_layers_count += group1['layers']
            first_layers_time += (group1['layers'] * group1['exposureTime'])
        if group2['enable']:
            first_layers_count += group2['layers']
            first_layers_time += (group2['layers'] * group2['exposureTime'])
        if group3['enable']:
            first_layers_count += group3['layers']
            first_layers_time += (group3['layers'] * group3['exposureTime'])
        if first_layers_count:
            first_layers_time -= (exposure_time * first_layers_count)
        lifting_length = lifting_height - (lifting_offset / 2)
        lifting_time = (60000 / (lifting_speed / lifting_length)) * 2;
        one_slice_time = lifting_time + exposure_time + 250
        estimated_time = one_slice_time * layers_number
        seconds = (estimated_time + first_layers_time) / 1000
        return seconds

    def GetTime(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return (h, m, s)

    def RefreshEstimateTime(self):
        estimated_time = self.EstimateTime()
        if not self._printer.Printing():
            self._estimated_time = estimated_time
        estimated_time = self.GetTime(estimated_time)
        self.estimated_time.SetLabel('%d:%02d:%02d' % estimated_time)

    def RefreshValues(self):
        if self._project and self._settings:
            self.RefreshEstimateTime()

    def OnSettingsLoaded(self, settings):
        self._settings = settings
        self.RefreshValues()

    def OnProjectUpdate(self, project):
        self.RefreshValues()

    def OnProjectRefresh(self, project):
        self.RefreshValues()

    def OnSettingsUpdate(self, settings):
        self.RefreshValues()

    def RemainingTime(self):
        return self._estimated_time - self._elapsed_time

    def RefreshEndTime(self):
        remaining_time  = self.RemainingTime()
        end_time = time.time() + remaining_time
        local_end_time = time.localtime(end_time)
        local_end_time_string = time.strftime("%H:%M:%S", local_end_time)
        self.end_time.SetLabel(local_end_time_string)

    def OnTimer(self, event):
        if self._printer.Printing():
            if not self._printer.Paused():
                self._elapsed_time += 1
                elapsed_time = self.GetTime(self._elapsed_time)
                self.elapsed_time.SetLabel('%d:%02d:%02d' % elapsed_time)
            self.RefreshEndTime()

    def _SendCommands(self):
        layers_number = int(self._project.GetSetting('layersNumber'))
        layers_height = float(self._project.GetSetting('layersHeight'))
        exposure_time = int(self._project.GetSetting('exposureTime'))
        lifting_speed = int(self._project.GetSetting('liftingSpeed'))
        lifting_height = float(self._project.GetSetting('liftingHeight'))
        lifting_offset = float(self._project.GetSetting('liftingOffset'))
        lg1 = self._settings.Get('layersGroup.1')
        lg2 = self._settings.Get('layersGroup.2')
        lg3 = self._settings.Get('layersGroup.3')
        layer_num = 0
        def SendCommand(exposure_time):
            self._printer.SendLiftUp(lifting_height, lifting_speed)
            self._printer.SendLiftDown(lifting_offset, lifting_speed)
            self._printer.SendShowSlice(layer_num)
            self._printer.SendLightOn()
            self._printer.SendWait(exposure_time)
            self._printer.SendLightOff()
            self._printer.SendHideSlice(layer_num)
        self._printer.SendPrintStart()
        self._printer.SendRelativeMode()
        if lg1['enable']:
            for layer in range(lg1['layers']):
                layer_num += 1
                SendCommand(lg1['exposureTime'])
        if lg2['enable']:
            for layer in range(lg2['layers']):
                layer_num += 1
                SendCommand(lg2['exposureTime'])
        if lg3['enable']:
            for layer in range(lg3['layers']):
                layer_num += 1
                SendCommand(lg3['exposureTime'])
        for layer in range(layers_number - layer_num):
            layer_num += 1
            SendCommand(exposure_time)
        self._printer.SendPrintEnd()

    def OnPrintStart(self):
        self.start_stop.Enable()
        self.pause_resume.Enable()
        start_time = time.time()
        local_start_time = time.localtime(start_time)
        local_start_time_string = time.strftime("%H:%M:%S", local_start_time)
        self.start_time.SetLabel(local_start_time_string)
        self.start_stop.SetToolTipString(_('Stop'))
        self.start_stop.SetLabel(_('Stop'))
        self.RefreshEndTime()

    def OnPrinterDisconnected(self, port):
        self.ResetButtons()

    def OnPrintEnd(self):
        self.Log(_('Job ended...'))
        self.ResetButtons()
        wx.Bell()

    def OnPrinterAborted(self):
        self.Log(_('Job aborted...'))
        self.ResetButtons()

    def OnPrinterResumed(self):
        self.Log(_('Job resumed...'))
        self.pause_resume.SetLabel(_('Pause'))
        self.pause_resume.SetToolTipString(_('Pause'))

    def OnPrinterPaused(self):
        self.Log(_('Job paused...'))
        self.pause_resume.Enable()
        self.pause_resume.SetLabel(_('Resume'))
        self.pause_resume.SetToolTipString(_('Resume'))

    def StartJob(self):
        if self._printer.Disconnected():
            return self.Error(_('Printer not connected !'))
        if self._printer.Printing():
            return self.Error(_('Job already started !'))
        try:
            self.start_stop.SetLabel(_('Wait...'))
            self.start_stop.Disable()
            self._elapsed_time = 0
            self._SendCommands()
        except JobException as e:
            self.Error(unicode(e))

    def StopJob(self):
        if not self._printer.Printing():
            return self.Error(_('Job already stoped !'))
        if self.Question(_('Abort current job ?')) == wx.ID_YES:
            try:
                self.start_stop.SetLabel(_('Wait...'))
                self.pause_resume.Disable()
                self.start_stop.Disable()
                self._printer.Abort()
            except JobException as e:
                self.Error(unicode(e))

    def PauseJob(self):
        if self._printer.Paused():
            return self.Error(_('Job already paused !'))
        try:
            self.pause_resume.SetLabel(_('Wait...'))
            self.pause_resume.Disable()
            self.start_stop.Disable()
            self._printer.Pause()
        except JobException as e:
            self.Error(unicode(e))

    def ResumeJob(self):
        if not self._printer.Paused():
            return self.Error(_('Job already running !'))
        try:
            self.start_stop.Enable()
            self._printer.Resume()
        except JobException as e:
            self.Error(unicode(e))

    def OnStartStopClick(self, event):
        if self._printer.Printing():
            self.StopJob()
        else:
            self.StartJob()

    def OnPauseResumeClick(self, event):
        if self._printer.Paused():
            self.ResumeJob()
        else:
            self.PauseJob()

    def OnClose(self):
        pass
