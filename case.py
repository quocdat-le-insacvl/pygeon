import pygame 
from settings.screen import *
from settings.police import *
from settings.load_img import *
from settings.color import *
from fonction import *

class Case():
    def __init__(self, i, j):
        self.in_case = None
        self.display = pygame.Surface(
            (pixel_red.get_width(), pixel_red.get_height()))
        self.display.blit(case, (0, 0))
        self.display.set_colorkey(BLACK)
        self.i = i
        self.j = j
        self.is_select = False

    def print_contains(self):
        if self.in_case != None:
            #screen.blit(self.in_case.display,(self.cordo()[0]+self.in_case.display.get_width()//2,self.cordo()[1]-self.in_case.display.get_height()//2))
            flip = pygame.transform.flip(self.in_case.display,True,False)
            flip.set_colorkey(BLACK)
            screen.blit(flip,(self.cordo()[0]-self.in_case.display.get_width()//2,self.cordo()[1]-self.in_case.display.get_height()//2+self.in_case.decalage[1]))
    def cordo(self):
        return ((self.j-self.i)*(pixel_red.get_width()+45)//2+screen.get_width()//2-pixel_red.get_width()//2, (self.j+self.i)*(pixel_red.get_width()+45)//4-100)

    def select(self, is_select):
        if is_select:
            screen.blit(case_select, self.cordo())
            self.is_select = True
        else:
            self.display.blit(case, (0, 0))
            screen.blit(self.display, (0, 0))
            self.is_select = False

    def select_neighbour(self, list_case):
        # if self.in_case != None:
        for x in list_case:
            x.is_select = False
            for i in range(-1,2):
                for j in range(-1,2):
                    if x.j+j == self.j and x.i+i == self.i:
                        x.select(True)
                    
    def select_diag(self,list_case):
        for x in list_case:
            for i in range(-7,7):
                if x.j+i == self.j and x.i+i == self.i:
                    x.select(True)
                if x.j+i == self.j and x.i-i == self.i:
                    x.select(True)
    def print_effect(self,list_case):
        for x in list_case:
            x.select(False)
            if x.j-3 == self.j and x.i+3 == self.i:
                x.select_neighbour(list_case)
    def checkIfSelected(self):
        if self.is_select:
            screen.blit(case_select, self.cordo())
