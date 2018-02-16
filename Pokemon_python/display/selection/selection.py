#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.sittings import Directory, Display_Config, Select_Config
from Pokemon_python.display.image import Background, Display
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, final_scale
from .button import Button
from .selector import Selector
from Pokemon_python.engine.core.move import Move

import pygame


class Selection_Display(Display):
    def __init__(self,pokemon):
        self.pokemon = pokemon
        print(self.pokemon.name())
        moves = pokemon.moves_can_use()
        height = Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1]
        self.bg = Background(Directory['SELECT_MOVE_FILE'],top_left_location=(0,height))
        self.selector = Selector()
        self.buttons = []
        for i in range(0,4):
            self.buttons.append( Button(Select_Config['POS_MOVE_'+str(i)],moves[i] if i<len(moves) else None))

        visualize_items = [self.bg, self.buttons[0], self.buttons[1], self.buttons[2], self.buttons[3], self.selector]
        Display.__init__(self, visualize_items)

    def get_move_selected(self):
        return self.selector.get_selection()

    def click_at(self, mouse):
        self.buttons[0].get_move().use()
        self.pokemon.hurt(10)
        print(self.pokemon.health())
        for i, button in enumerate(self.buttons):
            if button.point_inside(mouse):
                return i
        return None
