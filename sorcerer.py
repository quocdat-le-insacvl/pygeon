import pygame
from personnage import Perso
from settings import screen
class Sorcerer(Perso):
    #proficient with all simple weapons but cannot wear armor
    def __init__(self):
        super().__init__(self,classe="sorcerer",hit_dice=6)
        self.attack=0
        self.sPoints=0
        


    def get_class(self):
        print(self.classe)

    #################Sorts#################
    #Level1:

    def magic_missile(self,lvl_s):
        for i in lvl_s:
            deg=self.action.dice(4)+1

        #sort lvl1, envoie un missile supplémentaire par level (level du sort!)