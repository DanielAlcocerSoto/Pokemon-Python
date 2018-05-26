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


def set_poke(params):
	pass#params['poke_A1'] = Pokemon.Random(50, 0)

def set_agents(params):
	model = BaseModel() #same model in each episode -> no load memory
	def const_agent(r, p): return Agent(r, p, model, train_mode=False)
	params['const_A1']=params['const_A2']=const_agent

def run_battle_evaluation(n_episodes, params):
	header = '--------------------- EPISODE: {}/{} ------- WIN_RATE: {} ---------------------'
	myheader = header.format('{0}',n_episodes,'{1:.2f}')
	wins = emp = 0
	print('--------------------- EVALUATING AGENT ----------------------------')
	for i in range(n_episodes):
		win_rate = (wins*100)/max(i,1)
		print(myheader.format(i+1,win_rate))
		battle = Battle(**params)
		battle.play()
		if battle.winners() == None: emp+=1
		elif battle.winners(): wins+=1
	# Prins for analize
	print('----------------------------------------------------------')
	print('--------------------- RESULTS ----------------------------')
	print('WINS: {0}/{1} = {2:.2f}%'.format(wins,n_episodes,(wins*100)/n_episodes))
	print('Draws: {0}/{1} = {2:.2f}%'.format(emp,n_episodes,(emp*100)/n_episodes))
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
	# GPU TensorFlow Configuration
	from keras import backend as K
	import tensorflow as tf
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	session = tf.Session(config=config)
	K.set_session(session)
	print('GPU TensorFLow Configurated')

	# Params configuration
	params = Battle.default_argunents()
	params['base_level'] = args.base_level
	params['varability_level'] = args.var_level
	set_poke(params)
	set_agents(params)
	run_battle_evaluation(args.episodes, params)

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
