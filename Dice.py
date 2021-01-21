from settings.color import BLACK
import pygame, os
from settings import *

class Dice(pygame.sprite.Sprite):

    def __init__(self,num,combat,x=650,y=50,life_time=0,born=0):
        super().__init__()
        self.spawn_time = pygame.time.get_ticks()
        self.life_time = life_time
        self.numero = num #pour savoir le type du de
        self.x, self.y = x, y
        self.image = pygame.image.load(os.getcwd() + "/Addon/"+str(num)+".png").convert_alpha()
        # self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center = (self.x,self.y)) #remodifier
        self.combat = combat
        self.born = born

    def rotate(self,surface,angle,screen2):
        if pygame.time.get_ticks() - self.spawn_time >= self.born: 
            rotated_surface = pygame.transform.rotozoom(surface,-angle,1)
            #to not overwrite the original image surface
            rotated_rect = rotated_surface.get_rect(center = (self.x,self.y)) #remodifier
            #return rotated_surface, rotated_rect
            screen2.blit(rotated_surface, rotated_rect)

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time >= self.life_time:
            self.kill()
            self.combat.next_dice = True
            self.combat.stop = True
    
