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
	if args.action == 'generate_data': generate_data(args)
	elif args.action == 'play_with_rand':
		print('Running a battle with a random ally...')
		Double_Battle(base_level = 50, varability_level = 10).play()
	else: # para no cargar tensorflow siempre
		from Agent.agent_to_play import AgentPlay
		from Agent.agent_to_train import AgentTrain
		from Agent.environment import Environment
		from Agent.model import Model

		if args.action == 'play_to_eval':
			print('Running a battle with an agent ally...')
			def constructor_agent(role, pokemon):
				return TrainerIA(role, pokemon, Model(model_file=args.model_name))
			Double_Battle(  constructor_trainerA2 = constructor_agent, \
							base_level = 50, varability_level = 10).play()
		elif args.action == 'play_to_train':
			print('Running a battle to train an agent')
			#train_RL
		elif args.action == 'eval_agent':
			print('Running random battles to eval an agent')
			print('Not implemented yet... Sorry')
		elif args.action == 'train_agent':
			print('Running random battles to train an agent')
			#train_RL
		elif args.action == 'train_model':
			print('Training model...')
			model = Model()
			model.train()
			model.save(args.model_name)
			print('Finished')

if __name__ == '__main__':
	"""
		Main function of this funcionality.
	"""
	possible_actions = ['generate_data', 'play_with_rand', 'play_to_eval', \
					  	'play_to_train', 'eval_agent', 'train_agent', \
						'train_model']

	program_name = 'Pokémon Game'
	desc =  'This is a program to play a Double Battle Pokémon with an ally ' +\
			'Pokémon played by an artificial intelligence created with deep ' +\
			'reinforcement learning technics'

	desc_actions = 'Main action'

	parser = argparse.ArgumentParser(prog = program_name, description=desc)
	parser.add_argument('action', choices=possible_actions,
						default = 'normal', help=desc_actions)
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

	# Arguments for play
	parser.add_argument('--model_name' , '-model', default = 'model_test',
					help='Param for agent actions. Name of the model to use/create')

	main(parser.parse_args())
