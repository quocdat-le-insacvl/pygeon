import pygame
import random

def bonus(attribut): #pour assigner a chaque attribut les pts bonus correspondants
        if attribut == 1:
            return -5
        else:
            b, i = -5, 1
            while i <= attribut:
                if i%2 == 0:
                    b += 1
                i += 1
            return b

def affichage_box(window,text,color,x,y,taille):
    font = pygame.font.Font('freesansbold.ttf', 30)
    text = font.render(text, True, (0,0,0))
    window.blit(text,[x,y])

def generate_randint(a,b):
    return random.randint(a,b)

