#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Main exeutable file
"""

# Local imports
from Agent.model import BaseModel

# General imports
from time import time

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
This code rebuid a model from a log file and measures the time it takes.
"""
if __name__ == '__main__':
	"""
		Args: -

		Action:
			This function create a new model with the help of a log and saved in
			a file.
	"""
	print('Training model...')
	start = time()
	model = BaseModel(rebuid=True)
	model.save()
	print('Finished, time = {0:.2f}s'.format(time()-start))
