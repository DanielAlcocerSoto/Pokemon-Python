#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains useful functions to work with the database.

This module contains the following functions to import to another classes:

	load_info
	save_info
	download_sprite
	load_image
	load_sprite
	load_cell
	load_background

And the generic class useful for create other classes
who need to save information from the database:

	Object_Info
"""

# Local imports
from Configuration.settings import Directory

# 3rd party imports
from pygame.image import load

# General imports
import json
import shutil
import requests
import os.path

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Function to load a dictionary from the info directory.
"""
def load_info(name_file):
	"""
		Args:
			name_file ('str'): The name of the info file.

		Return ('dict'):
			The dictionary founded in the info directory with the name 'name_file'.
	"""
	with open(Directory['DIR_INFO']+name_file+'.json', 'r') as json_file:
		obj = json.load(json_file)
	return obj


"""
	Function to save a dictionary in a file in the info directory.
"""
def save_info(name_file, obj):
	"""
		Args:
			name_file ('str'): The name of the new info file.
			obj ('dict'): The dictionary with the info that is wanted to save.

		Action:
			Create a new info file (.json) with the dictionary 'obj'
			and save it	in the info directory with the name 'name_file'.
	"""
	with open(Directory['DIR_INFO']+name_file+'.json', 'w') as json_file:
		json.dump(obj, json_file, indent=4)


"""
	Function to download a sprite and save it.
"""
def download_sprite(url, name_file):
	"""
		Args:
			url ('str'): The url where the raw data of the sprite is.
			name_file ('str'): The name of the new image file.

		Action:
			Create a new image with the raw data in 'url' and save it in
			the sprites directory with the name 'name_file'.
	"""

	path = Directory['DIR_SPRITES']+name_file+'.png'
	if not os.path.exists(path): # Not download it if it already exists
		response = requests.get(url, stream=True)
		with open(path, 'wb') as file:
			shutil.copyfileobj(response.raw, file)


"""
	Functon to load a image from the images directory.
"""
def load_image(name_file):
	"""
		Args:
			name_file ('str'): The name of the image.

		Return (class:'pygame.Surface'):
			The image founded in the image directory with name 'name_file'.
	"""
	return load(Directory['DIR_IMAGES']+name_file+'.png')


"""
	Functon to load sprite images.
"""
def load_sprite(name_file):
	"""
		Args:
			name_file ('str'): The name of the sprite image.

		Return (class:'pygame.Surface'):
			The image founded in the sprites directory with name 'name_file'.
	"""
	return load(Directory['DIR_SPRITES']+name_file+'.png')


"""
	Functon to load cell images.
"""
def load_cell(name_file):
	"""
		Args:
			name_file ('str'): The name of the cell image.

		Return (class:'pygame.Surface'):
			The image founded in the cells directory with name 'name_file'.
	"""
	return load(Directory['DIR_CELLS']+name_file+'.png')


"""
	Functon to load background images.
"""
def load_background(name_file):
	"""
		Args:
			name_file ('str'): The name of the background image.

		Return (class:'pygame.Surface'):
			The image founded in the backgrounds directory with name 'name_file'.
	"""
	return load(Directory['DIR_BACKGROUND']+name_file+'.png')
