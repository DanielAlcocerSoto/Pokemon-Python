#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.sittings import Directory, Display_Config, Select_Config
from Pokemon_python.utils_data_base import load_cell
from Pokemon_python.display.image import Background
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, transalte

from Pokemon_python.engine.core.move import Move


import pygame

class Button():
    def __init__(self, top_left_location, move):
        self.move=move
        shift = (0,Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1])
        location = transalte(top_left_location,shift)
        self._location = scale_bg(location)
        self.set_move(move)

    def set_move(self,move):#TODO +type move
        name = Directory['CELL_NAME']+move.type() if move != None else Directory['NONE_CELL_FILE']
        image = load_cell('cell_poke')
        self._image =  pygame.transform.scale(image, scale_bg(image.get_size()))

    def get_move(self):
        return self.move

    def point_inside(self, point):
        left, top = self._location
        width, height = self._image.get_size()
        rect = pygame.Rect(left, top, width, height)
        return rect.collidepoint(point)

    def display(self,SCREEN):
        SCREEN.blit(self._image, self._location)
