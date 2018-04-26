#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module to test the Window class
"""

# Local imports
from Game.settings import Display_Config
from Game.engine.core.pokemon import Pokemon
from .window import Window

# General imports
from random import randint, choice

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Test the execution of the Window class.
"""
def main():
	list_poke = Pokemon.possible_names()
	base_level = 50
	vary = 50
	pokeA1 = Pokemon(choice(list_poke), base_level + randint(-vary,vary))
	pokeA2 = Pokemon(choice(list_poke), base_level + randint(-vary,vary))
	pokeF1 = Pokemon(choice(list_poke), base_level + randint(-vary,vary))
	pokeF2 = Pokemon(choice(list_poke), base_level + randint(-vary,vary))
	state = {
			"Ally_0":pokeA1,
			"Ally_1":pokeA2,
			"Foe_0":pokeF1,
			"Foe_1":pokeF2}
	display = Window(state)
	display.show('TEST')
	while True:
		display.visualize()
