#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

# Local imports
from Game.settings import Directory, Display_Config, Select_Config
from Game.utils_data_base import load_cell
from Game.display.image import Background
from Game.display.utils_display import pair_mult_num, scale, scale_bg, transalte

# 3rd party imports
import pygame

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""

"""
class Selector:
    def __init__(self, select_move = True, display_selector = True):
        self._select_move = 1 if select_move else 2
        self.display_selector = display_selector
        self._shift = (0,Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1])
        self.pos = [0,0]
        self.set_location()

    def set_location(self):
        name = 'SELECTOR_L_FILE' if self.pos[1] == 2 else 'SELECTOR_FILE'
        image = load_cell(Directory[name])
        self._image = pygame.transform.scale(image, scale_bg(image.get_size()))

        if self.pos[1] < 2:
            width = Select_Config['POS_MOVE_'+str(self.pos[0])][0]
            height = Select_Config['POS_MOVE_'+str(self.pos[1]*2)][1]
        else:
            width,height = Select_Config['POS_CANCEL']
        location = transalte((width,height), self._shift)
        self._location = scale_bg(location)

    def move_to_left(self):
        self.pos[0]=max(self.pos[0]-1,0)
        self.set_location()

    def move_to_right(self):
        self.pos[0]=min(self.pos[0]+1,1)
        self.set_location()

    def move_to_up(self):
        self.pos[1]=max(self.pos[1]-1,0)
        self.set_location()

    def move_to_down(self):
        self.pos[1]=min(self.pos[1]+1,self._select_move)
        self.set_location()

    def get_selection(self):
        return min(self.pos[1]*2+self.pos[0],4)

    def display(self,SCREEN):
        if self.display_selector:
            x = pygame.time.get_ticks()/1000
            if x-int(x)<0.7:
                SCREEN.blit(self._image, self._location)
