#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Environment class.
This class is the principal class to execute a battle in the game.

It contains the following class:

	Environment
"""

# Local imports
from Game.engine.double_battle import Double_Battle

# General imports
from random import randint, choice

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Class to make a environment for train RL.
"""
class Environment(Double_Battle):
    def __init__(self, agent, base_level = 50, varability_level = 5):
        Double_Battle.__init__(self, trainerA2 = agent, base_level = base_level,
                                     varability_level = varability_level)
