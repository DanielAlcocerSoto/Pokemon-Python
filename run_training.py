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
from Agent.cooperative_model import CoopModel, LearnerModel

# General imports
import argparse
from time import time
from itertools import combinations
from random import choice, randint

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

def set_random_attack(bool):
	from Configuration.settings import Attack_Config
	Attack_Config['USE_VARABILITY'] = bool
	Attack_Config['USE_CRITIC'] = bool
	Attack_Config['USE_MISSING'] = bool
	Attack_Config['USE_IV'] = bool

"""
def set_agents(params,args):
	model = BaseModel()
	def const_agent(r, p): return Agent(r, p, model, train_mode=True)
	params['const_F1']=params['const_F2']=const_agent
	return model
"""

def set_agents(params,args):
	baseModel = BaseModel(model_name = Agent_config['SUPPORT_MODEL_NAME'])
	learnerModel = LearnerModel()
	def const_agent_base(r, p): return Agent(r, p, baseModel, train_mode=False)
	def const_agent_learn(r, p): return Agent(r, p, learnerModel, train_mode=True)
	params['const_A1']=const_agent_base
	params['const_A2']=const_agent_learn
	#params['const_F1']=params['const_F2']=const_agent
	return learnerModel

def run_battle_training(n_episodes, model, params):
	header = '--------------------- EPISODE: {}/{} ---------------------'
	myheader = header.format('{}',n_episodes)
	print('--------------------- TRAINING AGENT ----------------------------')
	start = time()
	print(myheader.format(0))
	for i in range(n_episodes):
		if (i+1)%100 == 0: print(myheader.format(i+1))
		Battle(**params).play()
		if (i+1)%1000 == 0: model.train_and_save()
	model.train_and_save()
	print('Finished! Time = {0:.2f}s'.format(time()-start))


def run_combo_name_battle_training(n_repetitions, model, params):
	header = '--------------------- EPISODE: {}/{} ---------------------'
	start = time()
	names = Pokemon.possible_names()
	possible_names_comb = list(combinations(names, 2))
	len_comb = len(possible_names_comb)
	iner_loop = int(len(names)/2)
	myheader = header.format('{}',len_comb*iner_loop)
	i = 0
	bl = params['base_level']
	vl = params['varability_level']
	print('--------------------- TRAINING AGENT EQUALLY ----------------------------')
	print(myheader.format(0))
	for pF1,pF2 in possible_names_comb:
		for j in range(iner_loop):
			if (i+1)%100 == 0: print(myheader.format(i+1))

			params['poke_A1'] = Pokemon(names[j], bl+randint(-vl,vl))
			params['poke_A2'] = Pokemon(names[-j-1], bl+randint(-vl,vl))
			params['poke_F1'] = Pokemon(pF1, bl+randint(-vl,vl))
			params['poke_F2'] = Pokemon(pF2, bl+randint(-vl,vl))

			Battle(**params).play()
			if (i+1)%10000 == 0: model.train_and_save()
			i+=1
	model.train_and_save()
	print('Finished! Time = {0:.2f}h'.format((time()-start)/3600))

def run_combo_type_battle_training(n_repetitions, model, params):
	header = '--------------------- EPISODE: {}/{} ---------------------'
	from Game.engine.core.type import Type
	from Game.engine.core.pokemon import Pokemon
	type_poke = {}
	for name in Pokemon.possible_names():
		types = Pokemon(name,50)._info['types']
		if len(types) == 1: key = types[0]
		elif types[0] < types[1]: key = types[0]+'-'+types[1]
		else: key = types[1]+'-'+types[0]
		if key in type_poke.keys():type_poke[key].append(name)
		else: type_poke[key] = [name]

	names = list(type_poke.keys())
	possible_types_comb = list(combinations(names, 2))
	len_comb = len(possible_types_comb)
	iner_loop = int(len(names)/2)
	myheader = header.format('{}',len_comb*iner_loop*n_repetitions)
	i = 0
	bl = params['base_level']
	vl = params['varability_level']
	start = time()
	print('--------------------- TRAINING AGENT EQUALLY ----------------------------')
	print(myheader.format(0))
	for pF1,pF2 in possible_types_comb:
		for j in range(iner_loop):
			for k in range(n_repetitions):
				if (i+1)%100 == 0: print(myheader.format(i+1))

				params['poke_A1'] = Pokemon(choice(type_poke[names[j]]), bl+randint(-vl,vl))
				params['poke_A2'] = Pokemon(choice(type_poke[names[-j-1]]), bl+randint(-vl,vl))
				params['poke_F1'] = Pokemon(choice(type_poke[pF1]), bl+randint(-vl,vl))
				params['poke_F2'] = Pokemon(choice(type_poke[pF2]), bl+randint(-vl,vl))

				Battle(**params).play()
				if (i+1)%10000 == 0: model.train_and_save()
				i+=1
	model.train_and_save()
	print('Finished! Time = {0:.2f}h'.format((time()-start)/3600))

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
	set_random_attack(True)

	# Params configuration
	params = Battle.default_argunents()
	params['base_level'] = args.base_level
	params['varability_level'] = args.var_level
	model = set_agents(params,args)
	#run_battle_training(args.episodes, model, params)
	#run_combo_name_battle_training(args.episodes, model, params)
	run_combo_type_battle_training(args.episodes, model, params)

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
