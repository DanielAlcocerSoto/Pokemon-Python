#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.config import Configuration
from Pokemon_python.directory_config import Directory

class Music_Configuration(Configuration):
    def __init__(self):
        Configuration.__init__(self, Directory.MUSIC_CONFIG)
        self.VOLUME = self._config["VOLUME"]

        self.NAME_MUSIC = self._config["NAME_MUSIC"]
        self.NAME_GEN = self._config["NAME_GEN"]

        self.EXTENSION = self._config["EXTENSION"]

Music_Config = Music_Configuration()
