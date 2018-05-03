#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains some generic classes, useful for the implementation of
classes related to the visualization of elements on the screen.

It contains the following classes:

	Image
	Sprite
	Display
"""

# Local imports
from Configuration.settings import Directory, Display_Config, Battle_Config
from DataBase.utils_data_base import load_image
from .utils_display import scale, bottom_middle_to_top_left

# 3rd party imports
import pygame

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Class to display an image.
"""
class Image:
	def __init__(self, image_file, top_left_location = [0,0]):
		"""
			Args:
				image (class:'pygame.Surface'): The image to display in the
												screen.
				top_left_location (set:'int','int'): The top left location of
													 the 'image' in the screen.

			Action:
				Create a image that will be displayed in a screen in the
				'top_left_location' position.
		"""
		image = load_image(image_file)
		self._image = pygame.transform.scale(image, scale(image.get_size()))
		self._location = scale(top_left_location)

	"""
		Funcion to display this image.
	"""
	def display(self, SCREEN):
		"""
			Args:
				SCREEN (class:'pygame.Surface'): The current screen of the
												 window where to display the
												 image.

			Action:
				Display the image in SCREEN.
		"""
		SCREEN.blit(self._image, self._location)


"""
	Class to display the sprite of a pokemon.
"""
class Sprite:
	def __init__(self, pokemon, POS):
		"""
		    Args:
		        pokemon (class:'Pokemon'): The pokemon to be displayed.
		        POS ('str'): The key to obtain the position where display the
							 pokemon.

		    Action:
		        Create an object to show the sprite of 'pokemon' in the position
			    indicated by the 'POS' key.
		"""
		self.pokemon = pokemon
		image_file = Directory['DIR_SPRITES'] + pokemon.sprite(POS<2)
		image = load_image(image_file)

		if POS<2 :
			is_ally = 'A'
			factor_sprite = Display_Config['BACK_SPRITE_SCALE']
		else:
			is_ally = 'F'
			factor_sprite = Display_Config['FRONT_SPRITE_SCALE']

		name_format = Battle_Config['POS_POKE_FORMAT']
		location = Battle_Config[name_format.format(is_ally,POS%2+1)]

		final_size = scale(image.get_size(), factor_sprite)
		self._image = pygame.transform.scale(image, final_size)
		self._location = bottom_middle_to_top_left(scale(location), final_size)

	"""
        Funcion to display this sprite.
    """
	def display(self,SCREEN):
		if not self.pokemon.is_fainted():
			SCREEN.blit(self._image, self._location)


"""
	Generic class to display several displayables objects.
"""
class Display:
	def __init__(self, visualize_items):
		"""
			Args:
				visualize_items ('list of obj'): A list of object with a
												 'display' function (p.e. Image).

			Action:
				Create a object with several displayable items.
		"""
		self._visualize_items = visualize_items

	"""
		Funcion to display this several items.
	"""
	def display(self, SCREEN):
		"""
		Args:
			SCREEN (class:'pygame.Surface'): The current screen of the window
											 where to display the image.

		Action:
			Display several items in SCREEN.
		"""
		for surface in self._visualize_items:
			surface.display(SCREEN)
