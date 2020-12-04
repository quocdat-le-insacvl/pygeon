import pygame as pg
from settings.settings import *
from fonctions import *
from sprites import *

class Combat:
    def __init__(self, game, monster):
        self.game = game
        self.message = "Warning!"
        Text(game, self.message)
