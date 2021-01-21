import pygame
from personnage import Perso
from fog import Fog
from minimap import Minimap
class Camera():

    def __init__(self,perso,piece):
        self.center_x,self.center_y =0,0
        self.screen = pygame.display.set_mode((1800,1080))
        self.player = perso.img
        self.perso = perso
        self.piece = piece
        self.display_piece = pygame.Surface((2,2))
        self.fog = Fog(perso,self.piece.display)
        self.fog.init_fog_for_dungeon()
        #self.minimap = Minimap(self.piece.piece,self.fog,self.display_piece,[],self.perso)
        self.minimap.draw_minimap()

    def actualiser(self,perso):
        self.perso = perso

        self.center_x = -perso.pos_x+900
        self.center_y = -perso.pos_y+400
        

    def afficher(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.display_piece,(self.center_x,self.center_y))
        self.screen.blit(pygame.transform.scale(self.perso.img,(32,49)),(self.perso.pos_x+self.center_x,self.perso.pos_y+self.center_y))
        self.screen.blit(self.perso.donjon_mask.to_surface(),(self.perso.pos_x+self.center_x,self.perso.pos_y+self.center_y))
        a =self.piece.update_graph(self.perso)
        for meubles_images in a :
            self.screen.blit(meubles_images[0],(meubles_images[1][0] + self.center_x,meubles_images[1][1] + self.center_y))
        self.fog.draw_fog_dungeon()
        self.screen.blit(self.fog.surface, (self.center_x, self.center_y),
                            special_flags=pygame.BLEND_MULT)
        self.screen.blit(self.minimap)
        pygame.display.update()
    def init(self,perso):
        self.center_x = -perso.pos_x+900
        self.center_y = -perso.pos_y+400