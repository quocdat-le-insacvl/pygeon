import pygame
from time import clock
from interface import Interface
pygame.init()
interface=Interface()

running=True

while running:
    interface.basic_affichage()
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1 :
            interface.animation_event(event)
        if event.type == pygame.QUIT:
            running=False
            pygame.quit()

                    




