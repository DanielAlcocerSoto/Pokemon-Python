#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg
from Pokemon_python.display.display_config import Display_Config
from Pokemon_python.directory_config import Directory
from Pokemon_python.display.font.font_config import Font_Config

import pygame, sys


class Font:
    def __init__(self):
        self.LETTER_SIZE = int (Font_Config.LETTER_SIZE * Display_Config.SCALE * Display_Config.BACKGROUND_SCALE)
        self._font = pygame.font.Font(Directory.LETTER_FILE, self.LETTER_SIZE)

    def set_text(self, texts):#spit here
        self._text_img = [self._font.render(text, 0, Display_Config.BLACK) for text in texts]

    def display(self, SCREEN, pos):
        for i, t_img in enumerate(self._text_img):
            SCREEN.blit(t_img, (pos[0], pos[1]+self.LETTER_SIZE*Font_Config.LINE_SPACING_FACTOR*i))
