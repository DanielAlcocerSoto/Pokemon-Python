#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Dialog_display class.
This class show the dialog section and allows to write text to it

It contains the following class:

	Dialog_display
"""

# Local imports
from Configuration.settings import Directory, Display_Config, Dialog_Config
from Game.display.utils_display import transalte
from Game.display.image import Background, Display
from Game.display.font import Font

# 3rd party imports
import pygame

# General imports
from random import randint

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
    Class to display the dialog section and write text to it.
"""
class Dialog_display(Display):
    def __init__(self):
        """
            Args: -

            Action:
                Create an extension of the "Display" class to display the
				dialog section of the game.
        """
        top_left_location=(0,Display_Config['BATTLE_SIZE'][1])
        bg = Background(Directory['DIALOG_FILE'], top_left_location)
        self.font = Font(top_left_location, Dialog_Config['LOG_TEXT_SHIFT'])
        Display.__init__(self, [bg,self.font])

    """
    	Function to set a text that will be displayed in the dialog section.
    """
    def set_text(self, text):
        """
            Args:
                text ('str'): The text to display.

            Action:
                Set the text to display in the dialog section.
        """
        self.font.set_text(text)
