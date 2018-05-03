#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains useful functions to work with images
and do some calculations.

This module contains the following functions to import to another classes:

	scale
	bottom_middle_to_top_left
	shift
	num_to_text
"""

# Local imports
from Configuration.settings import Display_Config

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

# scale + bgscale, b&f sprite scale

def shift(pos, desp):
	return (pos[0]+desp[0],pos[1]+desp[1])

def scale(pair, factor=1):
	fact = Display_Config['SCALE']*factor
	return (int(pair[0]*fact), int(pair[1]*fact))

def bottom_middle_to_top_left(pos, sprite_size):  # only in sprite
	return (pos[0]-sprite_size[0]/2,pos[1]-sprite_size[1])

def num_to_text(num,max_digits=2): # only in button
	s_num= str(num)
	if len(s_num) < max_digits:
		spaces = max_digits-len(s_num)
		for i in range(0,spaces):
			s_num = ' '+s_num
	return s_num
