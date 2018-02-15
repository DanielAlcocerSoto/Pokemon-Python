#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import load_image, load_background
from Pokemon_python.display.utils_display import pair_mult_num, scale, final_scale
from Pokemon_python.sittings import Display_Config

import pygame

class Image(pygame.sprite.Sprite):
	def __init__(self, image, top_left_location):
		pygame.sprite.Sprite.__init__(self)
		self._image = image
		self._location = top_left_location

	def display(self,SCREEN):
		SCREEN.blit(self._image, self._location)

class Background(Image):
	def __init__(self, image_file, top_left_location = [0,0]):
		image = load_background(image_file)
		factor = Display_Config['BACKGROUND_SCALE']
		final_image =  pygame.transform.scale(image, final_scale(image.get_size(),factor))
		location =  final_scale(top_left_location, factor)
		Image.__init__(self,final_image,location)

class Display:
	def __init__(self, visualize_items):
		self._visualize_items = visualize_items

	def display(self, SCREEN):
		for surface in self._visualize_items:
			surface.display(SCREEN)
