#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from .window import Window

from Pokemon_python.engine.core.pokemon import Pokemon, possible_pokemons_names
from Pokemon_python.sittings import Display_Config

from random import randint, choice

#main call
def main():
	list_poke = possible_pokemons_names()
	base_level = 50
	varability_level = 50
	pokeA1 = Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level))
	pokeA2 = Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level))
	pokeF1 = Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level))
	pokeF2 = Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level))
	state = {
			Display_Config["Ally_0"]:pokeA1,
			Display_Config["Ally_1"]:pokeA2,
			Display_Config["Foe_0"]:pokeF1,
			Display_Config["Foe_1"]:pokeF2}
	display = Window(state)
	display.set_text_log('hola que pasa esto es un texto extra llargo gente')
	while True:
		display.visualize()
