import pygame 
from settings.screen import *
from settings.police import *
from settings.load_img import *
from settings.color import *
from fonction import *
from monster import *

class Case():
    def __init__(self, i, j):
        self.in_case = None
        self.display = pygame.Surface(
            (pixel_red.get_width(), pixel_red.get_height()))
        self.display.set_colorkey(WHITE)
        self.display.blit(case, (0, 0))
        self.display.set_colorkey(BLACK)
        self.i = i
        self.j = j
        self.is_select = False

    def print_contains(self,flip=True,x=0,y=0):
        if self.in_case != None:
            #screen.blit(self.in_case.display,(self.cordo()[0]+self.in_case.display.get_width()//2,self.cordo()[1]-self.in_case.display.get_height()//2))
            if flip:
                display = pygame.transform.flip(self.in_case.display,True,False)
                display.set_colorkey(BLACK)
                screen.blit(display,(self.cordo()[0]-self.in_case.display.get_width()//2+self.in_case.decalage[0]*2+100+x,self.cordo()[1]-self.in_case.display.get_height()//2+self.in_case.decalage[1]-50+y))
            else:
                screen.blit(self.in_case.display,(self.cordo()[0]-self.in_case.display.get_width()//2+self.in_case.decalage[0]+100+x,self.cordo()[1]-self.in_case.display.get_height()//2+self.in_case.decalage[1]-50+y))
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

    """Cette fonction va me rendre l ensemble des neighbours touches par le sort"""
    def select_neighbour(self, list_case,k=0):
        # if self.in_case != None:
        for x in list_case:
            x.is_select = False
            for i in range(-1-k,2+k):
                for j in range(-1-k,2+k):
                    if x.j+j == self.j and x.i+i == self.i:
                        x.select(True)
                    
    def select_diag(self,list_case):
        for x in list_case:
            for i in range(-1,2):
                if x.j+i == self.j and x.i+i == self.i:
                    x.select(True)
                if x.j+i == self.j and x.i-i == self.i:
                    x.select(True)

    "Initialement cette fonction donne un range de 1"
    def print_effect(self,list_case,j=0,i=0):
        for x in list_case:
            x.select(False)
            if x.j+j == self.j and x.i+i== self.i:
                x.select_neighbour(list_case)

    def checkIfSelected(self):
        if self.is_select:
            screen.blit(case_select, self.cordo())
    
    def select_neighbour_inverse(self, list_case,k):
        # if self.in_case != None:
        for x in list_case:
            x.is_select = False
            for i in range(-1-k,2+k):
                for j in range(-1-k,2+k):
                    if x.j+j == self.j and x.i+i == self.i:
                        x.select(False)
                        
    def print_effect_inverse(self,list_case,k=0,m=0):
        for x in list_case:
            x.select(False)
            if x.j-1-k == self.j and x.i+1+k == self.i:
                x.select_neighbour_inverse(list_case,m)

    def numero_case(self,list_case):
        k = 0
        while k<len(list_case):
            if (list_case[k].i == self.i and list_case[k].j == self.j):
                return k
            k += 1

    def effect_neighbour(self, list_case,k,liste):
        # if self.in_case != None:
        for x in list_case:
            x.is_select = False
            for i in range(-1-k,2+k):
                for j in range(-1-k,2+k):
                    if (x.j+j == self.j and x.i+i == self.i and x.in_case != None):
                        liste.append(x.in_case)
        

    def get_effect(self,list_case,k=0,m=0):
        liste_hit = []
        for x in list_case:
            x.select(False)
            if x.j-1-k == self.j and x.i+1+k == self.i:
                x.effect_neighbour(list_case,m,liste_hit)
        
        return liste_hit

    