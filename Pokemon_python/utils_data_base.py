#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from .sittings import Directory

from pygame.image import load

import json
import shutil

def print_dict(d, sort=False):
	print(json.dumps(d, indent=4, sort_keys=sort))

def load_json(name_file):
	with open(Directory['DIR_JSON']+name_file+'.json', 'r') as file:
		obj = json.load(file)
	return obj

def save_json(name_file, obj):
	with open(Directory['DIR_JSON']+name_file+'.json', 'w') as file:
		json.dump(obj, file, indent=4)

def download_sprite(url,name_file):
	response = requests.get(url, stream=True)
	with open(get_sprite_path(name_file), 'wb') as file:
		shutil.copyfileobj(response.raw, file)

def load_image(name_file):
	return load(Directory['DIR_IMAGES']+name_file+'.png')

def load_sprite(name_file):
    return load(Directory['DIR_SPRITES']+name_file+'.png')

def load_cell(name_file):
	return load(Directory['DIR_CELLS']+name_file+'.png')

def load_background(name_file):
	return load(Directory['DIR_BACKGROUND']+name_file+'.png')


class Object_Info:
	def __init__(self, name, file):
		file_dict = load_json(file)
		self._keys = list(file_dict.keys())
		self._name = name
		if self._name in self._keys:
			self._info = file_dict[name]
		else : raise Exception('Name "'+name+'" does not exist in '+file)

	def name(self):
		return self._name
