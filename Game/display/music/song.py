#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

# Local imports
from Game.settings import Directory,  Music_Config

# 3rd party imports
import pygame

# General imports
from random import choice

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""

"""
class Song:
    def __init__(self):
        self.name_song = choice(Music_Config['NAME_MUSIC'])+'_'+choice(Music_Config['NAME_GEN'])
        pygame.mixer.music.load(Directory['DIR_MUSIC']+self.name_song+Music_Config['EXTENSION'])
        pygame.mixer.music.set_volume(Music_Config['VOLUME']/100)

    def play(self, print_name = False):
        pygame.mixer.music.play(-1)
        if print_name: print('Playing '+self.name_song+' song')
