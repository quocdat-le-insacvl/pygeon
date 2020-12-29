import pygame

class Monstre:

    def __init__(self,DEX):
        self.name = "Monstre"
        self.resultat = 0
        self.tour = True
        self.DEX = DEX
        self.hit = False
        self.n_de = 6
        self.ac = 10
        self.hp = 100