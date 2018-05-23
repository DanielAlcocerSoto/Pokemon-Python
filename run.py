#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Main exeutable file
"""

# Local imports
from Game.engine.double_battle import Double_Battle as Battle
from Game.engine.trainer import TrainerRandom
from Game.engine.core.pokemon import Pokemon

from Agent.agent_to_play import AgentPlay
from Agent.agent_to_train import AgentTrain
from Agent.environment import Environment

from DataBase.generator_data_base import \
	generate_pokemons, generate_types, generate_moves

# General imports
import argparse
from time import time

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
	start = args.start
	if  args.type or args.all:
		print('Generating types info...')
		generate_types()
	if  args.move or args.all:
		print('Generating moves info...')
		generate_moves(start_iteration = start)
	if  args.poke or args.all:
		print('Generating pokemons info...')
		generate_pokemons(start_iteration = start)
	if  not (args.poke or args.move or args.type or args.all):
		print(	'Specify that you want to generate: --type (-t), --move (-m),'
				' --poke (-p) or --all (-a)')


"""
This code rebuid a model from a log file and measures the time it takes.
"""
def build_model():
	"""
		Args: -

		Action:
			This function create a new model with the help of a log and saved in
			a file.
	"""
	from Agent.model import Model # so do not load tensorflow always
	from Configuration.settings import Agent_config
	print('Training model...')
	Agent_config['INIT_MODEL_MODE'] = 'REBUILD' #force to rebuild model
	start = time()
	model = Model()
	end = time()
	model.save()
	print('Finished time = {0:.2f}s'.format(end-start))


"""
Run this code to play a battle with a random ally to evaluate the correct
functioning of the game.
"""
def play_with_rand(args):
	"""
		Args:
			args: parse_args return.

		Action:
			This function run a battle with a random ally with the parameters
			indicated in the parameter 'args'.
	"""
	print('Running a battle with a random ally...')
	Battle(	base_level = args.base_level,
			varability_level = args.var_level).play()


"""
Run this code to play a battle with an agent as ally for the manual evaluation
of the model.
"""
def play_to_eval(args):
	"""
		Args:
			args: parse_args return.

		Action:
			This function run a battle with an agent as ally with the parameters
			indicated in the parameter 'args'.
	"""
	from Agent.model import Model
	print('Running a battle with an agent ally...')
	def constructor_agent(role, pokemon): return AgentPlay(role, pokemon,  Model())
	header = '--------------------- EPISODE: {}/{} ---------------------'
	myheader = header.format('{}',args.episodes)
	for i in range(args.episodes):
		print(myheader.format(i+1))
		Battle( constructor_trainerA2 = constructor_agent,
				base_level = args.base_level,
				varability_level = args.var_level).play()



"""
Executes N battles played by a random and an agent to evaluate the performance
of the model.
"""
def eval_agent(args):
	"""
		Args:
			args: parse_args return.

		Action:
			This function play N battles with a random and an agent to evaluate
			the performance	of the model.
	"""
	from Agent.model import Model
	print('Running random battles to eval an agent')
	model = Model() #same model in each episode
	def constructor_agent(role, pokemon): return AgentPlay(role, pokemon, model)
	model2 = Model() #same model in each episode
	def constructor_agent2(role, pokemon): return AgentPlay(role, pokemon, model2)
	wins = emp = 0
	header = '--------------------- EPISODE: {}/{} ---------------------'
	myheader = header.format('{}',args.episodes)
	for i in range(args.episodes):
		print(myheader.format(i+1))
		battle = Battle(constructor_trainerA2 = constructor_agent,
						constructor_trainerA1 = constructor_agent2,#TrainerRandom,
						base_level = args.base_level,
						varability_level = args.var_level)
		battle.play()
		if battle.winners() == None: emp +=1
		elif battle.winners(): wins+=1
		# More prins for analize
	print('WINS: {}/{} = {}%'.format(wins,args.episodes,(wins*100)/args.episodes))
	print('Draws: {}/{} = {}%'.format(emp,args.episodes,(emp*100)/args.episodes))


def play_to_train(args):
	from Agent.model import Model
	print('Running a battle to train an agent')

	model = Model()
	def constructor_agent(role, pokemon):
		model.replay_and_train()
		return AgentTrain(role, pokemon, model)

	header = '--------------------- EPISODE: {}/{} ---------------------'
	myheader = header.format('{}',args.episodes)
	for i in range(args.episodes):
		print(myheader.format(i+1))
		Environment(constructor_trainerA2 = constructor_agent,
					base_level = args.base_level,
					varability_level = args.var_level).play()
	model.save()

def train_agent(args):
	from Configuration.settings import General_config
	from Configuration.settings import Attack_Config
	from Agent.model import Model
	print('Running random battles to train an agent')
	General_config['BATTLE_VERBOSE'] = False
	Attack_Config['USE_VARABILITY'] = False
	Attack_Config['USE_CRITIC'] = False
	Attack_Config['USE_MISSING'] = False
	start = time()
	model = Model()
	def constructor_agent(role, pokemon):
		model.replay_and_train()
		return AgentTrain(role, pokemon, model)

	header = '--------------------- EPISODE: {}/{} ---------------------'
	myheader = header.format('{}',args.episodes)
	for i in range(args.episodes):
		if (i+1)%100 == 0: print(myheader.format(i+1))
		Environment(constructor_trainerA1 = TrainerRandom,
					constructor_trainerA2 = constructor_agent,
					base_level = args.base_level,
					varability_level = args.var_level).play()
	model.save()
	print('Finished time = {0:.2f}s'.format(time()-start))


"""
Main function to execute this program
"""
def main(args):
	"""
		Args:
			args: parse_args return.

		Action:
			This function execute the action indicated in the parameter
			'args.action'.
	"""

	from keras import backend as K
	import tensorflow as tf

	config = tf.ConfigProto(intra_op_parallelism_threads=args.jobs, \
	                        inter_op_parallelism_threads=args.jobs, \
	                        allow_soft_placement=True, \
	                        device_count = {'CPU': args.jobs})
	session = tf.Session(config=config)
	K.set_session(session)

	if   args.action == 'generate_data':  generate_data(args)
	elif args.action == 'play_with_rand': play_with_rand(args)
	elif args.action == 'play_to_train':  play_to_train(args)
	elif args.action == 'play_to_eval':   play_to_eval(args)
	elif args.action == 'train_agent':    train_agent(args)
	elif args.action == 'eval_agent':     eval_agent(args)
	elif args.action == 'train_model':    build_model()

#Main of run
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

	desc_actions = 'Argument to indicate the main action. --------------- ' +\
	' ______________________________________________________'+\
	'"generate_data": This action allows to rebuild information of type, move'+\
	' and/or pokemon from PokeAPI (https://pokeapi.co/). '+\
	' ------------------------------- ' +\
	' ______________________________________________________'+\
	'"play_with_rand": This action executes a battle with a random ally to ' +\
	'evaluate its correct performance. '+\
	' ----- ' +\
	' ______________________________________________________'+\
	'"play_to_eval": This action runs a battle with an agent as ally for the '+\
	'manual evaluation of the model. '+\
	' ______________________________________________________'+\
	'"play_to_train": Executa N battles in which the agent learns from each ' +\
	'of them by playing with the player. '+\
	' - ' +\
	' ______________________________________________________'+\
	'"eval_agent": Executes N battles played by a random and an agent to ' +\
	'evaluate the performance of the model. '+\
	' ______________________________________________________'+\
	'"train_agent": Executes N battles played by a random and an agent to ' +\
	'train the model. '+\
	' --------------------- ' +\
	' ______________________________________________________'+\
	'"train_model": Trains a model with saved information of other games.'

	parser = argparse.ArgumentParser(prog = program_name, description=desc)
	parser.add_argument('action', choices=possible_actions,
						default = 'play_to_eval', help=desc_actions)
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
	# Arguments for play
	parser.add_argument('--episodes' , '-e', type = int, default = 5,
						help='Param for agent train actions. ' +\
						'Number of battles to play')
	parser.add_argument('--base_level' , '-bl', type = int, default = 50,
						help='Param for battle actions. ' +\
						'Base level of each pokemon')
	parser.add_argument('--var_level' , '-vl', type = int, default = 0,
						help='Param for battle actions. ' +\
						'Varability for pokemon\'s level (lvl = Base +/- Var)')
	parser.add_argument('--jobs' , '-j', type = int, default = 4,
						help='Num threads')
	main(parser.parse_args())
