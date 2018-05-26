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
from time import time

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

def set_random_attack(bool):
	from Configuration.settings import Attack_Config
	Attack_Config['USE_VARABILITY'] = bool
	Attack_Config['USE_CRITIC'] = bool
	Attack_Config['USE_MISSING'] = bool
	Attack_Config['USE_IV'] = bool

def set_poke(params,args):
	pass#params['poke_A1'] = Pokemon.Random(50, 0)

def set_agents(params,args):
	model = BaseModel()
	def const_agent(r, p): return Agent(r, p, model, train_mode=True)
	params['const_A1']=params['const_A2']=const_agent
	params['const_F1']=params['const_F2']=const_agent
	return model

def run_battle_training(n_episodes, model, params):
	header = '--------------------- EPISODE: {}/{} ---------------------'
	myheader = header.format('{}',n_episodes)
	print('--------------------- TRAINING AGENT ----------------------------')
	start = time()
	for i in range(n_episodes):
		if (i+1)%100 == 0: print(myheader.format(i+1))
		Battle(**params).play()
		if (i+1)%1000 == 0: model.train_and_save()
	model.train_and_save()
	print('Finished! Time = {0:.2f}s'.format(time()-start))

def main(args):
	# GPU TensorFlow Configuration
	from keras import backend as K
	import tensorflow as tf
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	session = tf.Session(config=config)
	K.set_session(session)
	print('GPU TensorFLow Configurated')

	#General configuartion
	General_config['BATTLE_VERBOSE'] = False
	set_random_attack(False)

	# Params configuration
	params = Battle.default_argunents()
	params['base_level'] = args.base_level
	params['varability_level'] = args.var_level
	set_poke(params,args)
	model = set_agents(params,args)
	run_battle_training(args.episodes, model, params)

#Main of run
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--episodes' , '-e', type = int, default = 5,
						help='Param for agent train actions. ' +\
						'Number of battles to play')
	parser.add_argument('--base_level' , '-bl', type = int, default = 50,
						help='Param for battle actions. ' +\
						'Base level of each pokemon')
	parser.add_argument('--var_level' , '-vl', type = int, default = 0,
						help='Param for battle actions. ' +\
						'Varability for pokemon\'s level (lvl = Base +/- Var)')
	main(parser.parse_args())
