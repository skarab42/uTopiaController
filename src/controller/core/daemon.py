# coding: utf-8
from __future__ import unicode_literals

import threading

class Daemon(threading.Thread):
    daemon = True

    def __init__(self):
        super(Daemon, self).__init__()
        self._loop = threading.Event()
        self._loop.set()

    def loop(self):
        pass

    def run(self):
        while self._loop.isSet():
            self.loop()

    def stop(self, timeout=None):
        self._loop.clear()
        self.join(timeout)
