import pygame
from perso import Perso

perso=Perso()

class Ennemie(Perso):

    def __init__(self):
        super().__init__()
        self.health=100
        self.health=10000
        self.max_health=10000
        self.velocity=10
        self.attack=10
        self.image = pygame.image.load('assets/ennemy.png')
        self.x=1200
        self.y=400
