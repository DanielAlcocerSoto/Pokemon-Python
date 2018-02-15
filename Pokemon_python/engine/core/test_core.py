#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.core.move import Move
from Pokemon_python.core.pokemon import Pokemon


if __name__ == '__main__':

	print('bulbasaur:')
	pk1=Pokemon('bulbasaur',50)
	print(pk1.health())
	print(pk1.get_stat('attack'))
	print(pk1.moves()[0].name())

	print('\ncharmander:')
	pk2=Pokemon('charmander',50)
	print(pk2.health())
	print(pk2.get_stat('attack'))
	print(pk2.moves()[0].name())

	print('\nditto:')
	pk3=Pokemon('ditto',50)
	print(pk3.health())
	print(pk3.get_stat('attack'))
	for move in pk3.moves_can_use():
		print(move.name())
