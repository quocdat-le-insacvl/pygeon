from piece import Piece
import pygame
import os
class Personnage():
    def __init__(self,screen):
        self.pos_x, self.pos_y = [815,45]
        self.perso = self.createImages("perso.png",colorkey=(255,255,255))
        print(self.perso.get_width())
        self.pieds_mask = pygame.mask.from_surface(pygame.Surface((self.perso.get_width()-30,10)))
        self.interact_range = (10,10)
        self.perso_screen = screen
        self.persos =  pygame.mask.from_surface(self.perso)
        self.rect_perso = pygame.Surface.get_bounding_rect(self.perso)
        self.velocity = 2
    
    def deplacerDroite(self):
        self.pos_x+=self.velocity
        
    def deplacerGauche(self):
        self.pos_x -=self.velocity
    def deplacerHaut(self):
        self.pos_y -=self.velocity
    def deplacerBas(self):
        self.pos_y+=self.velocity

    def afficher(self):
        #self.perso_screen.blit(self.perso,(self.pos_x,self.pos_y))
        self.rect_perso = pygame.Rect((self.pos_x,self.pos_y),(self.perso.get_width(),self.perso.get_height()))
        return self.perso
    def createImages(self,name,scale=True,colorkey=(0,0,0),forceScale=False):
        relative_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Donjon/imgs/")
        if name not in os.listdir(relative_path): 
            print("Image %s not in imgs/ directory" %name)
        elif name[-4:] != ".png" and name[-4:] != ".jpg":
            print("Image not a .png or a .jpg")
        else:
            image = pygame.image.load(os.path.join(relative_path,name))
            if image.get_width() >= 128 or image.get_height() >= 128 or forceScale:
                image = pygame.transform.scale(image,(32, 32))
            image.set_colorkey(colorkey)
            return image