#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import load_sprite
from Pokemon_python.display.image import Background, Display, Image
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, center_to_top_left, final_scale
from Pokemon_python.sittings import Directory, Display_Config, Battle_Config
from .health import Health

import pygame

from random import randint

POS_A1 = 0
POS_A2 = 1
POS_F1 = 2
POS_F2 = 3

class Sprite (Image):
	def __init__(self, image_file, POS):
		image = load_sprite(image_file)
		factor_sprite = Display_Config['BACK_SPRITE_SCALE'] if 'back' in image_file else Display_Config['FRONT_SPRITE_SCALE']

		x, y = image.get_size()
		b_x, b_y = pair_mult_num(Display_Config['BATTLE_SIZE'], Display_Config['BACKGROUND_SCALE'])
		if   POS == POS_A1: pos = (x/2, b_y-y/3)
		elif POS == POS_A2: pos = (3*x/2, b_y-y/3)
		elif POS == POS_F1: pos = (b_x-3*x/2, b_y/2.1)
		elif POS == POS_F2: pos = (b_x-x/2, b_y/2.1)

		top_left_location = center_to_top_left(pos, pair_mult_num(image.get_size(),factor_sprite))
		location = scale(top_left_location)
		final_image = pygame.transform.scale(image, final_scale(image.get_size(),factor_sprite))
		Image.__init__(self,final_image,location)


class Battle_display(Display):
	def __init__(self, state):
		self.battle_bg = Background(Directory['BACKGROUND_NAME']+str(randint(0,11)))
		self.health = Health()
		poke1 = '1_bulbasaur'
		poke2 = '3_venusaur'
		#1_bulbasaur
		#3_venusaur
		pk_a1 = Sprite(poke1+'_back', POS_A1)
		pk_a2 = Sprite(poke2+'_back', POS_A2)
		pk_f1 = Sprite(poke1+'_front', POS_F1)
		pk_f2 = Sprite(poke2+'_front', POS_F2)

		visualize_items = [self.battle_bg, pk_f1, pk_f2, pk_a1, pk_a2, self.health]
		Display.__init__(self, visualize_items)
