import pygame

class Monstre:

    def __init__(self,DEX,STR):
        self.name = "Monstre"
        self.resultat = 0
        self.tour = True
        self.DEX = DEX
        self.STR = STR
        self.hit = False
        self.n_de = 6
        self.ac = 10