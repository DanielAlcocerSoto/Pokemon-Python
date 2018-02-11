#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import load_image, load_background
from Pokemon_python.display.utils_display import pair_mult_num, scale, BACKGROUND_SCALE

import pygame, sys

class Image(pygame.sprite.Sprite):
	def __init__(self, image, factor, tl_location):
		pygame.sprite.Sprite.__init__(self)
		self._image = pygame.transform.scale(image, scale(pair_mult_num(image.get_size(),factor)))
		self._location = scale(tl_location)

	def display(self, SCREEN):
		SCREEN.blit(self._image, self._location)

class Background (Image):
	def __init__(self, image_file, top_left_location = (0,0)):
		image = load_background(image_file)
		tl_location = pair_mult_num(top_left_location, BACKGROUND_SCALE)
		Image.__init__(self, image, BACKGROUND_SCALE, tl_location)

class Display:
    def __init__(self, font, visualize_items):
        self.font = font
        self.visualize_items = visualize_items

    def display(self, SCREEN):
        for surface in self.visualize_items:
            surface.display(SCREEN)
