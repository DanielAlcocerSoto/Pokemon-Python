#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that consists mainly of the Battle_display classe.
It is used to generate the battle section, to display the currently state of the
battle. It display the level, name, bar of health and sprite of each pokemon.

It contains the following class:

    Battle_display
"""

# Local imports
from Configuration.settings import Directory, Battle_Config
from Game.display.image import Display, Image, Sprite
from .health import Health_Rect_Info

# General imports
from random import randint

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
		h = Directory['HEALTH_NAME']

		pk_a1 = Sprite(state['Ally_0'], Battle_Config['POS_A1'])
		pk_a2 = Sprite(state['Ally_1'], Battle_Config['POS_A2'])
		pk_f1 = Sprite(state['Foe_0'], Battle_Config['POS_F1'])
		pk_f2 = Sprite(state['Foe_1'], Battle_Config['POS_F2'])

		health_0 = Health_Rect_Info(state['Ally_0'], Battle_Config['POS_A1'], h.format('ally',0))
		health_1 = Health_Rect_Info(state['Ally_1'], Battle_Config['POS_A2'], h.format('ally',1))
		health_2 = Health_Rect_Info(state['Foe_0'], Battle_Config['POS_F1'], h.format('foe',0))
		health_3 = Health_Rect_Info(state['Foe_1'], Battle_Config['POS_F2'], h.format('foe',1))

		visualize_items = [battle_bg, pk_f1, pk_f2, pk_a1, pk_a2,
						   health_0, health_1, health_2, health_3]
		Display.__init__(self, visualize_items)
