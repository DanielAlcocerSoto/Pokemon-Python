#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import save_json, load_json, print_dict
from Pokemon_python.sittings import Directory

import requests
import json
import argparse


moves = load_json(Directory['MOVE_FILE'])
x = {}
for name, info in moves.items():
    x[name] = {field: value
        for field, value in info.items()
        if field != 'es_name'
    }
print_dict(x)

save_json(Directory['MOVE_FILE'],x)
