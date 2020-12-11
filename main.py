import pygame
from interface import fighter
from interface import Interface
from random import randrange
pygame.init()
interface=Interface()
running=True
interface.generer()
interface.basic_affichage()
while running:
    fighter.xp+=1
    fighter.levelupchange()
    n=pygame.time.get_ticks()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONUP:
            interface.affichage()
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()