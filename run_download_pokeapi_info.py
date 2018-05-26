#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Exeutable file.
Run this code to re-generate the information database of Types, Moves, and
Pokemons, and the image dataset of the pokemon sprites.
"""

# Local imports
from DataBase.generator_data_base import \
	generate_pokemons, generate_types, generate_moves

# General imports
import argparse

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
This functoin re-generate the information database of Types, Moves, and
Pokemons, and the image dataset of the pokemon sprites.
"""
def generate_data(args):
	"""
		Args:
			args: parse_args return.

		Action:
			This function call the action indicated in the parameter 'args'.
	"""
	if  args.type or args.all:
		print('Generating types info...')
		generate_types()
	if  args.move or args.all:
		print('Generating moves info...')
		generate_moves(start_iteration = args.start)
	if  args.poke or args.all:
		print('Generating pokemons info...')
		generate_pokemons(start_iteration = args.start)
	if  not (args.poke or args.move or args.type or args.all):
		print(	'Specify that you want to generate: --type (-t), --move (-m),'
				' --poke (-p) or --all (-a)')

#Main of run
if __name__ == '__main__':
	"""
		Main function of this funcionality.
	"""
	parser = argparse.ArgumentParser()
	# Arguments for generate_data
	parser.add_argument('--type', '-t', action='store_true',
						help='Param for "generate_data" action. ' +\
						'Flag to generate type\'s info')
	parser.add_argument('--move', '-m', action='store_true',
                   		help='Param for "generate_data" action. ' +\
						'Flag to generate move\'s info')
	parser.add_argument('--poke', '-p', action='store_true',
                  		help='Param for "generate_data" action. ' +\
						'Flag to generate pokemon\'s info')
	parser.add_argument('--all' , '-a', action='store_true',
                   		help='Param for "generate_data" action. ' +\
						'Flag to generate all the information')
	parser.add_argument('--start' , '-s', type=int, default = 0,
                   		help='Param for "generate_data" action. ' +\
						'Number of the starter iteration')
	generate_data(parser.parse_args())
