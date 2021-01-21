import pygame
from os import path

with open("Save/settings.txt") as options:
    SETTINGS = [ligne for ligne in options]


KEYS_DICO = {'move right': pygame.K_RIGHT, 'move left': pygame.K_LEFT, 'move up': pygame.K_UP, 'move down': pygame.K_DOWN}