import pygame
from personnage import *

class Rogue(Perso):

    def __init__(self,x=100,y=100,STR=8,DEX=8,CON=8,INT=8,WIS=8,CHA=8,hp=5,hp_max=5,level=0,xp=0,name=None):
        super().__init__(x=x,y=y,classe="rogue",hit_dice=6,name=name,STR=STR,DEX=DEX,CON=CON,INT=INT,WIS=WIS,CHA=CHA,hp=hp,hp_max=hp_max)

    def saving_throw(self,cara,damage,dc):
        """competence d'amelioration du saving throw de l'assassin"""
        dmg=super().saving_throw(cara,damage,dc)
        if dmg==damage//2 and cara==0 and self.level==2:
            return 0
        else:
            return dmg
    


