# coding: utf-8
from __future__ import unicode_literals

import wx
import os
import sys
import zipfile
import shutil

from controller.i18n import _
from controller.ui.mixins import FrameMixin
from controller.ui.base import ProjectPanel as BaseProjectPanel
from controller.project import ProjectException

# pubsub topics:
# - project_panel.on_slice(path)
# - project_panel.on_update(project)
# - project_panel.on_refresh(project)

class ProjectPanel(BaseProjectPanel, FrameMixin):
    _name = 'project_panel'
    _project = None
    _settings = None

    def __init__(self, parent, project):
        super(ProjectPanel, self).__init__(parent)
        self._project = project
        self.Sub('project.on_loaded', self.OnProjectLoaded)
        self.Sub('settings.on_loaded', self.OnSettingsLoaded)
        self.Sub('printer.on_print_start', self.OnPrintStart)
        self.Sub('printer.on_print_end', self.OnPrintEnd)
        self.Sub('printer.on_aborted', self.OnPrintEnd)
        self.Sub('printer.on_command_show_slice', self.OnPrinterShowSlice)
        self.Sub('printer.on_command_hide_slice', self.OnPrinterHideSlice)
        self.Sub('printer.on_aborted', self.OnPrintEnd)
        self.Sub('main_frame.on_close', self.OnClose)

    def Setup(self):
        self.SetProjectPath()
        self.EnableControls(False)
        self.open_zip.GetPickerCtrl().SetLabel(_('ZIP'))
        self.open_folder.GetPickerCtrl().SetLabel(_('Folder'))
        self.SetButtonBitmap(self.open_zip.GetPickerCtrl(), 'zip')
        self.SetButtonBitmap(self.open_folder.GetPickerCtrl(), 'folder')

    def OnPrintStart(self):
        self.slice.Disable()
        self.slice.SetValue(0)

    def OnPrintEnd(self):
        self.slice.Enable()

    def OnSettingsLoaded(self, settings):
        self._settings = settings
        lastProject = settings.Get('lastProject')
        if lastProject:
            self.LoadProjectFromFolder(lastProject)

    def OnProjectLoaded(self, project):
        self._settings.Set('lastProject', project.GetPath())
        self.EnableControls(True)
        self.slice.SetValue(0)
        self.ShowSlice(None)

    def SetProjectPath(self, path=None):
        if path is None:
            path = _('No project loaded')
        self.project_path.SetToolTipString(path)
        if path is not None:
            path = os.path.basename(path)
        self.project_path.SetValue(path)

    def EnableControls(self, enable=True):
        self.exposure_time.Enable(enable)
        self.lifting_speed.Enable(enable)
        self.lifting_height.Enable(enable)
        self.slice.Enable(enable)

    def RefreshSettings(self):
        self.Log(_('Refresh project settings...'))
        layers_number = int(self._project.GetSetting('layersNumber'))
        layers_height = float(self._project.GetSetting('layersHeight'))
        exposure_time = int(self._project.GetSetting('exposureTime'))
        lifting_speed = int(self._project.GetSetting('liftingSpeed'))
        lifting_height = float(self._project.GetSetting('liftingHeight'))
        lifting_offset = float(lifting_height - layers_height)
        total_height = layers_number * layers_height
        self._project.SetSetting('totalHeight', total_height)
        self._project.SetSetting('liftingOffset', lifting_offset)
        self.total_height.SetLabel(str(total_height))
        self.layers_number.SetLabel(str(layers_number))
        self.layers_height.SetLabel(str(layers_height))
        self.exposure_time.SetValue(exposure_time)
        self.lifting_speed.SetValue(lifting_speed)
        self.lifting_height.SetValue(lifting_height)
        self.slice.SetMax(layers_number)
        self.Pub('on_refresh', project=self._project)

    def LoadProjectFromFolder(self, path):
        self.Log(_('Loading: %s'), path)
        try:
            self._project.Load(path)
            self.SetProjectPath(path)
            self.RefreshSettings()
        except ProjectException as e:
            return self.Error(unicode(e))

    def LoadProjectFromZIP(self, path):
        if not zipfile.is_zipfile(path):
            return self.Error(_('Invalid ZIP file !\n%s'), path)
        zip_path = os.path.dirname(path)
        zip_file = os.path.basename(path)
        zip_folder = zip_file[:-4]
        zip_target = os.path.join(zip_path, zip_folder)
        args = (zip_file, zip_target)
        response = self.Question(_('Unzip "%s" ?\n%s'), args)
        if response == wx.ID_NO:
            return None
        if os.path.isdir(zip_target):
            question = _('Project folder already exists, overwrite it ?\n%s')
            if self.Question(question, zip_target) == wx.ID_NO:
                return None
            shutil.rmtree(zip_target)
        self.Log(_('Unzip "%s" to "%s"'), (zip_file, zip_target))
        try:
            os.mkdir(zip_target.encode(sys.getfilesystemencoding()))
        except Exception as e:
            return self.Error(_('Access denied !\n%s'), zip_target)
        try:
            zip_file = zipfile.ZipFile(path, 'r')
            zip_file.extractall(zip_target)
        except Exception as e:
            return self.Error(unicode(e))
        self.LoadProjectFromFolder(zip_target)

    def OnProjectChanged(self, event):
        path = event.GetPath()
        if path.endswith('.zip'):
            self.LoadProjectFromZIP(path)
        else:
            self.LoadProjectFromFolder(path)

    def UpdateSettings(self):
        if not self._project.Loaded():
            return None
        self._debounce = None
        self.Log(_('Update project settings...'))
        layers_number = int(self.layers_number.GetLabel())
        layers_height = float(self.layers_height.GetLabel())
        exposure_time = int(self.exposure_time.GetValue())
        lifting_speed = int(self.lifting_speed.GetValue())
        lifting_height = int(self.lifting_height.GetValue())
        lifting_offset = lifting_height - layers_height
        total_height = layers_number * layers_height
        self._project.SetSetting('totalHeight', total_height)
        self._project.SetSetting('layersNumber', layers_number)
        self._project.SetSetting('layersHeight', layers_height)
        self._project.SetSetting('exposureTime', exposure_time)
        self._project.SetSetting('liftingSpeed', lifting_speed)
        self._project.SetSetting('liftingHeight', lifting_height)
        self._project.SetSetting('liftingOffset', lifting_offset)
        self.Pub('on_update', project=self._project)

    def OnSettingsChange(self, event):
        self.UpdateSettings()

    def ShowSlice(self, slice_num=None):
        slice_path = None
        if slice_num:
            slice_path = self._project.GetSlicePath(slice_num)
        self.Pub('on_slice', path=slice_path)

    def OnSliceSlide(self, event):
        slice_num = self.slice.GetValue()
        if slice_num:
            self.ShowSlice(slice_num)

    def OnPrinterShowSlice(self, command, args):
        self.slice.SetValue(args)
        self.ShowSlice(args)

    def OnPrinterHideSlice(self, command, args):
        self.ShowSlice(0)

    def OnClose(self):
        if self._project.Loaded():
            self.Log(_('Save project settings...'))
            self._project.SaveSettings()
