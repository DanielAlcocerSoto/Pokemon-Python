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

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


def set_random_attack(bool):
	from Configuration.settings import Attack_Config
	Attack_Config['USE_VARABILITY'] = bool
	Attack_Config['USE_CRITIC'] = bool
	Attack_Config['USE_MISSING'] = bool
	Attack_Config['USE_IV'] = bool

def set_agents(params,args):
	#same model in each episode -> no load memory
	if args.model_type == 'coop':
		auxModel = BaseModel(model_name = Agent_config['SUPPORT_MODEL_NAME'])
		def const_agent_base(r, p): return Agent(r, p, auxModel, train_mode=False)
		model = CoopModel()

		def const_agent(r, p): return CoopAgent(r, p, model, train_mode=False)
		params['const_A2'] = const_agent_base
	else:
		if args.model_type == 'base':model = BaseModel()
		else: model = LearnerModel()

		def const_agent(r, p): return Agent(r, p, model, train_mode=False)
		params['const_A2']=const_agent
	params['const_A1']=const_agent

def run_random_battle_evaluation(n_episodes, params):
	header = '--------------------- EPISODE: {}/{} ------- WIN_RATE: {} ---------------------'
	myheader = header.format('{0}',n_episodes,'{1:.2f}')
	wins = emp = turns = 0
	print('--------------------- EVALUATING AGENT RANDOM ----------------------------')
	for i in range(n_episodes):
		win_rate = (wins*100)/max(i,1)
		print(myheader.format(i+1,win_rate))
		battle = Battle(**params)
		battle.play()
		winners = battle.winners()
		if winners == None: emp+=1
		elif winners:
			wins+=1
			turns += battle.n_turn
	# Prins for analize
	print('----------------------------------------------------------')
	print('--------------------- RESULTS ----------------------------')
	print('WINS: {0}/{1} = {2:.2f}%'.format(wins,n_episodes,(wins*100)/n_episodes))
	print('Draws: {0}/{1} = {2:.2f}%'.format(emp,n_episodes,(emp*100)/n_episodes))
	print('Mean turns: {0:.2f}'.format(turns/(n_episodes-emp)))
	print('State Size: {0}'.format(BaseModel().encoder.state_size))
	print('----------------------------------------------------------')

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

	#General configuartion
	General_config['BATTLE_VERBOSE'] = False
	if args.generation == 234: General_config['GENERATIONS'] = [2,3,4]
	set_random_attack(args.no_random)

	# Params configuration
	params = Battle.default_argunents()
	params['base_level'] = args.base_level
	params['varability_level'] = args.var_level
	if args.seed !=0: params['rand'] = Random(args.seed)
	set_agents(params,args)
	run_random_battle_evaluation(args.episodes, params)

#Main of run
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--episodes' , '-e', type = int, default = 2000,
						help='Param for agent train actions. ' +\
						'Number of battles to play')
	parser.add_argument('--base_level' , '-bl', type = int, default = 50,
						help='Param for battle actions. ' +\
						'Base level of each pokemon')
	parser.add_argument('--var_level' , '-vl', type = int, default = 2,
						help='Param for battle actions. ' +\
						'Varability for pokemon\'s level (lvl = Base +/- Var)')

	parser.add_argument('--no_random' , '-no_rand', action = 'store_false',
						default = True, help='Param for train with random')
	parser.add_argument('--generation' , '-gen', type=int, default = 234,
						choices = [1,234],
						help='Param for test with gen 1 or the others')
	parser.add_argument('--model_type', default = 'base',
						choices = ['base', 'learner', 'coop'],
						help='Model of ally')

	parser.add_argument('--seed' , '-s', type=int, default = 222,
						help='Seed to generate pokemon')
	main(parser.parse_args())
