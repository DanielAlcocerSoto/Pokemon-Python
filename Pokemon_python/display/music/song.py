#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import config, MUSIC_CONFIG

import pygame

from random import choice

#GLOBAL DISPLAY CONFIGURATIONS
CONFIG = config(MUSIC_CONFIG)
VOLUME = CONFIG['VOLUME']/100
DIR_MUSIC = CONFIG['DIR_MUSIC']
NAME_MUSIC = CONFIG['NAME_MUSIC']
NAME_GEN = CONFIG['NAME_GEN']
EXTENSION = CONFIG['EXTENSION']

class Song:
    def __init__(self):
        self.name_song = choice(NAME_MUSIC)+'_'+choice(NAME_GEN)
        pygame.mixer.music.load(DIR_MUSIC+self.name_song+EXTENSION)
        pygame.mixer.music.set_volume(VOLUME)

    def play(self, print_name = False):
        pygame.mixer.music.play(-1)
        if print_name: print('Playing '+self.name_song+' song')
