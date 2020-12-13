import pygame

class Competence():
    def __init__(self,classe):
        self.classe=classe
    
    def competence1(self):
        if self.classe=="fighter":
            print("selectionne la competence 1 fighter")
        if self.classe=="wizard":
            print("you earn magic missile")
        if self.classe=="rogue":
            print("selectionne la competence 1 sale rogue")
    def competence2(self):
        print("selectionne la competence 2")
    def competence3(self):
        print("selectionne la competence 3")
    def competence4(self):
        print("selectionne la competence 4")
    def competence5(self):
        print("selectionne la competence 5")



    
    