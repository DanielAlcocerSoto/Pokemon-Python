#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.config import Configuration
from Pokemon_python.directory_config import Directory

class Dialog_Configuration(Configuration):
    def __init__(self):
        Configuration.__init__(self, Directory.DIALOG_CONFIG)
        self.LOG_TEXT_SHIFT = self._config["LOG_TEXT_SHIFT"]

Dialog_Config = Dialog_Configuration()
