#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.sittings import Directory, Display_Config, Select_Config
from Pokemon_python.utils_data_base import load_cell
from Pokemon_python.display.image import Background
from Pokemon_python.display.utils_display import scale_bg, transalte, num_to_text
from Pokemon_python.display.font.font import Font

from Pokemon_python.engine.core.move import Move


import pygame

class Button():
    def __init__(self, top_left_location, move):
        shift = (0,Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1])
        location = transalte(top_left_location,shift)
        self._location = scale_bg(location)

        self.move=move
        name = Directory['CELL_NAME']+move.type().name() if move != None else Directory['NONE_CELL_FILE']
        image = load_cell(name)
        self._image = pygame.transform.scale(image, scale_bg(image.get_size()))

        self.font_name = Font(location,Select_Config['BUTTON_NAME_SHIFT'])
        self.font_name.set_text(move.name())

        self.font_max_pp = Font(location,Select_Config['BUTTON_M_PP_SHIFT'])
        self.font_max_pp.set_text(num_to_text(move.max_pp(), max_digits=2))

        self.font_actual_pp = Font(location,Select_Config['BUTTON_A_PP_SHIFT'])

    def get_move(self):
        return self.move

    def point_inside(self, point):
        left, top = self._location
        width, height = self._image.get_size()
        rect = pygame.Rect(left, top, width, height)
        return rect.collidepoint(point)

    def display(self,SCREEN):
        SCREEN.blit(self._image, self._location)
        self.font_name.display(SCREEN)
        self.font_max_pp.display(SCREEN)

        pct = self.move.actual_pp()/self.move.max_pp()
        color = 'BLACK' if pct>0.5 else 'YELLOW' if pct>0.25 else 'RED'
        self.font_actual_pp.set_text(num_to_text(self.move.actual_pp(), max_digits=2),color)
        self.font_actual_pp.display(SCREEN)
