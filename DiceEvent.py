import pygame as pg
from Dice import Dice

class DiceEvent:

    def __init__(self,combat,game=None):
        #self.compteur = 0
        self.velocity = 2
        self.damage = 0
        self.all_dices = pg.sprite.Group()
        self.resultat = 0
        self.dice = Dice(20,combat,life_time=1000)
        self.combat = combat
        self.start = True
        self.actdamage = False
        self.game = game
        self.time = 1000
        self.resultat = 0
        self.resultat_monstreatk, self.resultat_degats = 0, 0

    
    def reset_all(self):
        self.combat.message = "-"
        self.damage = 0 ###
        self.resultat = 0 ###

    def load_dice(self,i):
        self.dice.life_time = self.time + i
        self.all_dices.add(self.dice)

    def resume(self,n,i=1000,birthday_time=0):
        if n == 6:
            self.combat.actdamage = True #
        self.combat.pause = False
        self.dice = Dice(n,self.combat,born = birthday_time)
        self.load_dice(i)


