#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

import json

class Configuration:
    def __init__(self, path_config):
    	with open('Pokemon_python/'+path_config+'.json', 'r') as file:
    		self._config = json.load(file)
