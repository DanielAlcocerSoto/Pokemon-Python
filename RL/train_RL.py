#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module to test the Agent class
"""

# Local imports
from Game.engine.core.pokemon import Pokemon_Random
from RL.agent_to_train import AgentTrain
from RL.environment import Environment
from RL.model import Model

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Test the execution of the Agent class.
"""
if __name__ == "__main__":
	episodes = 2
	base_level = 50
	varability_level = 10

	pokemon = Pokemon_Random(base_level, varability_level)
	model = Model() #change to specify path
	agent = AgentTrain('Ally_1', pokemon, model)

	def constructor_agent(role, pokemon):
		return agent

	# Iterate the game
	for e in range(episodes):
		Environment(constructor_trainerA2 = constructor_agent, \
					base_level = base_level,
					varability_level=varability_level).play()

		agent.replay(Pokemon_Random(base_level, varability_level))

	agent.save_model()
