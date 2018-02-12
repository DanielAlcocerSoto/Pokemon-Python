#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.config import Configuration
from Pokemon_python.directory_config import Directory

class Font_Configuration(Configuration):
    def __init__(self):
        Configuration.__init__(self, Directory.FONT_CONFIG)
        
        self.LETTER_SIZE = self._config["LETTER_SIZE"]
        self.LINE_SPACING_FACTOR = self._config["LINE_SPACING_FACTOR"]

Font_Config = Font_Configuration()
