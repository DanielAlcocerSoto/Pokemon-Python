#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import load_sprite
from Pokemon_python.display.image import Background, Display, Image
from Pokemon_python.display.utils_display import num_to_text, scale_bg
from Pokemon_python.sittings import Directory, Display_Config, Battle_Config
from Pokemon_python.display.font.font import Font

import pygame

POS_A1 = 0
POS_A2 = 1
POS_F1 = 2
POS_F2 = 3

class Health_Rect_Info:
	def __init__(self, pokemon, POS):
		self.poke = pokemon
		self.BAR_LENGTH, self.BAR_HEIGHT = scale_bg(Display_Config['BAR_SIZE'])
		ally = 'A' if POS<2 else 'F'
		location = Battle_Config[Battle_Config['POS_BAR_FORMAT'].format(ally,POS%2+1)]
		self.POS_BAR = scale_bg(location)

		self.font_name = Font(location,Battle_Config['HEALTH_NAME_SHIFT'])
		self.font_name.set_text(pokemon.name(),'WHITE')

		self.font_level = Font(location,Battle_Config['HEALTH_LVL_SHIFT'])
		self.font_level.set_text(str(pokemon.level()),'WHITE')

	def display(self,SCREEN):
		self.font_level.display(SCREEN)
		self.font_name.display(SCREEN)
		self.poke.is_fainted()
		if not self.poke.is_fainted():
			pct = self.poke.health()/self.poke.get_stat('hp')
			fill = (pct * self.BAR_LENGTH)
			bar_img = pygame.Rect(self.POS_BAR[0],self.POS_BAR[1], fill, self.BAR_HEIGHT)
			color_name = 'GREEN' if pct>0.5 else 'YELLOW' if pct>0.25 else 'RED'
			pygame.draw.rect(SCREEN, Display_Config[color_name], bar_img)
