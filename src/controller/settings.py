# coding: utf-8
from __future__ import unicode_literals

from controller.i18n import _
from controller.core.settings import Settings as CoreSettings

# pubsub topics:
# - settings.on_load(path)
# - settings.on_loaded(settings)
# - settings.on_set(name, value)
# - settings.on_merge(settings)
# - settings.on_save(settings)
# - settings.on_saved(settings)
# - settings.on_error(message)

class Settings(CoreSettings):
    _name = 'settings'

    def GetCurrentPresets(self):
        return {
            'layersGroup.1': self.Get('layersGroup.1'),
            'layersGroup.2': self.Get('layersGroup.2'),
            'layersGroup.3': self.Get('layersGroup.3')
        }

    def SaveCurrentPresets(self, name=None):
        if name is None:
            name = self.Get('presetsName')
        c_presets = self.GetCurrentPresets()
        presets = self.Get('presets')
        presets[name] = c_presets
        self.Set('presetsName', name)
        self.Set('presets', presets)
        self.Save()

    def GetPresets(self, name):
        presets = self.Get('presets')
        try:
            return presets[name]
        except:
            self.Error(_('Presets "%s" not defined !'), name)

    def LoadPresets(self, name):
        self.Set('presetsName', name)
        self.Merge(self.GetPresets(name))
