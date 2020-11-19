import pygame
from perso import Perso

perso=Perso()
class Fighter(Perso):

    def __init__(self):
        super().__init__()
        self.health=1000
        self.max_health=1000
        self.mana=300
        self.velocity=10
        self.attack=10
        self.image = pygame.image.load('assets/fighter.png')
        self.x=0
        self.y=400
        self.trans=pygame.image.load('assets/transformation.png')
        self.etat=0


    def transf(self):
        if self.etat==0:
            self.o=200
            self.etat=1
        elif self.etat==1:
            self.mana-=100
            if self.mana<=0:
                self.etat==0
                self.o=0
