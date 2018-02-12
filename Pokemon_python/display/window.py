#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import load_image
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, center_to_top_left
from Pokemon_python.display.battle.battle import Battle_display
from Pokemon_python.display.dialog.dialog import Dialog_display
from Pokemon_python.display.music.song import Song
from Pokemon_python.display.display_config import Display_Config
#from Pokemon_python.diplay.buttons import buttons

import pygame, sys
from pygame.locals import *


ICON_NAME = 'icon'
TITLE = 'POKEMON DOUBLE BATTLE'

class Window:
	def __init__(self):
		pygame.init()
		SCREEN_SIZE = pair_mult_num((Display_Config.BATTLE_SIZE[0],Display_Config.BATTLE_SIZE[1]+Display_Config.LOG_SIZE[1]), Display_Config.BACKGROUND_SCALE)
		self.SCREEN = pygame.display.set_mode(scale(SCREEN_SIZE))

		pygame.display.set_icon(load_image(ICON_NAME))
		pygame.display.set_caption(TITLE)

		self.battle = Battle_display()
		self.dialog = Dialog_display()

		self.visualize_items = [self.battle, self.dialog]
		Song().play(True)

	def set_text_log(self, text):
		self.dialog.set_text(text)

	def visualize(self):
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
				print('QUIT GAME')
				pygame.quit()
				sys.exit()

			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				mouse = pygame.mouse.get_pos()
				print(mouse)
				#if Image[1].collidrect(mouse):

			elif event.type == KEYDOWN:
				#if the right arrow is pressed
				if event.key == K_RIGHT or event.key == K_d:
					print('right')
				elif event.key == K_LEFT or event.key == K_a:
					print('left')
				elif event.key == K_UP or event.key == K_w:
					print('up')
				elif event.key == K_DOWN or event.key == K_s:
					print('down')


		for surface in self.visualize_items:
			surface.display(self.SCREEN)

		pygame.display.update()
