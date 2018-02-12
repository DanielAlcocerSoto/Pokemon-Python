#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.directory_config import Directory
from Pokemon_python.display.music.music_config import Music_Config

import pygame

from random import choice


class Song:
    def __init__(self):
        self.name_song = choice(Music_Config.NAME_MUSIC)+'_'+choice(Music_Config.NAME_GEN)
        pygame.mixer.music.load(Directory.DIR_MUSIC+self.name_song+Music_Config.EXTENSION)
        pygame.mixer.music.set_volume(Music_Config.VOLUME/100)

    def play(self, print_name = False):
        pygame.mixer.music.play(-1)
        if print_name: print('Playing '+self.name_song+' song')
