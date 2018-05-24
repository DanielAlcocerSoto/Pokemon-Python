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

# General imports
import argparse
from time import time

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


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

#Main of run
if __name__ == '__main__':
