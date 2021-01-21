import pygame
from interface import Interface
from random import randrange
from settings.screen import screen
pygame.init()
interface=Interface()
running=True
interface.generer()
interface.basic_affichage()
while running:
    interface.perso.xp+=1
    interface.perso.update_hp_bar(screen)
    interface.perso.levelupchange()
    n=pygame.time.get_ticks()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN:
            interface.perso.quick_spell()
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running=False
                pygame.quit()
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()