import pygame
from personnage import *

class Fighter(Perso):

    def __init__(self):
        "proficent avec toutes les armes"
        super().__init__(classe="fighter")
        self.hit_dice=10


    def levelupchange(self):
        super().levelupchange() 
        self.attack=self.level

"""to do:
    def action_surge(self): |lvl1
    def champion(self): |lvl3
    def extra_attack(self): |lvl4"""

        

