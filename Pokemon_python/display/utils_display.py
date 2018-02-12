#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.display.display_config import Display_Config

def pair_mult_num(pair, num):
	return (int(pair[0]*num),int(pair[1]*num))

def scale(pair):
	return pair_mult_num(pair, Display_Config.SCALE)

def scale_bg(pair):
	return pair_mult_num(pair, Display_Config.SCALE*Display_Config.BACKGROUND_SCALE)

def center_to_top_left(pos, sprite_size):
	return (pos[0]-sprite_size[0]/2,pos[1]-sprite_size[1]/2)
