# coding: utf-8
from __future__ import unicode_literals

import os
import json

from wx.lib.pubsub import setupkwargs, pub

from controller.i18n import _
from controller.core.settings import Settings, SettingsException

class ProjectException(Exception):
    def __init__(self, message, args=None):
        if args is not None:
            message %= args
        super(ProjectException, self).__init__(message)

# pubsub topics:
# - project_settings.on_load(path)
# - project_settings.on_loaded(settings)
# - project_settings.on_set(name, value)
# - project_settings.on_merge(settings)
# - project_settings.on_save(settings)
# - project_settings.on_saved(settings)
# - project_settings.on_error(message)

class ProjectSettings(Settings):
    _name = 'project_settings'

# pubsub topics:
# - project.on_load(path)
# - project.on_loaded(project)
# - project.on_error(message)

class Project(object):
    _name = 'project'
    _path = None
    _loaded = False
    _settings = None
    _settings_filename = 'slacer.json'

    def __init__(self):
        super(Project, self).__init__()
        self._settings = ProjectSettings()

    def Pub(self, topic, **kwargs):
        pub.sendMessage('%s.%s' % (self._name, topic), **kwargs)

    def Sub(self, topic, callback):
        pub.subscribe(callback, topic)

    def Error(self, message, args=None):
        if args is not None:
            message %= args
        self.Pub('on_error', message=message)
        raise ProjectException(message)

    def Loaded(self):
        return self._settings.Loaded()

    def LoadSettings(self):
        self._settings.Load(os.path.join(self._path, self._settings_filename))

    def SaveSettings(self):
        self._settings.Save()

    def GetSettings(self):
        return self._settings.GetSettings()

    def GetSetting(self, name, default=None):
        return self._settings.Get(name, default)

    def SetSetting(self, name, value):
        self._settings.Set(name, value)

    def MergeSettings(self, settings):
        self._settings.Merge(settings)

    def GetPath(self):
        return self._path

    def SetPath(self, path):
        if not os.path.isdir(path):
            self.Error(_('Not a valid folder !\n%s'), path)
        self._path = path

    def Load(self, path):
        self.Pub('on_load', path=path)
        try:
            self.SetPath(path)
            self.LoadSettings()
            self.Pub('on_loaded', project=self)
        except SettingsException as e:
            self.Error(unicode(e))

    def GetSlicePath(self, slice_num):
        image_directory = self.GetSetting('imageDirectory', 'slices')
        return os.path.join(self._path, image_directory, '%i.png' % slice_num)
