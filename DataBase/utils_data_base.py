#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains useful functions to work with the database.

This module contains the following functions to import to another classes:

	load_info
	save_info
	download_sprite
	load_image
"""

# Local imports
from Configuration.settings import Directory

# 3rd party imports
from pygame.image import load

# General imports
import json
import shutil
import requests
from PIL import Image
from os.path import exists

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
	if not exists(path): # Not download it if it already exists
		response = requests.get(url, stream=True)
		with open(path, 'wb') as file: #create file
			shutil.copyfileobj(response.raw, file)
		# Crop the image
		image=Image.open(path)
		image.load()
		image.crop(image.getbbox()).save(path)

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
