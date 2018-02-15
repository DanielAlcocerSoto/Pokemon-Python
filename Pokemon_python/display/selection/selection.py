#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.sittings import Directory, Display_Config, Select_Config
from Pokemon_python.display.image import Background, Display
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, final_scale
from Pokemon_python.display.selection.button import Button
from Pokemon_python.display.selection.selector import Selector

import pygame


class Selection_Display(Display):
    def __init__(self):
        height = Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1]
        self.bg = Background(Directory['SELECT_MOVE_FILE'],top_left_location=(0,height))
        self.bt_0 = Button(Select_Config['POS_MOVE_0'])
        self.bt_1 = Button(Select_Config['POS_MOVE_1'])
        self.bt_2 = Button(Select_Config['POS_MOVE_2'])
        self.bt_3 = Button(Select_Config['POS_MOVE_3'])

        self.selector = Selector()

        self.set_info_moves([None,None,None,None])

        visualize_items = [self.bg, self.bt_0, self.bt_1, self.bt_2, self.bt_3,self.selector]
        Display.__init__(self, visualize_items)

    def set_info_moves(self,moves):
        self.bt_0.set_move(moves[0] if len(moves)>0 else None)
        self.bt_1.set_move(moves[1] if len(moves)>1 else None)
        self.bt_2.set_move(moves[2] if len(moves)>2 else None)
        self.bt_3.set_move(moves[3] if len(moves)>3 else None)
