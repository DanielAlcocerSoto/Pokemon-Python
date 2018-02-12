#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.config import Configuration
from Pokemon_python.directory_config import Directory

class Battle_Configuration(Configuration):
    def __init__(self):
        Configuration.__init__(self, Directory.BATTLE_CONFIG)
        self.POS_BAR_F2 = self._config["POS_BAR_F2"]
        self.POS_BAR_F1 = self._config["POS_BAR_F1"]
        self.POS_BAR_A1 = self._config["POS_BAR_A1"]
        self.POS_BAR_A2 = self._config["POS_BAR_A2"]

Battle_Config = Battle_Configuration()
