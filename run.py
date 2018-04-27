#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

# Local imports
from Game.engine.double_battle import Double_Battle
from DataBase.generator_data_base import \
	generate_pokemons, generate_types, generate_moves

# General imports
import argparse

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

"""
Run this code to re-generate the information database of Types, Moves, and
Pokemons, and the image dataset of the pokemon sprites.
"""
def generate_data(args):
	"""
		Args:
			args: parse_args return.

		Action:
			This function call the action indicated in the parameter 'args'.
	"""
	print_name = not args.no_print_name
	start = args.start
	print(start)
	if  args.type or args.all:
		print('Generating types info...')
		generate_types(print_name = print_name)
	if  args.move or args.all:
		print('Generating moves info...')
		generate_moves(start_iteration = start, print_name = print_name)
	if  args.poke or args.all:
		print('Generating pokemons info...')
		generate_pokemons(start_iteration = start, print_name = print_name)
	if  not (args.poke or args.move or args.type or args.all):
		print(	'Specify that you want to generate: --type (-t), --move (-m),'
				' --poke (-p) or --all (-a)')

"""
Main function to execute this program
"""
def main(args):
	"""
		Args:
			args: parse_args return.

		Action:
			This function call the action indicated in the parameter 'args'.
	"""
	if args.action == 'normal':
		print('Running a normal battle...')
		Double_Battle(base_level = 50, varability_level = 10).play()
	elif args.action == 'generate_data': generate_data(args)


if __name__ == '__main__':
	"""
		Main function of this funcionality.
	"""
	program_name = 'Pokémon Game'
	desc  = 'This is a program to play a Double Battle Pokémon with an ally ' +\
			'Pokémon played by an artificial intelligence created with deep ' +\
			'reinforcement learning technics'

	parser = argparse.ArgumentParser(prog = program_name, description=desc)
	parser.add_argument('action', choices=['normal','generate_data'],
						default = 'normal', help='Main action')

	# Arguments for generate_data
	parser.add_argument('--type', '-t', action='store_true',
						help='Param for "generate_data" action. Flag to generate type\'s info')
	parser.add_argument('--move', '-m', action='store_true',
                   		help='Param for "generate_data" action. Flag to generate move\'s info')
	parser.add_argument('--poke', '-p', action='store_true',
                  		help='Param for "generate_data" action. Flag to generate pokemon\'s info')
	parser.add_argument('--all' , '-a', action='store_true',
                   		help='Param for "generate_data" action. Flag to generate all the information')
	parser.add_argument('--start' , '-s', type=int, default = 0,
                   		help='Param for "generate_data" action. Number of the starter iteration')
	parser.add_argument('--no_print_name' , action='store_true',
                   		help='Param for "generate_data" action. Flag to not print the name of the data')
	main(parser.parse_args())
