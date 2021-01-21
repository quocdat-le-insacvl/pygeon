import pygame
from personnage import Perso
from fog import Fog
from minimap import Minimap
from fonction import print_mooving_entity
class Camera():

    def __init__(self,perso,piece,list_monster):
        self.center_x,self.center_y =0,0
        self.screen = pygame.display.set_mode((1800,1080))
        self.player = perso.img
        self.perso = perso
        self.piece = piece
        self.display_piece = pygame.Surface((2,2))
        self.fog = Fog(perso,self.piece.display)
        self.fog.init_fog_for_dungeon()
        self.list_monster = list_monster
        self.minimap = Minimap(self.piece.piece,self.fog,self.piece.display,list_monster,self.perso)
    

    def actualiser(self,perso):
        self.perso = perso

        self.center_x = -perso.pos_x+900
        self.center_y = -perso.pos_y+400

        self.minimap.player = perso
        self.minimap.map = self.piece.piece
        self.minimap.display_with_nature = self.piece.display
        self.minimap.fog=self.fog
        self.minimap.draw_minimap()

    def afficher(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.display_piece,(self.center_x,self.center_y))
        self.screen.blit(pygame.transform.scale(self.perso.img,(32,49)),(self.perso.pos_x+self.center_x,self.perso.pos_y+self.center_y))
        self.screen.blit(self.perso.donjon_mask.to_surface(),(self.perso.pos_x+self.center_x,self.perso.pos_y+self.center_y))
        print_mooving_entity(self.fog, self.screen,self.list_monster,self.center_x,self.center_y)
        for x in self.list_monster:
                x.type_animation = "walk"
                if x.mouvement[0] < 0 :
                    x.animate_map(flip=True,scale=(50,80))
                else:
                    x.animate_map(scale=(50,80))
                x.moove_patrouille(self.perso,self.list_monster)
        
        a =self.piece.update_graph(self.perso)
        for meubles_images in a :
            self.screen.blit(meubles_images[0],(meubles_images[1][0] + self.center_x,meubles_images[1][1] + self.center_y))
        self.fog.draw_fog_dungeon()
        self.screen.blit(self.fog.surface, (self.center_x, self.center_y),
                            special_flags=pygame.BLEND_MULT)
        self.minimap.draw_minimap()
        pygame.display.update()
    def init(self,perso):
        self.center_x = -perso.pos_x+900
        self.center_y = -perso.pos_y+400