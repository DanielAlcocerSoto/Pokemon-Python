#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module to load all the game settings, mainly to display and generate database.

This module contains the following configuration dictionaries,
that can be imported to another classes:

	Directory
	Sentence
	Generate_Config
	Attack_Config
	Display_Config
	Battle_Config
	Dialog_Config
	Select_Config
	Font_Config
	Music_Config
"""

# General imports
import json

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Function to load a dictionary.
"""
def _load_dict(path):
	"""
		Args:
			path ('str'): The name of the path.

		Return ('dict'):
			The dictionary founded in the path 'path'.
	"""
	with open(path+'.json', 'r') as json_file:
		obj = json.load(json_file)
	return obj

# The Root of the configuration directory
_ROOT = 'Configuration/'

# The configuration dictionary with directories information (paths, names ...)
Directory = _load_dict(_ROOT+'directory_config')

"""
	Function to load a configuration dictionary.
"""
def _load_config(name):
	"""
		Args:
			name ('str'): The name of the configuration dictionary.

		Return ('dict'):
			The configuration dictionary with name 'name'.
	"""
	return _load_dict(_ROOT+Directory[name])


# The configuration dictionary with the patterns
# of sentences to show messages to the user
Sentence = _load_config('TEXT_PATTERN')

# The configuration dictionary with information about
# how the database must be generated
Generate_Config  = _load_config('GENERATE_CONFIG')

# The configuration dictionary with the settings
# about how to calculate a attack
Attack_Config = _load_config('ATTACK_CONFIG')

# The configuration dictionary with the mainly
# settings about how to display the game
Display_Config = _load_config('DISPLAY_CONFIG')

# The configuration dictionary with the settings
# about how to display the battle section
Battle_Config = _load_config('BATTLE_CONFIG')

# The configuration dictionary with the settings
# about how to display the dialog section
Dialog_Config = _load_config('DIALOG_CONFIG')

# The configuration dictionary with the settings
# about how to display the selection section
Select_Config = _load_config('SELECT_CONFIG')

# The configuration dictionary with the settings
# about how to create a Font class
Font_Config = _load_config('FONT_CONFIG')

# The configuration dictionary with the settings
# about how to play the music of the game
Music_Config = _load_config('MUSIC_CONFIG')

# The configuration dictionary with the
# parameters for RL agent and its model
Agent_config = _load_config('AGENT_CONFIG')
