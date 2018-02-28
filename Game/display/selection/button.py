#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Buttons classes.
These classes show relevant information of the buttons in the correct position,
besides allowing to detect if they have been clicked.

It contains the following classes:

	Button
    Button_Move
    Button_Target
    Button_Cancel
"""

# Local imports
from Game.settings import Directory, Display_Config, Select_Config
from Game.utils_data_base import load_cell
from Game.display.image import Background
from Game.display.utils_display import scale_bg, transalte, num_to_text
from Game.display.font.font import Font

# 3rd party imports
import pygame

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	General class to represents a button.
"""
class Button:
    def __init__(self, position_name, name_img, obj):
        """
            Args:
                position_name ('str'): The key to obtain the position of this
                                       button.
                name_img ('str'): The key to obtain name of the button image.
                obj (class:'Object_Into'): The object to be displayed by the
                                           button.
                    Note: Object_Into is a general class. Some of the classes
                    that extends this class are Pokemon or Move.

            Action:
                Create an General Button to show relevant information of 'obj'
                and allows to detect if it has been clicked.
        """
        top_left_location = Select_Config[position_name]
        height = Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1]
        shift = (0, height)
        self.location_pre_scale = transalte(top_left_location, shift)
        self._location = scale_bg(self.location_pre_scale)
        image = load_cell(name_img)
        self._image = pygame.transform.scale(image, scale_bg(image.get_size()))

        self.obj = obj
        button_shift =  Select_Config['BUTTON_NAME_SHIFT']
        self.font_name = Font(self.location_pre_scale, button_shift)
        self.font_name.set_text('' if obj == None else obj.name() )

    """
        Funcion to display this button.
    """
    def display(self,SCREEN):
        SCREEN.blit(self._image, self._location)
        self.font_name.display(SCREEN)

    """
        Funtion that returns True if 'point' is inside of this button.
        (tuple:('int','int') --> 'bool')
    """
    def point_inside(self, point):
        left, top = self._location
        width, height = self._image.get_size()
        rect = pygame.Rect(left, top, width, height)
        return rect.collidepoint(point)

"""
	Extended class from Button to display info of a move.
"""
class Button_Move(Button):
    def __init__(self, position_name, move):
        """
            Args:
                position_name ('str'): The key to obtain the position.
                move (class:'Move'): The move to be displayed by the button.

            Action:
                Create an extencion of 'Button' to show relevant information
                abount 'move'.
        """
        if move != None:
            name_img = Directory['CELL_NAME'].format(move.type().name())
        else:
            name_img = Directory['NONE_CELL_FILE']
        Button.__init__(self, position_name, name_img, move)
        if move != None:
            a_pp_shift = Select_Config['BUTTON_A_PP_SHIFT']
            self.font_actual_pp = Font(self.location_pre_scale, a_pp_shift)
            m_pp_shift = Select_Config['BUTTON_M_PP_SHIFT']
            self.font_max_pp = Font(self.location_pre_scale, m_pp_shift)
            self.font_max_pp.set_text(num_to_text(move.max_pp()))

    """
        Funcion to display this button.
    """
    def display(self,SCREEN):
        Button.display(self,SCREEN)
        if self.obj != None:
            pct = self.obj.actual_pp()/self.obj.max_pp()
            color = 'BLACK' if pct>0.5 else 'YELLOW' if pct>0.25 else 'RED'
            text_num = num_to_text(self.obj.actual_pp())
            self.font_actual_pp.set_text(text_num, color)
            self.font_actual_pp.display(SCREEN)
            self.font_max_pp.display(SCREEN)

"""
	Extended class from Button to display the name of a pokemon.
"""
class Button_Target(Button):
    def __init__(self, position_name, pokemon):
        """
            Args:
                position_name ('str'): The key to obtain the position.
                pokemon (class:'Pokemon'): The pokemon to be displayed.

            Action:
                Create an extencion of 'Button' to show the name of 'pokemon'.
        """
        name_img = Directory['CELL_NAME'].format('poke')
        Button.__init__(self, position_name, name_img, pokemon)

"""
	Extended class from Button, specialized for the cancel button.
"""
class Button_Cancel(Button):
    def __init__(self):
        """
            Args: -

            Action:
                Create an extencion of 'Button' that not show anything.
                It is the button for the cancel button.
        """
        name_img = Directory['CELL_NAME'].format('poke')
        Button.__init__(self, 'POS_CANCEL', name_img, None)

    """
        Function to avoid showing the button.
    """
    def display(self,SCREEN):
        pass
