#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import load_sprite
from Pokemon_python.display.image import Background, Display, Image
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, center_to_top_left, final_scale
from Pokemon_python.sittings import Directory, Display_Config, Battle_Config
from .health import Health_Rect_Info

import pygame

from random import randint

class Sprite (Image):
	def __init__(self, pokemon, POS):
		self.pokemon = pokemon
		image_file = pokemon.sprite(POS<2)
		image = load_sprite(image_file)
		factor_sprite = Display_Config['BACK_SPRITE_SCALE'] if 'back' in image_file else Display_Config['FRONT_SPRITE_SCALE']

		x, y = image.get_size()
		b_x, b_y = pair_mult_num(Display_Config['BATTLE_SIZE'], Display_Config['BACKGROUND_SCALE'])
		if   POS == Battle_Config['POS_A1']: pos = (x/2, b_y-y/3)
		elif POS == Battle_Config['POS_A2']: pos = (3*x/2, b_y-y/3)
		elif POS == Battle_Config['POS_F1']: pos = (b_x-3*x/2, b_y/2.1)
		elif POS == Battle_Config['POS_F2']: pos = (b_x-x/2, b_y/2.1)

		top_left_location = center_to_top_left(pos, pair_mult_num(image.get_size(),factor_sprite))
		location = scale(top_left_location)
		final_image = pygame.transform.scale(image, final_scale(image.get_size(),factor_sprite))
		Image.__init__(self,final_image,location)

	def display(self,SCREEN):
		if not self.pokemon.is_fainted(): Image.display(self,SCREEN)

class Battle_display(Display):
	def __init__(self, state):
		battle_bg = Background(Directory['BACKGROUND_NAME'].format(str(randint(0,11))))
		health_bg = Background(Directory['HEALTH_FILE'])

		health_0 = Health_Rect_Info(state[Display_Config['Ally_0']], Battle_Config['POS_A1'])
		health_1 = Health_Rect_Info(state[Display_Config['Ally_1']], Battle_Config['POS_A2'])
		health_2 = Health_Rect_Info(state[Display_Config['Foe_0']], Battle_Config['POS_F1'])
		health_3 = Health_Rect_Info(state[Display_Config['Foe_1']], Battle_Config['POS_F2'])

		pk_a1 = Sprite(state[Display_Config['Ally_0']], Battle_Config['POS_A1'])
		pk_a2 = Sprite(state[Display_Config['Ally_1']], Battle_Config['POS_A2'])
		pk_f1 = Sprite(state[Display_Config['Foe_0']], Battle_Config['POS_F1'])
		pk_f2 = Sprite(state[Display_Config['Foe_1']], Battle_Config['POS_F2'])

		visualize_items = [battle_bg, pk_f1, pk_f2, pk_a1, pk_a2, health_bg, health_0, health_1, health_2, health_3]
		Display.__init__(self, visualize_items)
