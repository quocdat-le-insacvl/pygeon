import pygame
from personnage import *

class Fighter(Perso):

    def __init__(self):
        super().__init__(classe="fighter")
        self.hit_dice=10
        # self.image = pygame.image.load('projet pygame/assets/Fighter.png')

        # self.trans=pygame.image.load('projet pygame/assets/transformation.png')


    def get_class(self):
        print(self.classe)

    def levelupchange(self):
        super().levelupchange()  

        

