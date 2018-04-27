#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Environment class.
This class is the principal class to train an Agent.

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
    def doTurn(self):
        Double_Battle.doTurn(self)
        #recive_results
        for trainer in self._trainers:
            if not trainer.pokemon().is_fainted():
                trainer.recive_results(self.last_attacks,self.is_finished())
