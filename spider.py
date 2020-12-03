import fonctions
import random
from settings import *
import pygame

class Spider:

    def __init__(self,x,y):
        self.pos = [x,y]
        self.stre = 12
        self.dex = 16
        self.con = 13
        self.inte = 3
        self.wis = 12
        self.cha = 4
        self.perception = 3
        self.stealth = 7
        self.passive_p = 13 #passive perception
        self.attack = 3
        self.DC = 11
        self.hp = 10
        self.ac = 13 #armor class

        self.image = pygame.image.load("img/spider.png")
        self.image = pygame.transform.scale(self.image, (2*config.SCALE ,config.SCALE*2))
        self.rect = self.image.get_rect(center = (x,y))

    def damage(self):
        return random.randint(1,6)+1

    def render(self, screen,camera):
        screen.blit(self.image,self.rect)
        
