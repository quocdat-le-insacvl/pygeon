import pygame, os
from settings import *

class Dice(pygame.sprite.Sprite):

    def __init__(self,num):
        super().__init__()
        self.numero = num #pour savoir le type du de
        self.image = pygame.image.load(os.getcwd() + "/Addon/"+str(num)+".png")
        self.rect = self.image.get_rect(center = (620,180)) #remodifier

    def rotate(self,surface,angle,screen2):
        rotated_surface = pygame.transform.rotozoom(surface,-angle,1) 
        #to not overwrite the original image surface
        rotated_rect = rotated_surface.get_rect(center = (620,170)) #remodifier
        #return rotated_surface, rotated_rect
        screen2.blit(rotated_surface,rotated_rect)

#config.SCREEN_X/2,config.SCREEN_Y/2