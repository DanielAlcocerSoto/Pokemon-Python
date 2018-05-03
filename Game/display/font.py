#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Font class.
This class allows to write a text in the screen. It can decide the position
the size if the color of the text.

It contains the following class:

	Font
"""

# Local imports
from Configuration.settings import Directory, Display_Config, Font_Config
from Game.display.utils_display import translate, scale_bg

# 3rd party imports
import pygame

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
    Class to Font to write text in screen.
"""
class Font:
    def __init__(self, reference, shift, letter_size=Font_Config['LETTER_SIZE']):
        """
            Args:
                reference ('int','int'): A reference point.
                shift ('int','int'): A shift to be made to the reference point.
                letter_size (int): The size of the text.

            Action:
                Create an image to write on the screen in 'reference' position
                moved 'shift', with a size of 'letter_size'.
        """
        self.pos = scale_bg(translate(reference, shift))
        f_scale = Display_Config['SCALE'] * Display_Config['BACKGROUND_SCALE']
        self.LETTER_SIZE = int (letter_size * f_scale)
        self._font = pygame.font.Font(Directory['FONT_FILE'], self.LETTER_SIZE)
        self.set_text('')

    """
    	Function to set a text that will be displayed.
    """
    def set_text(self, text, color_name = "BLACK"):
        """
            Args:
                text ('str'): The text to show.
                color_name ('str'): The key name of the color of the text.

            Action:
                Set the text to display and the color of it.
        """
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

        self._text_img = [self._font.render(text, 1, Display_Config[color_name])
                          for text in texts.values()]

    """
        Funcion to display the text.
    """
    def display(self, SCREEN):
        for i, t_img in enumerate(self._text_img):
            space = self.LETTER_SIZE*Font_Config['LINE_SPACING_FACTOR']*i
            SCREEN.blit(t_img, (self.pos[0], self.pos[1]+space))
