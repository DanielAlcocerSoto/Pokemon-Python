#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import load_sprite
from Pokemon_python.display.image import Background, Display, Image
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, center_to_top_left, final_scale
from Pokemon_python.display.display_config import Display_Config
from Pokemon_python.directory_config import Directory
from Pokemon_python.display.battle.battle_config import Battle_Config

import pygame

from random import randint

POS_BAR_F2 = scale_bg(Battle_Config.POS_BAR_F2)
POS_BAR_F1 = scale_bg(Battle_Config.POS_BAR_F1)
POS_BAR_A1 = scale_bg(Battle_Config.POS_BAR_A1)
POS_BAR_A2 = scale_bg(Battle_Config.POS_BAR_A2)

POS_A1 = 0
POS_A2 = 1
POS_F1 = 2
POS_F2 = 3

class Sprite (Image):
	def __init__(self, image_file, POS):
		image = load_sprite(image_file)
		factor_sprite = Display_Config.BACK_SPRITE_SCALE if 'back' in image_file else Display_Config.FRONT_SPRITE_SCALE

		x, y = image.get_size()
		b_x, b_y = pair_mult_num(Display_Config.BATTLE_SIZE, Display_Config.BACKGROUND_SCALE)
		if   POS == POS_A1: pos = (x/2, b_y-y/3)
		elif POS == POS_A2: pos = (3*x/2, b_y-y/3)
		elif POS == POS_F1: pos = (b_x-3*x/2, b_y/2.1)
		elif POS == POS_F2: pos = (b_x-x/2, b_y/2.1)

		top_left_location = center_to_top_left(pos, pair_mult_num(image.get_size(),factor_sprite))
		location = scale(top_left_location)
		final_image = pygame.transform.scale(image, final_scale(image.get_size(),factor_sprite))
		Image.__init__(self,final_image,location)


class Health (Background):
	def __init__(self):
		Background.__init__(self, Directory.HEALTH_FILE)
		self.BAR_LENGTH, self.BAR_HEIGHT = scale_bg(Display_Config.BAR_SIZE)
		self.bar_img_col = [
			(pygame.Rect(POS_BAR_F2[0],POS_BAR_F2[1], self.BAR_LENGTH, self.BAR_HEIGHT),Display_Config.GREEN),
			(pygame.Rect(POS_BAR_F1[0],POS_BAR_F1[1], self.BAR_LENGTH, self.BAR_HEIGHT),Display_Config.GREEN),
			(pygame.Rect(POS_BAR_A1[0],POS_BAR_A1[1], self.BAR_LENGTH, self.BAR_HEIGHT),Display_Config.GREEN),
			(pygame.Rect(POS_BAR_A2[0],POS_BAR_A2[1], self.BAR_LENGTH, self.BAR_HEIGHT),Display_Config.GREEN)]

	def set_health_of(indx, act_health, max_health):
		pct = act_health/max_health
		x, y = POS_BAR_F2
		fill = (pct/100.0 * BAR_LENGTH)
		color = Display_Config.GREEN if pct>0.5 else Display_Config.YELLOW if pct>0.25 else Display_Config.RED
		self.bar_img_col[indx] = (pygame.Rect(x, y, fill, self.BAR_HEIGHT), color)

	def display(self,SCREEN):
		Background.display(self,SCREEN)
		for bar_img, color in self.bar_img_col:
			pygame.draw.rect(SCREEN, color, bar_img)


class Battle_display(Display):
	def __init__(self):
		self.battle_bg = Background(Directory.BACKGROUND_NAME+str(randint(0,11)))
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
