#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.display.image import Background, Display
from Pokemon_python.display.utils_display import pair_mult_num, scale, transalte
from Pokemon_python.sittings import Directory, Display_Config, Dialog_Config
from Pokemon_python.display.font.font import Font

import pygame

from random import randint


class Dialog_display(Display):
        def __init__(self):
            top_left_location=(0,Display_Config['BATTLE_SIZE'][1])
            self.bg = Background(Directory['DIALOG_FILE'], top_left_location)
            self.font = Font(top_left_location, Dialog_Config['LOG_TEXT_SHIFT'])
            Display.__init__(self, [self.bg,self.font])

        def set_text(self, text):
            self.font.set_text(text)
