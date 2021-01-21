from settings.color import BLACK, WHITE
import pygame
from personnage import img_perso, perso_stealth
from settings.screen import *
from fonction import draw_text
from settings.police import Drifftype, ColderWeather, Rumbletumble, coeff, coeff1, coeff2, ColderWeather_small
from settings.load_img import light_mask
class Stealth:
    def __init__(self, game, cooldown=5000):
        self.player = game.player
        self.game = game
        self.screen = screen
        self.cooldown = cooldown
        self.last_spawn_time = pygame.time.get_ticks()
        self.available = True 
        self.player_image = img_perso
        self.perso_stealth = perso_stealth
        self.casting = False
        self.duration = 3000
        self.surface_stealth = self.player.img.copy()
        self.fog_steath = pygame.Surface(self.screen.get_size()).convert()
        self.fog_steath.set_colorkey(BLACK, pygame.RLEACCEL)
        self.fog_steath.fill((200, 200, 200))
        
    def update(self):
        now = pygame.time.get_ticks()
        draw_text("Stealth available: %i " % ( self.available), ColderWeather, WHITE, screen, 100, 300)
        if not self.available and now - self.last_spawn_time > self.cooldown:
            self.available = True
        if self.casting:
            if now - self.last_spawn_time < self.duration:
                self.use()
            else:
                self.unuse()
        # self.cast()
        
    def cast(self):
        if self.available:
            print("Cast skill : STEALTH")
                        
            self.available = False
            self.last_spawn_time = pygame.time.get_ticks()
            self.casting = True
            self.player.visible = False
            '''
            for monster in self.game.list_mooving_entity:
                monster.is_aggresive = False'''

    def use(self):
        self.player.img = self.perso_stealth

        self.screen.blit(self.fog_steath, (0, 0),
                         special_flags=pygame.BLEND_MULT)

    def unuse(self):
        self.player.img = self.player_image
        self.player.visible = True
        '''for monster in self.game.list_mooving_entity:
            monster.is_aggresive = True'''
    

class Perception:
    def __init__(self, game, cooldown=5000):
        self.player = game.player
        self.game = game
        self.screen = screen
        self.cooldown = cooldown
        self.last_spawn_time = pygame.time.get_ticks()
        self.available = True
        self.casting = False
        self.duration = 3000
        self.light_image = self.game.fog.light_image
        self.light_rect = self.game.fog.light_rect
        self.radius = self.game.fog.light_radius
        self.expand = 0
        self.light_mask = light_mask
        
        # Pour efficacité
        self.pause = 100 
        self.last_expand = pygame.time.get_ticks()

        

    def update(self):
        now = pygame.time.get_ticks()
        draw_text("Perception available: %i " % (self.available),
                  ColderWeather, WHITE, screen, 100, 400)
        if not self.available and now - self.last_spawn_time > self.cooldown:
            self.available = True
        if self.casting:
            if now - self.last_spawn_time < self.duration:
                self.use()
            else:
                self.unuse()
        # self.cast()

    def cast(self):
        if self.available:
            print("Cast skill : STEALTH")

            self.available = False
            self.last_spawn_time = pygame.time.get_ticks()
            self.casting = True
            self.expand = 0

    def use(self):
        now = pygame.time.get_ticks()

        if now - self.last_expand > self.pause:
            self.expand += 60
            #self.player.img = self.perso_stealth
            self.game.fog.light_image = pygame.transform.scale(
                self.light_mask, (self.radius + self.expand, self.radius + self.expand))
            self.game.fog.light_rect = self.game.fog.light_image.get_rect()
            self.last_expand = now

    def unuse(self):
        self.game.fog.light_image = pygame.transform.scale(
            self.light_mask, (self.radius, self.radius))
        self.game.fog.light_rect = self.game.fog.light_image.get_rect()
