#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import load_sprite
from Pokemon_python.display.image import Background, Display, Image
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, center_to_top_left, final_scale
from Pokemon_python.sittings import Directory, Display_Config, Battle_Config

import pygame


POS_BAR_F2 = scale_bg(Battle_Config['POS_BAR_F2'])
POS_BAR_F1 = scale_bg(Battle_Config['POS_BAR_F1'])
POS_BAR_A1 = scale_bg(Battle_Config['POS_BAR_A1'])
POS_BAR_A2 = scale_bg(Battle_Config['POS_BAR_A2'])

class Health (Background):
	def __init__(self):
		Background.__init__(self, Directory['HEALTH_FILE'])
		self.BAR_LENGTH, self.BAR_HEIGHT = scale_bg(Display_Config['BAR_SIZE'])
		self.bar_img_col = [
			(pygame.Rect(POS_BAR_F2[0],POS_BAR_F2[1], self.BAR_LENGTH, self.BAR_HEIGHT),Display_Config['GREEN']),
			(pygame.Rect(POS_BAR_F1[0],POS_BAR_F1[1], self.BAR_LENGTH, self.BAR_HEIGHT),Display_Config['GREEN']),
			(pygame.Rect(POS_BAR_A1[0],POS_BAR_A1[1], self.BAR_LENGTH, self.BAR_HEIGHT),Display_Config['GREEN']),
			(pygame.Rect(POS_BAR_A2[0],POS_BAR_A2[1], self.BAR_LENGTH, self.BAR_HEIGHT),Display_Config['GREEN'])]

	def set_health_of(idx, act_health, max_health):
		pct = act_health/max_health
		x, y = POS_BAR_F2
		fill = (pct/100.0 * BAR_LENGTH)
		color = 'GREEN' if pct>0.5 else 'YELLOW' if pct>0.25 else 'RED'
		self.bar_img_col[idx] = (pygame.Rect(x, y, fill, self.BAR_HEIGHT),Display_Config[color])

	def display(self,SCREEN):
		Background.display(self,SCREEN)
		for bar_img, color in self.bar_img_col:
			pygame.draw.rect(SCREEN, color, bar_img)
