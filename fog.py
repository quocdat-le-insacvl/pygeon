from settings.screen import screen
from settings.color import NIGHT_COLOR,LIGHT_RADIUS
from settings.load_img import light_mask
import pygame
from personnage import Perso

class Fog:
    def __init__(self, player,map_display):
        
        self.player = player
        self.screen = screen
        self.surface = pygame.Surface(
            map_display.get_size()).convert()
        self.surface.fill(NIGHT_COLOR)
        # self.surface.set_colorkey(BLACK)
        self.light_image = light_mask
        self.light_radius = LIGHT_RADIUS
        self.light_image = pygame.transform.scale(
            self.light_image, (self.light_radius, self.light_radius))
        self.light_rect = self.light_image.get_rect()

    def draw_fog(self):
        self.light_rect.center = (self.player.pos_x+self.player.img.get_width() //
                                  2, self.player.pos_y+self.player.img.get_height()//2)
       
        self.surface.blit(self.light_image, self.light_rect)
    def init_fog_for_dungeon(self):
        self.light_image = pygame.transform.scale(
        self.light_image, (400, 400))

        self.light_rect = self.light_image.get_rect()
    def draw_fog_dungeon(self):
        self.light_rect.center = (self.player.pos_x+32 //
                                  2, self.player.pos_y+49//2)
       
        self.surface.blit(self.light_image, self.light_rect)


