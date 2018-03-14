#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module to test the Agent class
"""

# Local imports
from .environment import Environment
from .modell import Model

# General imports
import argparse

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


file_model = "model_test"

"""
	Test the execution of the Agent class.
"""
def main(args):
    model = Model()
	model.train()
	model.save(file_model)

if __name__ == '__main__':
	"""
		Main function of this funcionality.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('--move', '-m', action='store_true')
	parser.add_argument('--poke', '-p', action='store_true')
	parser.add_argument('--type', '-t', action='store_true')
	parser.add_argument('--all' , '-a', action='store_true')
	main(parser.parse_args())
