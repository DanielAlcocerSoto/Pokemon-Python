#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.sittings import load_config
from .display.window import Window

class Interface:
    def __init__(self, state, grafic=True):
        if grafic:
            self.window = Window(state)
            self._func = self.window.set_text
        else:
            self._func = print
        self.sentence = load_config('TEXT_FILE')

    def show(self, name, **args):
        text = self.sentence[name].format(args)
        self._func(text)

    def update():
        try:
            self.window.visualize()
        except:
            pass

    def get_action_user():
        try:
            self.window.visualize()
        except:
            #TODO code in trainer input
            pass
