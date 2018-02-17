#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.sittings import Directory, Display_Config, Select_Config
from Pokemon_python.display.image import Background, Display
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, final_scale
from .button import Button_Move, Button_Target, Button_Cancel
from .selector import Selector
from Pokemon_python.engine.core.move import Move

import pygame


class Selection_Manager:
    def __init__(self,state):
        self.selection_move = Selection_Move(state[Display_Config["Ally_0"]])
        self.selection_target = Selection_Target(state[Display_Config["Foe_0"]],state[Display_Config["Foe_1"]])
        self.selection_none = Selection_None()
        self.modes = {
          "MODE_MOVE":  self.selection_move,
          "MODE_TARGET":self.selection_target,
          "MODE_OFF":   self.selection_none
        }
        self.change_mode('MODE_MOVE')

    def get_selected(self):
        return self.active_mode.get_idx_selected()

    def click_at(self, mouse):
        return self.active_mode.click_at(mouse)

    def in_mode(self,name_mode):
        return self.mode == name_mode

    def change_mode(self,name_mode):
        self.mode = name_mode
        self.active_mode = self.modes[name_mode]
        self.selector = self.active_mode.selector
        self._visualize_items = [self.active_mode]

    def display(self,SCREEN):
        self.active_mode.display(SCREEN)

class Selection_Display(Display):
    def __init__(self, background_name, buttons):
        height = Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1]
        bg = Background(Directory[background_name],top_left_location=(0,height))
        self.selector = Selector(select_move= not 'TARGET' in background_name, display_selector= not 'EMPTY' in background_name)
        self.buttons = buttons
        visualize_items = [bg]
        for button in self.buttons: visualize_items.append(button)
        visualize_items.append(self.selector)
        Display.__init__(self, visualize_items)

    def get_idx_selected(self):
        return self.selector.get_selection()

    def click_at(self, mouse):
        for i, button in enumerate(self.buttons):
            if button.point_inside(mouse): return i
        return None

class Selection_Move(Selection_Display):
    def __init__(self, pokemon):
        moves = pokemon.moves_can_use()
        buttons = [Button_Move('POS_MOVE_'+str(i), moves[i] if i<len(moves) else None) for i in range(0,4)]
        Selection_Display.__init__(self,'SELECT_MOVE_FILE', buttons)

class Selection_Target(Selection_Display):
    def __init__(self, target_0, target_1):
        buttons = [#TODO all pokemons posible selectable interest for IA
            Button_Target('POS_MOVE_0', target_0),
            Button_Target('POS_MOVE_1', target_1),
            Button_Target('POS_MOVE_2', None),
            Button_Target('POS_MOVE_3', None),
            Button_Cancel()]
        Selection_Display.__init__(self,'SELECT_TARGET_FILE', buttons)

class Selection_None(Selection_Display):
    def __init__(self):
        Selection_Display.__init__(self,'SELECT_EMPTY_FILE', [])

    def get_move_selected(self):
        return None

    def click_at(self, mouse):
        return None
