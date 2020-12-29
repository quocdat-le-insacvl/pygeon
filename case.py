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
            if x.j == self.j and x.i == self.i - 1:
                x.select(True)
            if x.j == self.j and x.i == self.i + 1:
                x.select(True)
            if x.i == self.i and x.j == self.j - 1:
                x.select(True)
            if x.i == self.i and x.j == self.j + 1:
                x.select(True)

    def checkIfSelected(self):
        if self.is_select:
            screen.blit(case_select, self.cordo())
