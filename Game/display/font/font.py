#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

# Local imports
from Game.settings import Directory, Display_Config, Font_Config
from Game.display.utils_display import transalte, scale_bg

# 3rd party imports
import pygame

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""

"""
class Font:
    def __init__(self, reference, shift, letter_size=Font_Config['LETTER_SIZE'] ):
        self.pos = scale_bg(transalte(reference, shift))
        self.LETTER_SIZE = int (letter_size * Display_Config['SCALE'] * Display_Config['BACKGROUND_SCALE'])
        self._font = pygame.font.Font(Directory['FONT_FILE'], self.LETTER_SIZE)
        self.set_text('')

    def set_text(self, text, color_name = "BLACK"):
        counter_char = line = 0
        texts = {}
        for word in text.split(' '):
            counter_char += len(word)
            if line in texts and counter_char<=Font_Config['MAX_LENGHT']:
                texts[line] += ' '+word
                counter_char += 1
            else:
                line += 1
                texts[line] = word
                counter_char = len(word)+1

        self._text_img = [self._font.render(text, 1, Display_Config[color_name]) for text in texts.values()]

    def display(self, SCREEN):
        for i, t_img in enumerate(self._text_img):
            SCREEN.blit(t_img, (self.pos[0], self.pos[1]+self.LETTER_SIZE*Font_Config['LINE_SPACING_FACTOR']*i))
