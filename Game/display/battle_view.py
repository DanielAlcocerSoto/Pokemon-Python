#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that consists mainly of the Battle_display classe.
It is used to generate the battle section, to display the currently state of the
battle. It display the level, name, bar of health and sprite of each pokemon.

It contains the following classes:

    Battle_display
    Health_Rect_Info
"""

# Local imports
from Configuration.settings import Directory, Display_Config, Battle_Config
from .image import Display, Image, Sprite
from .utils_display import scale
from .font import Font

# General imports
from random import randint

# 3rd party imports
from pygame import Rect, draw

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Extended class from Display to display the battle section.
"""
class Battle_display(Display):
	def __init__(self, state):
		"""
		    Args:
		        state ('dict of class:Pokemon'): A dictionary with all the
												 information needed to display
		                                         the a battle.
					Note: This dict have as key: "Ally_0","Ally_1","Foe_0" and
						  "Foe_1" with the corresponding pokemon.
		    Action:
		        Create an extension of the "Display" class to display the
				battle section of the game.
		"""
		num = str(randint(0,11))
		battle_bg = Image(Directory['BACKGROUND_NAME'].format(num))

		pk_a1 = Sprite(state['Ally_0'], Battle_Config['POS_A1'])
		pk_a2 = Sprite(state['Ally_1'], Battle_Config['POS_A2'])
		pk_f1 = Sprite(state['Foe_0'], Battle_Config['POS_F1'])
		pk_f2 = Sprite(state['Foe_1'], Battle_Config['POS_F2'])

		h = Directory['HEALTH_NAME']
		health_0 = Health_Rect_Info(state['Ally_0'], Battle_Config['POS_A1'], h.format('ally',0))
		health_1 = Health_Rect_Info(state['Ally_1'], Battle_Config['POS_A2'], h.format('ally',1))
		health_2 = Health_Rect_Info(state['Foe_0'], Battle_Config['POS_F1'], h.format('foe',0))
		health_3 = Health_Rect_Info(state['Foe_1'], Battle_Config['POS_F2'], h.format('foe',1))

		visualize_items = [battle_bg, pk_f1, pk_f2, pk_a1, pk_a2,
						   health_0, health_1, health_2, health_3]
		Display.__init__(self, visualize_items)

"""
	Class to display a info of a pokemon in the battle section.
"""
class Health_Rect_Info:
	def __init__(self, pokemon, POS, path_image):
		"""
		    Args:
		        pokemon (class:'Pokemon'): The pokemon which information will be
										   displayed.
		        POS ('str'): The key to obtain the position where display the
							 pokemon info.

		    Action:
		        Display the info of the 'pokemon' in the 'POS' location.
		"""
		self.bg = Image(path_image)
		self.poke = pokemon
		self.BAR_LENGTH, self.BAR_HEIGHT = scale(Battle_Config['BAR_SIZE'])
		is_ally = 'A' if POS<2 else 'F'
		name_format = Battle_Config['POS_BAR_FORMAT']
		location = Battle_Config[name_format.format(is_ally,POS%2+1)]
		self.POS_BAR = scale(location)

		self.font_name = Font(location, Battle_Config['HEALTH_NAME_SHIFT'])
		self.font_name.set_text(pokemon.name(),'WHITE')

		self.font_level = Font(location, Battle_Config['HEALTH_LVL_SHIFT'])
		self.font_level.set_text(str(pokemon.level()),'WHITE')

	"""
        Funcion to display info of a pokemon.
    """
	def display(self,SCREEN):
		if not self.poke.is_fainted():
			self.bg.display(SCREEN)
			self.font_level.display(SCREEN)
			self.font_name.display(SCREEN)

			pct = self.poke.health()/self.poke.get_stat('hp')
			fill = (pct * self.BAR_LENGTH)
			x, y = self.POS_BAR
			bar_img = Rect(x, y, fill, self.BAR_HEIGHT)
			color_name = 'GREEN' if pct>0.5 else 'YELLOW' if pct>0.25 else 'RED'
			draw.rect(SCREEN, Display_Config[color_name], bar_img)
