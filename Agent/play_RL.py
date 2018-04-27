
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module to test the Double_Battle class
"""

# Local imports
from Game.engine.double_battle import Double_Battle
from Agent.agent_to_play import TrainerIA
from Agent.model import Model

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Test the execution of the Double_Battle class.
"""
if __name__ == "__main__":
	def constructor_agent(role, pokemon):
		return TrainerIA(role, pokemon, Model( model_file='model_test')) #change to specify path

	Double_Battle(  constructor_trainerA2 = constructor_agent, \
					base_level = 50, varability_level = 10).play()
