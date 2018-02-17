#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.sittings import Directory, Display_Config, Select_Config
from Pokemon_python.display.image import Background, Display
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, final_scale
from .button import Button, Button_Target
from .selector import Selector
from Pokemon_python.engine.core.move import Move

import pygame


class Selection_Display(Display):
    def __init__(self,state):
        height = Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1]
        self.selection_move = Selection_Move(height,state[Display_Config["Ally_0"]])
        self.selection_target = Selection_Target(height,state[Display_Config["Foe_0"]],state[Display_Config["Foe_1"]])
        self.selection_none = Selection_None(height)
        self.modes = {
          "MODE_MOVE":self.selection_move,
          "MODE_TARGET":self.selection_target,
          "MODE_OFF":self.selection_none
        }
        Display.__init__(self, [])
        self.change_mode('MODE_MOVE')

    def get_selected(self):
        return self.active_mode.get_move_selected()

    def click_at(self, mouse):
        return self.active_mode.click_at(mouse)

    def in_mode(self,name_mode):
        return self.mode == name_mode

    def change_mode(self,name_mode):
        self.mode=name_mode
        self.active_mode = self.modes[name_mode]
        self.selector = self.active_mode.selector
        self._visualize_items = [self.active_mode]

class Selection_Move(Display):
    def __init__(self,height,pokemon):
        self.pokemon = pokemon
        moves = pokemon.moves_can_use()
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
        for i, button in enumerate(self.buttons):
            if button.point_inside(mouse):
                return i
        return None

class Selection_Target(Display):
    def __init__(self,height,target_0,target_1):
        self.bg = Background(Directory['SELECT_TARGET_FILE'],top_left_location=(0,height))
        self.selector = Selector(False)
        self.target_0 = target_0
        self.target_1 = target_1
        self.buttons = [#TODO all pokemons posible selectable+ cancel button to detect it on click
            Button_Target(Select_Config['POS_MOVE_0'],target_0),
            Button_Target(Select_Config['POS_MOVE_1'],target_1)
        ]

        visualize_items = [self.bg, self.buttons[0], self.buttons[1], self.selector]
        Display.__init__(self, visualize_items)

    def get_move_selected(self):
        return self.selector.get_selection()

    def click_at(self, mouse):
        for i, button in enumerate(self.buttons):
            if button.point_inside(mouse):
                return i
        return None

class Selection_None(Display):
    def __init__(self,height):
        self.bg = Background(Directory['SELECT_EMPTY_FILE'],top_left_location=(0,height))
        visualize_items = [self.bg]
        self.selector = Selector(False)
        Display.__init__(self, visualize_items)

    def get_move_selected(self):
        return None

    def click_at(self, mouse):
        return None
