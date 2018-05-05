#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Window class.
This class is the principal class to execute the graphic interface of the game.

It contains the following class:

	Window
"""

# Local imports
from Configuration.settings import Directory, Display_Config
from DataBase.utils_data_base import load_image
from .utils_display import scale
from .music import Song
from .dialog_view import Dialog_display
from .battle_view import Battle_display
from .selection_view.selection import Selection_Manager
from .display_RL_info.moves_display import Moves_display
from .display_RL_info.stats_display import Stats_display

# 3rd party imports
import pygame, sys
from pygame import display, time
from pygame.locals import *

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Class to display a battle.
"""
class Window:
	def __init__(self,state):
		"""
			Args:
				state ('dict of class:Pokemon'): A dictionary with all the
												 information needed to display
												 the a battle.
					Note: This dict have as key: "Ally_0", "Ally_1", "Foe_0"
						  and "Foe_1" with the corresponding pokemon as a value.

			Action:
				Create and execute a window where the 'state' of a  battle
				is displayed.
		"""
		pygame.init()
		width, height = Display_Config['BATTLE_SIZE']
		height += Display_Config['LOG_SIZE'][1]
		height += Display_Config['SELECT_SIZE'][1]
		if state['use_agent'] and Display_Config['VISUALIZE_AGENT_INFO']: width*=2
		SCREEN_SIZE = (width,height)
		self.SCREEN = display.set_mode(scale(SCREEN_SIZE))

		display.set_icon(load_image(Directory['ICON_FILE']))
		display.set_caption(Display_Config['TITLE'])

		self.battle = Battle_display(state)
		self.dialog = Dialog_display()
		self.select = Selection_Manager(state)
		self.visualize_items = [self.battle, self.dialog, self.select]

		if Display_Config["PLAY_MUSIC"]: Song().play()

		if state['use_agent'] and Display_Config['VISUALIZE_AGENT_INFO']:
			self.visualize_items.append(Stats_display(state))
			self.visualize_items.append(Moves_display(state))

	"""
		Function to exit the program depending on the event of the window.
	"""
	def manage_event_quit(self, event):
		"""
			Args:
				event ('class:Event'): A event form pygame.

			Action:
				Quit of pygame and the game if the event detected by pygame
				is the enter or the space key, or if the button exit is pressed.
		"""
		if event.type == QUIT or (event.type == KEYDOWN and
								 (event.key in [K_ESCAPE, K_q])):
			print('QUIT GAME')
			pygame.quit()
			sys.exit()

	"""
		Function to refresh the window.
	"""
	def visualize(self, manage_event=True):
		"""
			Args:
				manage_event ('bool'): Indicates if it is necessary to check
									   the exit event.

			Action:
				Display the current state of the battle, refreshing the
				screen, calling the 'display' functions of the objects that
				form this window. In the case that 'manage_event' is true,
				the exit event will also be checked.
		"""
		if manage_event:
			for event in pygame.event.get():
				self.manage_event_quit(event)
		for surface in self.visualize_items:
			surface.display(self.SCREEN)
		display.update()

	"""
		Function to display a message in the dialog section.
	"""
	def show(self, text, time_display):
		"""
			Args:
				name ('Str'): The name of the sentence pattern.
				args ('list od str'): The params to do a format to the sentence.
				time_display ('int'): Time (in seconds) the message will be displayed.

			Action:
				Display a the sentence pattern 'name', foramted with 'args' and
				wait 'time_display' seconds. The message also disappear if the
				enter or space key is pressed.
		"""
		self.dialog.set_text(text)
		self.visualize(manage_event=False)
		time_init = time.get_ticks()
		delta_time = 0
		click_enter = False
		# Wait 'time' sec or click/enter event
		while delta_time < time_display and not click_enter:
			for event in pygame.event.get():
				self.manage_event_quit(event)
				if (event.type == MOUSEBUTTONDOWN and event.button == 1) or \
				(event.type == KEYDOWN and event.key in [K_RETURN, K_SPACE]):
					click_enter = True
			delta_time = (time.get_ticks() - time_init)/1000

	"""
		Function to get the index of the selected item in the selection section.
	"""
	def get_selection_from_display(self):
		"""
			Args: -

			Return ('int'):
				The index of the button if any button is selected, either
				by keyboard or mouse. If there is nothing selected at the time
				of calling this function, it will return null.
				It also manages the movement of the selector by keyboard and
				mmanage the quit event.
		"""
		for event in pygame.event.get():
			self.manage_event_quit(event)
			if not self.select.in_mode('MODE_OFF'):
				if event.type == MOUSEBUTTONDOWN and event.button == 1:
					mouse = pygame.mouse.get_pos()
					return self.select.click_at(mouse)

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
						return self.select.get_selected()
		return None

	"""
		Function to get a action the action selected by the user.
	"""
	def get_action(self):
		"""
			Args: -

			Return ('int','int'):
				The move index and the target index of the action decided by
				the user.
				Note: If the user has not yet decided the action, it wait until
				the user select an action.
		"""
		change_mode = self.select.change_mode
		in_mode = self.select.in_mode

		change_mode('MODE_MOVE')
		move = target = None
		while target == None:
			self.visualize(manage_event=False)
			idx = self.get_selection_from_display()

			if idx != None:
				if in_mode('MODE_MOVE'):
					move = idx
					change_mode('MODE_TARGET')
				elif in_mode('MODE_TARGET'):
					if idx == 4: change_mode('MODE_MOVE') #cancel button
					elif idx in [0,1]:
						target = idx
						change_mode('MODE_OFF')

		return (move, target)
