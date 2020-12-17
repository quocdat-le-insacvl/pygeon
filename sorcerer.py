import pygame
from personnage import Perso
from settings import screen
from math import trunc
from fonctions import exit_checkevent,board_with_msg
from settings import color
class Sorcerer(Perso):
    #proficient with all simple weapons but cannot wear armor
    def __init__(self,STR=8,DEX=8,CON=8,INT=8,WIS=8,CHA=8,hp=10,hp_max=10,inventaire=10,name=None,classe=None,level=0,xp=0):
        super().__init__(classe="sorcerer",hit_dice=6)
        self.name="anthozgg"
        self.attack=0
        self.sPoints=0
        self.spells_slots=[]

    
    


    def get_class(self):
        print(self.classe)

    #################Sorts#################
    #Level1:

    def magic_missile(self):
        running=True
        while running:
            board=board_with_msg("choose a lvl to cast your spell")

            running=exit_checkevent()
            for i in lvl_s:
                deg=self.action.dice(4)+1

        #sort lvl1, envoie un missile supplémentaire par level (level du sort!)
    
    def levelupchange(self):
        super().levelupchange()
        if self.level==1:
            self.spells_slots.append(2)
        elif self.level==2:
            self.spells_slots[0]=3
        elif self.level==3:
            self.spells_slots[0]=4
            self.spells_slots.append(2)
        elif self.level==4:
            self.spells_slots[1]=3
        if self.level>=2:
            self.sPoints=self.level
            self.attack=trunc(self.level/2)
    
