#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.display.image import Background, Display
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg
from Pokemon_python.display.display_config import Display_Config

import pygame, sys

from random import randint

#LOCAL DISPLAY CONFIGURATIONS
LOG_NAME  = 'log'
LOG_TEXT_SHIFT=(17,7)
LETTER_SIZE = int (10 * Display_Config.SCALE * Display_Config.BACKGROUND_SCALE)
LINE_SPACING_FACTOR = 1.5

class Log (Background):
    def __init__(self, top_left_location, font):
        Background.__init__(self, LOG_NAME, top_left_location)
        text_pos = (top_left_location[0]+LOG_TEXT_SHIFT[0], top_left_location[1]+LOG_TEXT_SHIFT[1])
        self._text_pos = scale(pair_mult_num(text_pos, Display_Config.BACKGROUND_SCALE))
        self.set_text('')
        self.font=font

    def set_text(self, texts):
        self._text_img = [self.font.render(text, 0, Display_Config.BLACK) for text in texts]

    def display(self,SCREEN):
        Background.display(self,SCREEN)
        for i, t_img in enumerate(self._text_img):
            SCREEN.blit(t_img, (self._text_pos[0],self._text_pos[1]+LETTER_SIZE*LINE_SPACING_FACTOR*i))


class Dialog_display(Display):
    def __init__(self, font):
        self.dialog_bg = Log((0,Display_Config.BATTLE_SIZE[1]), font)
        Display.__init__(self, font, [self.dialog_bg])

    def set_text(self,text):
        self.dialog_bg.set_text(text)
