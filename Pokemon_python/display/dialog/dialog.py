#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.display.image import Background
from Pokemon_python.display.utils_display import pair_mult_num, scale, transalte
from Pokemon_python.sittings import Directory, Display_Config, Dialog_Config
from Pokemon_python.display.font.font import Font

import pygame

from random import randint


class Dialog_display(Background):
        def __init__(self):
            top_left_location=(0,Display_Config['BATTLE_SIZE'][1])
            Background.__init__(self, Directory['DIALOG_FILE'], top_left_location)
            shift = Dialog_Config['LOG_TEXT_SHIFT']
            text_pos = transalte(top_left_location,shift)
            self._text_pos = scale(pair_mult_num(text_pos, Display_Config['BACKGROUND_SCALE']))
            self.font = Font()

        def set_text(self, text):
            self.font.set_text(text)

        def display(self,SCREEN):
            Background.display(self,SCREEN)
            self.font.display(SCREEN, self._text_pos)
