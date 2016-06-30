# coding: utf-8
from __future__ import unicode_literals

import os
import json

from controller.i18n import _
from controller.pubsub import pubsub

class SettingsException(Exception):
    def __init__(self, message, args=None):
        if args is not None:
            message %= args
        super(SettingsException, self).__init__(message)

# pubsub topics:
# - settings.on_load(path)
# - settings.on_loaded(settings)
# - settings.on_set(name, value)
# - settings.on_merge(settings)
# - settings.on_save(settings)
# - settings.on_saved(settings)
# - settings.on_error(message)

class Settings(object):
    _name = 'core_settings'
    _path = None
    _loaded = False
    _settings = {}

    def Pub(self, topic, **kwargs):
        pubsub.publish('%s.%s' % (self._name, topic), **kwargs)

    def Sub(self, topic, callback):
        pubsub.subscribe(topic, callback)

    def Error(self, message, args=None):
        if args is not None:
            message %= args
        self.Pub('on_error', message=message)
        raise SettingsException(message)

    def GetSettings(self):
        return self._settings

    def Get(self, name, default=None):
        try:
            return self._settings[name]
        except:
            return default

    def Set(self, name, value):
        self.Pub('on_set', name=name, value=value)
        self._settings[name] = value

    def Merge(self, settings):
        self.Pub('on_merge', settings=settings)
        self._settings.update(settings)

    def GetPath(self):
        return self._path

    def SetPath(self, path):
        if not os.path.isfile(path):
            self.Error(_('Not a valid file !\n%s'), path)
        self._path = os.path.realpath(path)

    def Loaded(self):
        return self._loaded

    def Load(self, path=None):
        self.Pub('on_load', path=path)
        if path is not None:
            self.SetPath(path)
        try:
            self._settings = json.load(open(self._path, 'r'))
            self.Pub('on_loaded', settings=self)
            self._loaded = True
        except Exception as e:
            self.Error('%s\n%s', (unicode(e), self._path))

    def Save(self):
        self.Pub('on_save', settings=self)
        try:
            json.dump(self._settings, open(self._path, 'w'),
                      sort_keys=True, indent=4, separators=(',', ': '))
            self.Pub('on_saved', settings=self)
        except Exception as e:
            self.Error(unicode(e))
