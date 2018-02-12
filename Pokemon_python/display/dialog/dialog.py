#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.display.image import Background, Display
from Pokemon_python.display.utils_display import pair_mult_num, scale
from Pokemon_python.display.display_config import Display_Config
from Pokemon_python.display.font.font import Font

import pygame, sys

from random import randint

#LOCAL DISPLAY CONFIGURATIONS
LOG_NAME  = 'log'
LOG_TEXT_SHIFT=(17,7)


class Log (Background):
    def __init__(self, top_left_location):
        Background.__init__(self, LOG_NAME, top_left_location)
        text_pos = (top_left_location[0]+LOG_TEXT_SHIFT[0], top_left_location[1]+LOG_TEXT_SHIFT[1])
        self._text_pos = scale(pair_mult_num(text_pos, Display_Config.BACKGROUND_SCALE))
        self.font = Font()
        self.set_text('')

    def set_text(self, text):
        self.font.set_text(text)

    def display(self,SCREEN):
        Background.display(self,SCREEN)
        self.font.display(SCREEN, self._text_pos)


class Dialog_display(Display):
    def __init__(self):
        self.dialog_bg = Log((0,Display_Config.BATTLE_SIZE[1]))
        Display.__init__(self, [self.dialog_bg])

    def set_text(self,text):
        self.dialog_bg.set_text(text)
