#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the some generic classes, useful for the implementation of
classes related to the visualization of elements on the screen.

It contains the following classes:

	Image
	Background
	Display
"""

# Local imports
from Game.settings import Display_Config
from Game.utils_data_base import load_image, load_background
from .utils_display import pair_mult_num, scale, scale_bg

# 3rd party imports
import pygame

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Generic class to display a image.
"""
class Image:
	def __init__(self, image, top_left_location):
		"""
		Args:
			image (class:'pygame.Surface'): The image to display in the screen.
			top_left_location (set:'int','int'): The top left location of the
												 'image' in the screen.

		Action:
			Create a image that will be displayed in a screen in the
			'top_left_location' position.
		"""
		self._image = image
		self._location = top_left_location

	"""
		Funcion to display this image.
	"""
	def display(self, SCREEN):
		"""
		Args:
			SCREEN (class:'pygame.Surface'): The current screen of the window
											 where to display the image.

		Action:
			Display the image in SCREEN.
		"""
		SCREEN.blit(self._image, self._location)

"""
	Class to display a Background image.
"""
class Background(Image):
	def __init__(self, image_file, top_left_location = [0,0]):
		"""
		Args:
			image (class:'pygame.Surface'): The image to display in the screen.
			top_left_location (set:'int','int'): The top left location of the
												 'image' in the screen.

		Action:
			Create a image that will be displayed in a screen in the
			'top_left_location' position.
		"""
		image = load_background(image_file)
		factor = Display_Config['BACKGROUND_SCALE']
		final_image =  pygame.transform.scale(image, scale_bg(image.get_size()))
		location = scale_bg(top_left_location)
		Image.__init__(self,final_image,location)

"""
	Generic class to display several displayables objects.
"""
class Display:
	def __init__(self, visualize_items):
		"""
		Args:
			visualize_items ('list of obj'): A list of object with a 'display'
											 function (p.e. Image).

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
