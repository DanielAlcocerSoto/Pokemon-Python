#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import config, DISPLAY_CONFIG

#GLOBAL DISPLAY CONFIGURATIONS
CONFIG = config(DISPLAY_CONFIG)
SCALE = CONFIG['SCALE']
BACKGROUND_SCALE = CONFIG['BACKGROUND_SCALE']

def pair_mult_num(pair, num):
	return (int(pair[0]*num),int(pair[1]*num))

def scale(pair):
	return pair_mult_num(pair, SCALE)

def scale_bg(pair):
	return pair_mult_num(pair, SCALE*BACKGROUND_SCALE)

def center_to_top_left(pos, sprite_size):
	return (pos[0]-sprite_size[0]/2,pos[1]-sprite_size[1]/2)
