#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Selector class.
This class allows to create a selector to get a selection from the screen.

It contains the following class:

	Selector
"""

# Local imports
from Configuration.settings import Directory, Display_Config, Select_Config
from DataBase.utils_data_base import load_cell
from Game.display.image import Background
from Game.display.utils_display import scale_bg, transalte

# 3rd party imports
import pygame

__version__ = '0.9'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
    Class to display a selector of butttons and get the index of the buttton
    selected.
"""
class Selector:
	def __init__(self, select_move = True):
		"""
			Args:
				select_move ('bool'): Indicate if select moves or pokemons.

			Action:
				Create a selector able to move between the different buttons and
				obtain the index of the selected button.
		"""
		self._select_move = 1 if select_move else 2
		shift = Display_Config['BATTLE_SIZE'][1]+Display_Config['LOG_SIZE'][1]
		self._shift = (0, shift)
		self.pos = [0,0]
		self._time_init = pygame.time.get_ticks()
		self._set_location()

	"""
	    Class function to set the location of the selector.
	"""
	def _set_location(self):
	    """
	        Args: -

	        Action:
	        	Set the position of this selector in the correct loction
	            depending on 'self.pos'.
	    """
	    name = 'SELECTOR_L_FILE' if self.pos[1] == 2 else 'SELECTOR_FILE'
	    image = load_cell(Directory[name])
	    self._image = pygame.transform.scale(image, scale_bg(image.get_size()))

	    if self.pos[1] < 2:
	        width = Select_Config['POS_MOVE_'+str(self.pos[0])][0]
	        height = Select_Config['POS_MOVE_'+str(self.pos[1]*2)][1]
	    else:
	        width,height = Select_Config['POS_CANCEL']
	    location = transalte((width,height), self._shift)
	    self._location = scale_bg(location)
	    self._time_init = pygame.time.get_ticks()

	"""
	    Moves the selector to the left.
	"""
	def move_to_left(self):
	    old_pos = list(self.pos)
	    self.pos[0] = max(self.pos[0]-1,0)
	    if old_pos != self.pos: self._set_location()

	"""
	    Moves the selector to the right.
	"""
	def move_to_right(self):
	    old_pos = list(self.pos)
	    self.pos[0] = min(self.pos[0]+1,1)
	    if old_pos != self.pos: self._set_location()

	"""
	    Moves the selector up.
	"""
	def move_to_up(self):
	    old_pos = list(self.pos)
	    self.pos[1] = max(self.pos[1]-1,0)
	    if old_pos != self.pos: self._set_location()

	"""
	    Moves the selector down.
	"""
	def move_to_down(self):
	    old_pos = list(self.pos)
	    self.pos[1] = min(self.pos[1]+1,self._select_move)
	    if old_pos != self.pos: self._set_location()

	"""
	    Get the index of the botton currently selected.
	"""
	def get_selection(self):
	    return min(self.pos[1]*2+self.pos[0],4)

	"""
	    Funcion to display this object.
	"""
	def display(self,SCREEN):
	    stripe = (1000*Select_Config["SELECTOR_DISPLAY_STRIPE"])
	    delta_time = (pygame.time.get_ticks() - self._time_init)/stripe
	    if delta_time-int(delta_time)<Select_Config["SELECTOR_DISPLAY_TIME"]:
	        SCREEN.blit(self._image, self._location)
