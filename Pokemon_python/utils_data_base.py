#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from pygame.image import load

import json
import shutil

POKE_FILE = 'pokemonDB'
TYPE_FILE = 'typeDB'
MOVE_FILE = 'moveDB'

DIR_DB = 'DataBase/'
DIR_JSON = DIR_DB+'JSon/'
DIR_IMAGES = DIR_DB+'Images/'
DIR_CELLS = DIR_IMAGES+'Cells/'
DIR_SPRITES = DIR_IMAGES+'Sprites/'
DIR_BACKGROUND = DIR_IMAGES+'Backgrounds/'

DISPLAY_CONFIG = 'Pokemon_python/display/display_config.json'
MUSIC_CONFIG = 'Pokemon_python/display/music/music_config.json'

def print_dict(d, sort=False):
	print(json.dumps(d, indent=4, sort_keys=sort))

def load_json(name_file):
	with open(DIR_JSON+name_file+'.json', 'r') as file:
		obj = json.load(file)
	return obj

def save_json(name_file, obj):
	with open(DIR_JSON+name_file+'.json', 'w') as file:
		json.dump(obj, file, indent=4)

def download_sprite(url,name_file):
	response = requests.get(url, stream=True)
	with open(get_sprite_path(name_file), 'wb') as file:
		shutil.copyfileobj(response.raw, file)

def load_image(name_file):
	return load(DIR_IMAGES+name_file+'.png')

def load_sprite(name_file):
    return load(DIR_SPRITES+name_file+'.png')

def load_cell(name_file):
	return load(DIR_CELLS+name_file+'.png')

def load_background(name_file):
	return load(DIR_BACKGROUND+name_file+'.png')

def config(path_config):
	with open(path_config, 'r') as file:
		obj = json.load(file)
	return obj

class Object_Info:
	def __init__(self, name, file):
		fileDict = load_json(file)
		self._keys = list(fileDict.keys())
		self._name = name
		if self._name in self._keys:
			self._info = fileDict[name]
		else : raise Exception('Name "'+name+'" does not exist in '+file)

	def name(self):
		return self._name
