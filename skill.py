from settings.color import BLACK, WHITE
import pygame
from personnage import ava_perso
class Stealth:
    def __init__(self, game, cooldown=7000):
        self.player = game.player
        self.game = game
        self.cooldown = cooldown
        self.last_spawn_time = pygame.time.get_ticks()
        self.available = True 
        # self.player_image = ava_perso
        self.casting = False
        self.duration = 3000
        self.surface_stealth = self.player.img.copy()
        
        
    def update(self):
        now = pygame.time.get_ticks()
        if not self.available and now - self.last_spawn_time > self.cooldown:
            self.available = True
        if self.casting:
            if now - self.last_spawn_time < self.duration:
                self.use()
            else:
                self.unuse()
        self.cast()
        
    def cast(self):
        if self.available:
            print("Cast skill : STEALTH")
                        
            self.available = False
            self.last_spawn_time = pygame.time.get_ticks()
            self.casting = True

    def use(self):
        self.player.img.fill(WHITE)
    
    def unuse(self):
        # self.player.img = self.player_image
        pass
    
