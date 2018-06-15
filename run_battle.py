#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Main exeutable file
"""

# Local imports
from Configuration.settings import General_config, Agent_config
from Game.engine.double_battle import Double_Battle as Battle
from Game.engine.core.pokemon import Pokemon

from Agent.agent import Agent
from Agent.model import BaseModel

# General imports
import argparse

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


def set_random_attack(bool):
	from Configuration.settings import Attack_Config
	Attack_Config['USE_VARABILITY'] = bool
	Attack_Config['USE_CRITIC'] = bool
	Attack_Config['USE_MISSING'] = bool
	Attack_Config['USE_IV'] = bool

def set_agents(params,args):
	model = BaseModel(model_name = args.model)
	def const_agent(r, p): return Agent(r, p, model, train_mode=False)
	params['const_A2']=const_agent

"""
Executes N battles played by two agent to evaluate the performance of the model.
"""
def main(args):
	"""
		Args:
			args: parse_args return.

		Action:
			This function play N battles with a random and an agent to evaluate
			the performance	of the model.
	"""
	# GPU TensorFlow Configuration
	from keras import backend as K
	import tensorflow as tf
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	session = tf.Session(config=config)
	K.set_session(session)
	print('GPU TensorFlow Configurated')

	#General configuartion
	General_config['BATTLE_VERBOSE'] = True
	General_config['GENERATIONS'] = [2,3,4]
	set_random_attack(args.random)

	# Params configuration
	params = Battle.default_argunents()
	params['base_level'] = args.base_level
	params['varability_level'] = args.var_level
	set_agents(params,args)
	Battle(**params).play()

#Main of run
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--base_level' , '-bl', type = int, default = 50,
						help='Param for battle actions. ' +\
						'Base level of each pokemon')
	parser.add_argument('--var_level' , '-vl', type = int, default = 0,
						help='Param for battle actions. ' +\
						'Varability for pokemon\'s level (lvl = Base +/- Var)')

	parser.add_argument('--model' , '-m', type = str, default = "",
											help='Model to use as ally agent.')
	parser.add_argument('--random' , '-r', type = bool, default = True,
						help='Use random in battle')
	main(parser.parse_args())
