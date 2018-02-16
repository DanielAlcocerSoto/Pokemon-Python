#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from .window import Window

from Pokemon_python.engine.core.pokemon import Pokemon, possible_pokemons_names

from random import randint, choice

#main call
def main():
	list_poke = possible_pokemons_names()
	base_level = 50
	varability_level = 5
	trainerA1 = Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level))
	trainerA2 = Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level))
	trainerF1 = Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level))
	trainerF2 = Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level))
	state = {"Ally_0":trainerA1,"Ally_1":trainerA2,"Foe_0":trainerF1,"Foe_1":trainerF2}
	display = Window(state)
	display.set_text_log('hola que pasa esto es un texto extra llargo gente')
	while True:
		display.visualize()
