#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module to test the Double_Battle class
"""

# Local imports
from .double_battle import Double_Battle, Attack
from .core.pokemon import Pokemon

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Test the execution of the Double_Battle class.
"""
def main():
	"""
	a1=Attack(pk1,pk2,pk1.moves()[0])
	print('\nbulbasaur vs. charmander')
	print(a1.dmg)
	print(a1.is_critic)
	print(pk2.health())

	a2=Attack(pk2,pk1,pk2.moves()[0])
	print('\ncharmander vs. bulbasaur')
	print(a2.dmg)
	print(a2.is_critic)
	print(pk1.health())
    """

	#tr0 = TrainerInput(ALLY, Pokemon('bulbasaur', 95))
	#tr2 = TrainerRandom(FOE, Pokemon('seadra',95))


	Battle = Double_Battle(base_level = 50, varability_level = 10)
	while(not Battle.is_finished()):
		Battle.doTurn()
	Battle.show_result()
