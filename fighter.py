import pygame
from personnage import *

class Fighter(Perso):

    def __init__(self):
        "proficent avec toutes les armes"
        super().__init__(classe="fighter")
        self.hit_dice=10
        "si SW (Second Wind) est a true il est utilisable"
        self.SW=False

    def levelupchange(self):
        super().levelupchange() 
        self.attack=self.level
        if self.level==1:
            self.SW=True

    def rest(self):
        super().rest()
        self.SW=True

    ### Actions ###
    def secondWind(self):
        if self.SW==True:
            hp_bonus=self.action.dice(10)
            if

    
    def extra_attack(self):
        if self.masterAction>0 and self.bonusAction>0:
            self.Action=2
            self.masterAction-=1
            self.bonusAction-=1
        else:
            running=True
            while running:
                running=board_error("no bonus action or Master Action left")
    
    ### Fin des actions ###

"""to do:
    def action_surge(self): |lvl1
    def champion(self): |lvl3
    def extra_attack(self): |lvl4"""

        

