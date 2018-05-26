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

# General imports
import argparse
from time import time

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


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
	from Agent.model import BaseModel
	print('Running a battle with an agent ally...')
	def constructor_agent(role, pokemon): return AgentPlay(role, pokemon,  BaseModel())
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
	from Agent.model import BaseModel
	print('Running random battles to eval an agent')
	model = BaseModel() #same model in each episode
	def constructor_agent(role, pokemon): return AgentPlay(role, pokemon, model)
	model2 = BaseModel() #same model in each episode
	def constructor_agent2(role, pokemon): return AgentPlay(role, pokemon, model2)
	wins = emp = 0
	header = '--------------------- EPISODE: {}/{} ------- WIN_RATE: {} ---------------------'
	myheader = header.format('{0}',args.episodes,'{1:.2f}')
	for i in range(args.episodes):
		win_rate = (wins*100)/max(i,1)
		print(myheader.format(i+1,win_rate))
		battle = Battle(constructor_trainerA2 = constructor_agent,
						constructor_trainerA1 = constructor_agent2,#TrainerRandom,
						base_level = args.base_level,
						varability_level = args.var_level)
		battle.play()
		if battle.winners() == None: emp +=1
		elif battle.winners(): wins+=1
	# Prins for analize
	print('WINS: {0}/{1} = {2:.2f}%'.format(wins,args.episodes,(wins*100)/args.episodes))
	print('Draws: {0}/{1} = {2:.2f}%'.format(emp,args.episodes,(emp*100)/args.episodes))

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
	eval_agent(parser.parse_args())
