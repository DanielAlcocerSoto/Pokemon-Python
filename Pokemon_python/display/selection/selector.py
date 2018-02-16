#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.sittings import Directory, Display_Config, Select_Config
from Pokemon_python.utils_data_base import load_cell
from Pokemon_python.display.image import Background
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, transalte


import pygame

class Selector:
    def __init__(self, select_move = True):
        self._select_move = 1 if select_move else 2
        self._shift = (0,Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1])
        self.pos = [0,0]
        self.set_location()

    def set_location(self):
        name = 'SELECTOR_L_FILE' if self.pos[0] == 2 else 'SELECTOR_FILE'
        image = load_cell(Directory[name])
        self._image = pygame.transform.scale(image, scale_bg(image.get_size()))

        if self.pos[0] < 2:
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
        x = pygame.time.get_ticks()/1000
        if x-int(x)<0.7:
            SCREEN.blit(self._image, self._location)
