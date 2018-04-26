#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Run this code to re-generate the information database of Types, Moves, and
Pokemons, and the image dataset of the pokemon sprites.
"""

# Local import
from Game.generate_data.generator_data_base import \
	generate_pokemons, generate_types, generate_moves

# General imports
import argparse

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


def action(args):
	"""
		Args:
			args: parse_args return.

		Action:
			This function call the action indicated in the parameter 'args'.
	"""
	if  args.move or args.all:
		print('Generating moves info...')
		generate_moves()
	if  args.poke or args.all:
		print('Generating pokemons info...')
		generate_pokemons()
	if  args.type or args.all:
		print('Generating types info...')
		generate_types()
	if  not (args.poke or args.move or args.type or args.all):
		print(	'Specify that you want to generate: --move(-m), --poke(-p),'
				' --type(-t) or --all(-a)')


if __name__ == '__main__':
	"""
		Main function of this funcionality.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('--move', '-m', action='store_true')
	parser.add_argument('--poke', '-p', action='store_true')
	parser.add_argument('--type', '-t', action='store_true')
	parser.add_argument('--all' , '-a', action='store_true')
	action(parser.parse_args())
