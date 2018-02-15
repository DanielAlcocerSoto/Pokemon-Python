#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

import json

def load_dict(path):
	with open(path+'.json', 'r') as file:
		obj = json.load(file)
	return obj

_ROOT = 'Pokemon_python/'
Directory = load_dict(_ROOT+'directory_config')

def load_config(name):
	return load_dict(_ROOT+Directory[name])

Display_Config = load_config('DISPLAY_CONFIG')
Battle_Config = load_config('BATTLE_CONFIG')
Dialog_Config = load_config('DIALOG_CONFIG')
Font_Config = load_config('FONT_CONFIG')
Music_Config = load_config('MUSIC_CONFIG')
Select_Config = load_config('SELECT_CONFIG')
