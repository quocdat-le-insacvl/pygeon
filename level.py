import pygame as pg
from settings.settings import *
from sprites import *
from tilemap import *
#from fonctions import *
import math
from combat import *
import random 
# HUD functions

class Level:
    def __init__(self, game, level=1):
        self.game = game 
        self.level = level 
        self.num_monster = level * 3
        self.time_spawn_monster = TIME_SPAWN_MONSTER
        self.last_spawn = pg.time.get_ticks()
        
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_spawn >= self.time_spawn_monster:
            self.spawn_monster()
            self.last_spawn = now
        if self.num_monster <= 0:
            self.level_up()
    
    def spawn_monster(self):
        self.num_monster -= 1
        x = random.randint(0, self.game.map.width)
        y = random.randint(0, self.game.map.height)
        Mob(self.game, x, y)
        
    def level_up(self):
        Text(self.game, 'LEVEL UP!!!', RED, 70)
        self.level += 1
        self.num_monster = self.level *3 
