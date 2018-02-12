#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.config import Configuration

class Directory_Configuration(Configuration):
    def __init__(self):
        Configuration.__init__(self,'directory_config')
        #Config file path
        self.DISPLAY_CONFIG = self._config["DISPLAY_CONFIG"]
        self.BATTLE_CONFIG = self._config["BATTLE_CONFIG"]
        self.DIALOG_CONFIG = self._config["DIALOG_CONFIG"]
        self.MUSIC_CONFIG = self._config["MUSIC_CONFIG"]
        self.FONT_CONFIG = self._config["FONT_CONFIG"]
        #name files
        self.POKE_FILE = self._config["POKE_FILE"]
        self.TYPE_FILE = self._config["TYPE_FILE"]
        self.MOVE_FILE = self._config["MOVE_FILE"]
        self.ICON_FILE = self._config["ICON_FILE"]
        self.DIALOG_FILE = self._config["DIALOG_FILE"]
        self.LETTER_FILE = self._config["LETTER_FILE"]
        self.HEALTH_FILE = self._config["HEALTH_FILE"]
        self.BACKGROUND_NAME = self._config["BACKGROUND_NAME"]
        #General directories
        self.DIR_JSON = self._config["DIR_JSON"]
        self.DIR_MUSIC = self._config["DIR_MUSIC"]
        self.DIR_CELLS = self._config["DIR_CELLS"]
        self.DIR_IMAGES = self._config["DIR_IMAGES"]
        self.DIR_SPRITES = self._config["DIR_SPRITES"]
        self.DIR_BACKGROUND = self._config["DIR_BACKGROUND"]

Directory = Directory_Configuration()
