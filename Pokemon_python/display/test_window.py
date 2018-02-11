#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.display.window import Window

#main call
def main():
	display = Window()
	display.set_text_log(['hola que pasa esto es un','texto extra llargo gente'])
	while True:
		display.visualize()
