#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.config import Configuration
from Pokemon_python.directory_config import Directory

class Display_Configuration(Configuration):
    def __init__(self):
        Configuration.__init__(self, Directory.DISPLAY_CONFIG)
        self.TITLE = self._config["TITLE"]
        #Scales
        self.SCALE = self._config["SCALE"]
        self.FRONT_SPRITE_SCALE = self._config["FRONT_SPRITE_SCALE"]
        self.BACK_SPRITE_SCALE = self._config["BACK_SPRITE_SCALE"]
        self.BACKGROUND_SCALE = self._config["BACKGROUND_SCALE"]
        #Sizes
        self.BATTLE_SIZE = self._config["BATTLE_SIZE"]
        self.SPRITE_SIZE = self._config["SPRITE_SIZE"]
        self.BAR_SIZE = self._config["BAR_SIZE"]
        self.LOG_SIZE = self._config["LOG_SIZE"]
        #Colors
        self.GREEN = self._config["GREEN"]
        self.YELLOW = self._config["YELLOW"]
        self.RED = self._config["RED"]
        self.BLACK = self._config["BLACK"]

Display_Config = Display_Configuration()
