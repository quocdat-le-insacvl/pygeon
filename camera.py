import pygame
from perso import Personnage
class Camera():
    def __init__(self,perso,piece):
        self.center_x,self.center_y =0,0
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.player = perso.perso
        self.perso = perso
        self.piece = piece
        self.display_piece = pygame.Surface((2,2))
    def actualiser(self,perso):
        self.perso = perso
        self.center_x = -perso.X+900
        self.center_y = -perso.Y+400
        

    def afficher(self,display):
        self.screen.fill((0,0,0))
        self.screen.blit(self.display_piece,(self.center_x,self.center_y))
        self.screen.blit(self.perso.perso,(self.perso.X+self.center_x,self.perso.Y+self.center_y))
        a =self.piece.update_graph(self.perso)
        for meubles_images in a :
            self.screen.blit(meubles_images[0],(meubles_images[1][0] + self.center_x,meubles_images[1][1] + self.center_y))
            print("yo")
        pygame.display.update()
    def init(self,perso):
        self.center_x = -perso.X+900
        self.center_y = -perso.Y+400