import pygame as pg
from settings.settings import *
# from fonctions import *
from sprites import *

class Combat:
    def __init__(self, game):
        self.game = game
        self.game.player.reset()
        self.message = "Combat started!!!!"
        Text(game, self.message, RED, 100, [100, HEIGHT // 2 ])
