#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from .double_battle import Double_Battle, Attack
from .core.pokemon import Pokemon

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



	Battle = Double_Battle(base_level = 95, varability_level = 5)
	while(not Battle.is_finished()):
		Battle.doTurn()
	Battle.show_result()
	print('Allies win? '+str(Battle.winners()))
