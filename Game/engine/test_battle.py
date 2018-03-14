#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module to test the Double_Battle class
"""

# Local imports
from .double_battle import Double_Battle

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Test the execution of the Double_Battle class.
"""
def main():
	Double_Battle(base_level = 50, varability_level = 10).play()
