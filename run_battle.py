#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Main exeutable file
"""

# Local imports
from Configuration.settings import General_config, Agent_config
from Game.engine.double_battle import Double_Battle as Battle
from Game.engine.core.pokemon import Pokemon

from Agent.agent import Agent, CoopAgent
from Agent.model import BaseModel
from Agent.cooperative_model import CoopModel, LearnerModel

# General imports
import argparse
from random import Random
import colorama

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


def set_random_attack(bool):
	from Configuration.settings import Attack_Config
	Attack_Config['USE_VARABILITY'] = bool
	Attack_Config['USE_CRITIC'] = bool
	Attack_Config['USE_MISSING'] = bool
	Attack_Config['USE_IV'] = bool

def set_agents(params,args):
	if args.model_type == 'coop':
		print("Using Cooperative Agent")
		if args.model == "": model = CoopModel()
		else: model = CoopModel(model_name = args.model)
		def const_agent(r, p): return CoopAgent(r, p, model, train_mode=False)
	else:
		if args.model_type == 'base':
			print("Using Base Agent")
			if args.model == "": model = BaseModel()
			else: model = BaseModel(model_name = args.model)
		else:
			print("Using Learner Agent")
			if args.model == "": model = LearnerModel()
			else: model = LearnerModel(model_name = args.model)
		def const_agent(r, p): return Agent(r, p, model, train_mode=False)
	params['const_A2']=const_agent


"""
Execute a battle with a TrainerInput and agent
"""
def main(args):
	"""
		Args:
			args: parse_args return.

		Action:
			This function play a battle with a player and an agent.
	"""


	#General configuartion
	General_config['BATTLE_VERBOSE'] = True
	General_config['GENERATIONS'] = [1,2,3,4]
	set_random_attack(args.random)

	# Params configuration
	params = Battle.default_argunents()
	params['base_level'] = args.base_level
	params['varability_level'] = args.var_level
	set_agents(params,args)


	colorama.init()

	#random
	import random
	random.seed(222)

	N_Games = 2
	Battles = [(0,333),(1,333),(2,111),(4,222)]

	k=1
	for i, seed in Battles:
		for test in range(N_Games):
			if args.seed !=0: params['rand'] = Random(seed) #Random(args.seed)
			battle = Battle(**params)
			for j in range(0,i): battle = Battle(**params)
			print('________________ BATTLE NUMBER {} ________________'.format(k))
			battle.play()
		k+=1


#Main of run
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--base_level' , '-bl', type = int, default = 50,
						help='Param for battle actions. ' +\
						'Base level of each pokemon')
	parser.add_argument('--var_level' , '-vl', type = int, default = 2,
						help='Param for battle actions. ' +\
						'Varability for pokemon\'s level (lvl = Base +/- Var)')

	parser.add_argument('--model' , '-m', type = str, default = "coop",
						help='Name of the model to use as ally agent.')
	parser.add_argument('--model_type', default = 'coop',
						choices = ['base', 'learner', 'coop'],
						help='Model of ally')
	parser.add_argument('--random' , '-r', type = bool, default = True,
						help='Use random in battle')

	parser.add_argument('--seed' , '-s', type=int, default = 222,
						help='Seed to generate pokemon')
	main(parser.parse_args())
