#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import load_sprite
from Pokemon_python.display.image import Image, Background, Display
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, center_to_top_left
from Pokemon_python.display.display_config import Display_Config

import pygame, sys

from random import randint

_x, _y = Display_Config.SPRITE_SIZE
_b_x, _b_y = pair_mult_num(Display_Config.BATTLE_SIZE, Display_Config.BACKGROUND_SCALE)
POS_A1 = (_x/2, _b_y-_y/3)			#(48 ,184) for BG_SCALE = 1.5
POS_A2 = (3*_x/2, _b_y-_y/3)		#(144,184)
POS_F1 = (_b_x-3*_x/2, _b_y/2.1)	#(240,108)
POS_F2 = (_b_x-_x/2, _b_y/2.1)		#(336,108)

POS_BAR_F2 = scale_bg((57,22))
POS_BAR_F1 = scale_bg((50,51))
POS_BAR_A1 = scale_bg((189,107))
POS_BAR_A2 = scale_bg((196,136))


BACKGROUND_NAME = 'background_'
HEALTH_NAME = 'health'


class Sprite (Image):
	def __init__(self, image_file, center):
		image = load_sprite(image_file)
		factor = Display_Config.BACK_SPRITE_SCALE if 'back' in image_file else Display_Config.FRONT_SPRITE_SCALE
		tl_location = center_to_top_left(center, pair_mult_num(Display_Config.SPRITE_SIZE, factor))
		Image.__init__(self, image, factor, tl_location)

class Health (Background):
	def __init__(self):
		Background.__init__(self, HEALTH_NAME)
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
        self.battle_bg = Background(BACKGROUND_NAME+str(randint(0,11)))
        self.health = Health()
        poke1 = '1_bulbasaur'
        poke2 = '3_venusaur'
        #1_bulbasaur
        #3_venusaur
        pk_a1 = Sprite(poke1+'_back',  POS_A1)
        pk_a2 = Sprite(poke2+'_back',  POS_A2)
        pk_f1 = Sprite(poke1+'_front', POS_F1)
        pk_f2 = Sprite(poke2+'_front', POS_F2)

        visualize_items = [self.battle_bg, pk_f1, pk_f2, pk_a1, pk_a2, self.health]
        Display.__init__(self, visualize_items)
