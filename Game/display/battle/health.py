#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Health_Rect_Info class.
This class display the name, the level and the health bar of a pokemon

It contains the following class:

	Health_Rect_Info
"""

# Local imports
from Configuration.settings import Display_Config, Battle_Config
from Game.display.utils_display import scale
from Game.display.image import Image
from Game.display.font import Font

# 3rd party imports
import pygame

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Class to display a info of a pokemon in the battle section.
"""
class Health_Rect_Info:
	def __init__(self, pokemon, POS, path_image):
		"""
		    Args:
		        pokemon (class:'Pokemon'): The pokemon which information will be 
										   displayed.
		        POS ('str'): The key to obtain the position where display the
							 pokemon info.

		    Action:
		        Display the info of the 'pokemon' in the 'POS' location.
		"""
		self.bg = Image(path_image)
		self.poke = pokemon
		self.BAR_LENGTH, self.BAR_HEIGHT = scale(Battle_Config['BAR_SIZE'])
		is_ally = 'A' if POS<2 else 'F'
		name_format = Battle_Config['POS_BAR_FORMAT']
		location = Battle_Config[name_format.format(is_ally,POS%2+1)]
		self.POS_BAR = scale(location)

		self.font_name = Font(location,Battle_Config['HEALTH_NAME_SHIFT'])
		self.font_name.set_text(pokemon.name(),'WHITE')

		self.font_level = Font(location,Battle_Config['HEALTH_LVL_SHIFT'])
		self.font_level.set_text(str(pokemon.level()),'WHITE')

	"""
        Funcion to display info of a pokemon.
    """
	def display(self,SCREEN):
		if not self.poke.is_fainted():
			self.bg.display(SCREEN)
			self.font_level.display(SCREEN)
			self.font_name.display(SCREEN)

			pct = self.poke.health()/self.poke.get_stat('hp')
			fill = (pct * self.BAR_LENGTH)
			x, y = self.POS_BAR
			bar_img = pygame.Rect(x, y, fill, self.BAR_HEIGHT)
			color_name = 'GREEN' if pct>0.5 else 'YELLOW' if pct>0.25 else 'RED'
			pygame.draw.rect(SCREEN, Display_Config[color_name], bar_img)
