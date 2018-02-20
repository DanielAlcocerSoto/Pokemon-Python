#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import load_image
from Pokemon_python.sittings import Directory, Display_Config, load_config
from .utils_display import pair_mult_num, scale, scale_bg, center_to_top_left
from .music.song import Song
from .battle.battle import Battle_display
from .dialog.dialog import Dialog_display
from .selection.selection import Selection_Manager
from Pokemon_python.engine.core.move import Move

import pygame, sys
from pygame.locals import *

from time import sleep

class Window:
	def __init__(self,state):
		pygame.init()
		width = Display_Config['BATTLE_SIZE'][0]
		height = Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1]+Display_Config['SELECT_SIZE'][1]
		SCREEN_SIZE = pair_mult_num((width,height), Display_Config['BACKGROUND_SCALE'])
		self.SCREEN = pygame.display.set_mode(scale(SCREEN_SIZE))

		pygame.display.set_icon(load_image(Directory['ICON_FILE']))
		pygame.display.set_caption(Display_Config['TITLE'])

		self.battle = Battle_display(state)
		self.dialog = Dialog_display()
		self.select = Selection_Manager(state)
		self.visualize_items = [self.battle, self.dialog, self.select]
		#Song().play(True)
		self.sentence = load_config('TEXT_FILE')

	def visualize(self):#TODO pause to read
		action = self.manage_events()
		for surface in self.visualize_items:
			surface.display(self.SCREEN)
		pygame.display.update()
		return action

	def set_action_selected(self,obj):
		if obj != None:
			if self.select.in_mode('MODE_MOVE'):
				self.move = obj
				self.select.change_mode('MODE_TARGET')
			elif self.select.in_mode('MODE_TARGET'):
				self.target = obj
				if obj == 4: #cancel button
					self.select.change_mode('MODE_MOVE')
					return None
				elif obj in [0,1]:
					self.select.change_mode('MODE_OFF')
					return (self.move, self.target)
		return None

	def manage_events(self):
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q])):
				print('QUIT GAME')
				pygame.quit()
				sys.exit()

			elif not self.select.in_mode('MODE_OFF'):
				if event.type == MOUSEBUTTONDOWN and event.button == 1:
					mouse = pygame.mouse.get_pos()
					return self.set_action_selected(self.select.click_at(mouse))

				elif event.type == KEYDOWN:
					if event.key in [K_RIGHT, K_d]:
						self.select.selector.move_to_right()
					elif event.key in [K_LEFT, K_a]:
						self.select.selector.move_to_left()
					elif event.key in [K_UP, K_w]:
						self.select.selector.move_to_up()
					elif event.key in [K_DOWN, K_s]:
						self.select.selector.move_to_down()
					elif event.key in [K_RETURN, K_SPACE]:
						return self.set_action_selected(self.select.get_selected())
		return None

	def show(self, name, *args, time=2):
		text = self.sentence[name].format(*args)
		print(text)
		self.dialog.set_text(text)
		self.visualize()
		sleep(time)#click or enter

	def get_action(self):
		self.select.change_mode('MODE_MOVE')
		action = None
		while action == None:
			action = self.visualize()
		return action
