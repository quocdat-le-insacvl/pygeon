import pygame
from interface import Interface
from random import randrange
pygame.init()
interface=Interface()
running=True
interface.generer()
interface.basic_affichage()
while running:
    interface.perso.xp+=1
    interface.perso.levelupchange()
    n=pygame.time.get_ticks()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONUP:
            interface.affichage()
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()