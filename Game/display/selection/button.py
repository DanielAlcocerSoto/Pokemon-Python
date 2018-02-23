#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

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

"""
class Button:
    def __init__(self, position_name, name_img, obj):
        top_left_location = Select_Config[position_name]
        shift = (0,Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1])
        self.location_pre_scale = transalte(top_left_location,shift)
        self._location = scale_bg(self.location_pre_scale)
        image = load_cell(name_img)
        self._image = pygame.transform.scale(image, scale_bg(image.get_size()))

        self.obj = obj
        self.font_name = Font(self.location_pre_scale, Select_Config['BUTTON_NAME_SHIFT'])
        self.font_name.set_text('' if obj == None else obj.name() )

    def display(self,SCREEN):
        SCREEN.blit(self._image, self._location)
        self.font_name.display(SCREEN)

    def point_inside(self, point):
        left, top = self._location
        width, height = self._image.get_size()
        rect = pygame.Rect(left, top, width, height)
        return rect.collidepoint(point)

    def get_object(self):
        return self.obj


class Button_Move(Button):
    def __init__(self, position_name, move):
        name_img = Directory['CELL_NAME'].format(move.type().name()) if move != None else Directory['NONE_CELL_FILE']
        Button.__init__(self, position_name, name_img, move)
        if move != None:
            self.font_actual_pp = Font(self.location_pre_scale, Select_Config['BUTTON_A_PP_SHIFT'])
            self.font_max_pp = Font(self.location_pre_scale, Select_Config['BUTTON_M_PP_SHIFT'])
            self.font_max_pp.set_text(num_to_text(move.max_pp()))

    def display(self,SCREEN):
        Button.display(self,SCREEN)
        if self.obj != None:
            pct = self.obj.actual_pp()/self.obj.max_pp()
            color = 'BLACK' if pct>0.5 else 'YELLOW' if pct>0.25 else 'RED'
            self.font_actual_pp.set_text(num_to_text(self.obj.actual_pp()),color)
            self.font_actual_pp.display(SCREEN)
            self.font_max_pp.display(SCREEN)

class Button_Target(Button):
    def __init__(self, position_name, pokemon):
        name_img = Directory['CELL_NAME'].format('poke')
        Button.__init__(self, position_name, name_img, pokemon)

class Button_Cancel(Button):
    def __init__(self):
        name_img = Directory['CELL_NAME'].format('poke')
        Button.__init__(self, 'POS_CANCEL', name_img, None)

    def display(self,SCREEN):
        pass
