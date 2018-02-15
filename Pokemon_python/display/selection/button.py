#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.sittings import Directory, Display_Config, Select_Config
from Pokemon_python.display.image import Background
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, transalte
from Pokemon_python.utils_data_base import load_cell


import pygame

class Button():
    def __init__(self, top_left_location):
        shift = (0,Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1])
        location = transalte(top_left_location,shift)
        self._location = scale_bg(location)

    def set_move(self,move):#TODO +type move
        name = Directory['CELL_NAME'] if move != None else Directory['NONE_CELL_FILE']
        image = load_cell('cell_poke')
        self._image =  pygame.transform.scale(image, scale_bg(image.get_size()))

    def display(self,SCREEN):
        SCREEN.blit(self._image, self._location)
