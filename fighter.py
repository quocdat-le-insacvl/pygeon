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
            if self.Action>0:
                if self.level>=3:
                    self.Action-=1
                    self.SW=False
                    return [[self.level,0,1,0,12,2,0,0]for n in range(3)]
                else:
                    hp_bonus=self.action.dice(10)
                    if hp_bonus+self.hp>self.hp_max:
                        self.hp=self.hp_max
                    else:
                        self.hp+=hp_bonus
                    self.Action-=1
                    self.SW=False
        else:
            running=True
            while running:
                running=board_error("no Second Wind left")

    ### Bonus Actions ###
    def extra_attack(self):
        if self.masterAction>0 and self.bonusAction>0:
            self.Action=2
            self.masterAction-=1
            self.bonusAction-=1
        else:
            running=True
            while running:
                running=board_error("no bonus action or Master Action left")
    
    ###Passives###
    def calcul_armor(self,type_of_calcul=0):
        if self.level>=2:
            return super().calcul_armor()+1
        return super().calcul_armor()
    def damage(self):
        return super().damage()+1

"""to do:
    def action_surge(self): |lvl1
    def champion(self): |lvl3
    def extra_attack(self): |lvl4
    toutes les comp avec items"""

        
fighter=Fighter()
print(fighter.damage())