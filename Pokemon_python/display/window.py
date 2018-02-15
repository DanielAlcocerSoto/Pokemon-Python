#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import load_image
from Pokemon_python.display.utils_display import pair_mult_num, scale, scale_bg, center_to_top_left
from Pokemon_python.sittings import Directory, Display_Config
from Pokemon_python.display.music.song import Song
from Pokemon_python.display.battle.battle import Battle_display
from Pokemon_python.display.dialog.dialog import Dialog_display
from Pokemon_python.display.selection.selection import Selection_Display

import pygame, sys
from pygame.locals import *

class Window:
	def __init__(self):
		pygame.init()
		width = Display_Config['BATTLE_SIZE'][0]
		height = Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1]+Display_Config['SELECT_SIZE'][1]
		SCREEN_SIZE = pair_mult_num((width,height), Display_Config['BACKGROUND_SCALE'])
		self.SCREEN = pygame.display.set_mode(scale(SCREEN_SIZE))

		pygame.display.set_icon(load_image(Directory['ICON_FILE']))
		pygame.display.set_caption(Display_Config['TITLE'])

		self.battle = Battle_display()
		self.dialog = Dialog_display()
		self.select = Selection_Display()

		self.visualize_items = [self.battle, self.dialog, self.select]
		#Song().play(True)

	def visualize(self):
		self.manage_events()
		for surface in self.visualize_items:
			surface.display(self.SCREEN)
		pygame.display.update()

	def manage_events(self):
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
				if event.key == K_RIGHT or event.key == K_d:
					self.select.selector.move_to_right()
				elif event.key == K_LEFT or event.key == K_a:
					self.select.selector.move_to_left()
				elif event.key == K_UP or event.key == K_w:
					self.select.selector.move_to_up()
				elif event.key == K_DOWN or event.key == K_s:
					self.select.selector.move_to_down()
				elif event.key == K_RETURN or event.key == K_SPACE:
					print(self.select.selector.get_selection())

	def set_text_log(self, text):
		self.dialog.set_text(text)
