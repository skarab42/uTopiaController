# coding: utf-8
from __future__ import unicode_literals

import wx

from controller.i18n import _
from controller.ui.mixins import FrameMixin
from controller.ui.base import SettingsPanel as BaseSettingsPanel
from controller.core.settings import SettingsException

# pubsub topics:
# - settings_panel.on_update(settings)
# - settings_panel.on_refresh(settings)

class SettingsPanel(BaseSettingsPanel, FrameMixin):
    _name = 'settings_panel'
    _file_path = './settings.json'
    _settings = None

    def __init__(self, parent, settings):
        super(SettingsPanel, self).__init__(parent)
        self._settings = settings
        self.Sub('settings.on_loaded', self.OnSettingsLoaded)
        self.Sub('main_frame.on_close', self.OnClose)

    def Setup(self):
        try:
            self._settings.Load(self._file_path)
        except SettingsException as e:
            self.Error(unicode(e))

    def RefreshPresetsList(self):
        self.Log(_('Refresh presets list...'))
        self.presets.Clear()
        for name in sorted(self._settings.Get('presets', {})):
            self.presets.Append(name)

    def SetPresetsSelected(self, name=None):
        if name is None:
            name = self._settings.Get('presetsName')
        presets_position = self.presets.FindString(name)
        self.presets.SetSelection(presets_position)

    def RefreshSettings(self):
        self.Log(_('Refresh custom settings...'))
        lg1 = self._settings.Get('layersGroup.1')
        lg2 = self._settings.Get('layersGroup.2')
        lg3 = self._settings.Get('layersGroup.3')
        self.layers_group_1_count.SetValue(lg1['layers'])
        self.layers_group_2_count.SetValue(lg2['layers'])
        self.layers_group_3_count.SetValue(lg3['layers'])
        self.layers_group_1_time.SetValue(lg1['exposureTime'])
        self.layers_group_2_time.SetValue(lg2['exposureTime'])
        self.layers_group_3_time.SetValue(lg3['exposureTime'])
        self.layers_group_1_count.Enable(True)
        self.layers_group_1_time.Enable(lg1['enable'])
        self.layers_group_2_count.Enable(lg1['enable'])
        self.layers_group_2_time.Enable(lg2['enable'])
        self.layers_group_3_count.Enable(lg2['enable'])
        self.layers_group_3_time.Enable(lg3['enable'])
        self.Pub('on_refresh', settings=self._settings)

    def OnSettingsLoaded(self, settings):
        self.RefreshPresetsList()
        self.SetPresetsSelected()
        self.RefreshSettings()

    def PresetsIsModified(self, name):
        names = self._settings.Get('presets')
        if name not in names.keys():
            return True
        presets = self._settings.GetPresets(name)
        current_presets = self._settings.GetCurrentPresets()
        return presets != current_presets

    def AskForSavePresets(self, name=None):
        if name is None:
            name = self._settings.Get('presetsName')
        if not self.PresetsIsModified(name):
            return None
        question = _('Presets "%s" has been modified !\nSave changes ?')
        if self.Question(question, name) == wx.ID_YES:
            self.Log(_('Save "%s" presets...'), name)
            self._settings.SaveCurrentPresets(name)

    def LoadPresets(self, name):
        self.Log(_('Loading presets: %s'), name)
        self._settings.LoadPresets(name)
        self.RefreshSettings()

    def OnPresetsSelected(self, event):
        self.AskForSavePresets()
        self.LoadPresets(self.presets.GetValue())

    def UpdateSettings(self):
        self.Log(_('Update custom settings...'))
        lg1_layers = self.layers_group_1_count.GetValue()
        lg2_layers = self.layers_group_2_count.GetValue()
        lg3_layers = self.layers_group_3_count.GetValue()
        lg1_time = self.layers_group_1_time.GetValue()
        lg2_time = self.layers_group_2_time.GetValue()
        lg3_time = self.layers_group_3_time.GetValue()
        lg1 = bool(lg1_layers)
        lg2 = bool(lg2_layers) and lg1
        lg3 = bool(lg3_layers) and lg2
        group1 = dict(layers=lg1_layers, exposureTime=lg1_time, enable=lg1)
        group2 = dict(layers=lg2_layers, exposureTime=lg2_time, enable=lg2)
        group3 = dict(layers=lg3_layers, exposureTime=lg3_time, enable=lg3)
        self._settings.Set('layersGroup.1', group1)
        self._settings.Set('layersGroup.2', group2)
        self._settings.Set('layersGroup.3', group3)
        self.Pub('on_update', settings=self._settings)
        self.RefreshSettings()

    def OnSettingsChange(self, event):
        self.UpdateSettings()

    def SavePresets(self, name):
        self.Log(_('Save current presets...'))
        self._settings.SaveCurrentPresets(name)
        self.RefreshPresetsList()
        self.SetPresetsSelected()

    def OnSaveClick(self, event):
        name = self.presets.GetValue()
        if self.PresetsIsModified(name):
            self.SavePresets(name)
            self.Alert(_('Presets "%s" saved !'), name)
        else:
            self.Alert(_('No changes in "%s" to save !'), name)

    def DeletePresets(self, name):
        if name == 'Defaults':
            return self.Alert(_('"Defaults" presets is protected !'))
        if self.Question(_('Delete "%s" presets ?'), name) == wx.ID_YES:
            self.Log(_('Delete "%s" presets...'), name)
            presets = self._settings.Get('presets', {})
            position = self.presets.FindString(name)
            del presets[name]
            self._settings.Set('presets', presets)
            name = self.presets.GetString(position - 1)
            self.LoadPresets(name)
            self.SaveSettings()
            self.RefreshPresetsList()
            self.SetPresetsSelected()

    def OnDeleteClick(self, event):
        self.DeletePresets(self.presets.GetValue())

    def SaveSettings(self):
        if self._settings.Loaded():
            self.Log(_('Save custom settings...'))
            self._settings.Save()

    def OnClose(self):
        self.AskForSavePresets()
        self.SaveSettings()
