import pygame
from fighter import Fighter
from ennemie import Ennemie

fighter=Fighter()
ennemie=Ennemie()

class Interface(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((1500, 1000))
        self.background = pygame.image.load('assets/grass.jpg')


    def basic_affichage(self):
        pygame.display.set_caption("projet fighter")
        self.screen.blit(self.background, (0,-200))
        self.screen.blit(fighter.trans,(0,600))
        ennemie.animation(self.screen)
        fighter.animation(self.screen)
        pygame.display.flip()

    def animation_event(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1 :
            fighter.transf()