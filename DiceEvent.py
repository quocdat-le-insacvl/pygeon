import pygame
from Dice import Dice
from fonction import generate_randint

class DiceEvent:

    def __init__(self,combat,game):
        #self.compteur = 0
        self.velocity = 2
        self.damage = 0
        self.all_dices = pygame.sprite.Group()
        self.resultat = 0
        self.dice = Dice(20)
        self.combat = combat
        self.start = True
        self.actdamage = False
        self.game = game

    def compter(self):
        self.combat.compteur += self.velocity

    def limit(self):
        return self.combat.compteur == 100

    def reset(self):
        self.combat.compteur = 0
    
    def reset_all(self):
        self.combat.message = "-"
        self.damage = 0 ###
        self.resultat = 0 ###

    def load_dice(self):
        self.all_dices.add(self.dice)

    def check(self):
        if self.limit():
            self.all_dices.remove(self.dice)
            self.combat.pause = True
            self.combat.stop = True
    

    def pause(self):
        if self.limit():
            self.all_dices.remove(self.dice)
            self.dice = Dice("pause")##
            self.load_dice()
            self.reset()
    
    def resume(self,n):
        if n == 6:
            self.actdamage = True
        self.all_dices.remove(self.dice)
        self.combat.pause = False
        self.dice = Dice(n)
        self.load_dice()
        self.reset()


