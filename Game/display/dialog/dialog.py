#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

# Local imports
from Game.settings import Directory, Display_Config, Dialog_Config
from Game.display.utils_display import pair_mult_num, scale, transalte
from Game.display.image import Background, Display
from Game.display.font.font import Font

# 3rd party imports
import pygame

# General imports
from random import randint

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""

"""
class Dialog_display(Display):
        def __init__(self):
            top_left_location=(0,Display_Config['BATTLE_SIZE'][1])
            self.bg = Background(Directory['DIALOG_FILE'], top_left_location)
            self.font = Font(top_left_location, Dialog_Config['LOG_TEXT_SHIFT'])
            Display.__init__(self, [self.bg,self.font])

        def set_text(self, text):
            self.font.set_text(text)
