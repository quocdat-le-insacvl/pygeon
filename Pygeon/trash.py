import pygame, sys,pickle,os
import numpy
import math
import random
from pygame import mixer
from script import pack,player,Wikitem,playerbis,pack_bis,entity_1
from pygame.locals import *
from settings.screen import LARGEUR, LONGUEUR, screen,WINDOWS_SIZE
from settings.police import Drifftype,ColderWeather,Rumbletumble,coeff,coeff1,coeff2,ColderWeather_small
from settings.load_img import *
from settings.color import *

pygame.init()
clock = pygame.time.Clock()

class Game():
    def __init__(self):
        self.x = 0
    def load_map(self,path):
        f = open(path,'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        map = []
        for row in data:
            map.append(list(row))
        return map   
    def image_loader(self,path) -> str:
        for i in os.listdir(path):
            yield (i,pygame.image.load(path + i)) 
    def transform_image(self,walk):
        for x in walk:
            walk[x] = pygame.transform.scale(walk[x],(3*walk[x].get_width(),3*walk[x].get_height()))
    def collision_test(self,rect,tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
    def move(self,rect,movement,tiles):
        collision_types = False
        rect.x += movement[0]
        hit_list = self.collision_test(rect,tiles)
        for tile in hit_list:
            if movement[0] > 0 :
                rect.right = tile.left 
                collision_types = True
            elif movement[0] < 0 :
                rect.left = tile.right
                collision_types = True
        rect.y += movement[1]
        hit_list = self.collision_test(rect,tiles)
        for tile in hit_list:
            if movement[1] > 0 :
                rect.bottom = tile.top
                collision_types = True
            elif movement[1] < 0 :
                rect.top = tile.bottom
                collision_types = True
        return rect,collision_types
    def print_map(self,Map,display,center_x,center_y):
        cubesize=190
        grass = dict(self.image_loader('Pygeon/Addon/grass/'))
        display.fill(LIGHT_GREY)
        for x in grass:
            grass[x] = pygame.transform.scale(grass[x],(200,200))
        tiles_rect=[]
        i=0
        for layer in Map:
            j=0
            for tile in layer:
                x = (j-i)*cubesize//2+9300
                y = (j+i)*cubesize//4
                if Map[i][j] != None:
                    if Map[i][j] == '1' :
                        n = random.randint(1,5)
                        display.blit(grass['grass_' + str(n) + '.png'],(x-center_x,y-center_y))
                    if Map[i][j] == '2' :
                        display.blit(floor,(x-center_x,y-center_y))
                        display.blit(arbre,(x-center_x,y-center_y-100))
                        tiles_rect.append(pygame.Rect((x-center_x)+arbre.get_width()//3,(y-center_y)-arbre.get_height()//3,arbre.get_width()//2.5,arbre.get_height()//3))
                    if Map[i][j] == '5' :
                        display.blit(end_game,(x-center_x,y-center_y-50))
                        tiles_rect.append(pygame.Rect(x-center_x,y-center_y-40,30,30))
                j+=1    
            i+=1
        i=0
        return display,tiles_rect
    def print_entity(self,entity,center_x,center_y,tiles_rect):
        display_entity = pygame.Surface((entity.img.get_width(),entity.img.get_height()))
        display_entity.fill(LIGHT_GREY)
        display_entity.set_colorkey(LIGHT_GREY)
        display_entity.blit(entity.img,(0,0))
        screen.blit(display_entity,(center_x+entity.pos_x,center_y+entity.pos_y))
        tiles_rect.append(pygame.Rect(entity.pos_x,entity.pos_y,entity.img.get_width(),entity.img.get_height()//2))
        return tiles_rect
    def move_ramdom_entity(self,entity,tiles_rect,n):
        if n < 24 :
            pass
        else:
            self.move(entity.rect,[0,-1],tiles_rect)
            entity.pos_x = entity.rect.x
            entity.pos_y = entity.rect.y
        entity.update_center()
    def Credit(self):
        cubesize=190
        center_x,center_y=-8000,0

        Map = self.load_map(r"C:\Users\Antho\Desktop\Pygeon\pygeon\Pygeon\map.txt")
        self.draw_text('CHARGEMENT',ColderWeather,WHITE,screen,LONGUEUR//2,LARGEUR//2)
        
        
        display = pygame.Surface((19200,10800))
        walk_bottom =dict(self.image_loader('Pygeon/Addon/walk_bottom/'))
        self.transform_image(walk_bottom)
        walk_right = dict(self.image_loader('Pygeon/Addon/walk_right/'))
        self.transform_image(walk_right)
        walk_left = dict(self.image_loader('Pygeon/Addon/walk_left/'))
        self.transform_image(walk_left)
        walk_top = dict(self.image_loader('Pygeon/Addon/walk_top/'))
        
        self.transform_image(walk_top)

        player_x,player_y=LONGUEUR//2-walk_bottom['walk_bottom_' + str(1) +'.png'].get_width()//2-8000,LARGEUR//2-walk_bottom['walk_bottom_' + str(1) +'.png'].get_height()//2
        player_rect = pygame.Rect(player_x-center_x,player_y-center_y,walk_bottom['walk_bottom_' + str(1) +'.png'].get_width(),walk_bottom['walk_bottom_' + str(1) +'.png'].get_height())
        display_joueurs = pygame.Surface((walk_bottom['walk_bottom_' + str(1) +'.png'].get_width(),walk_bottom['walk_bottom_' + str(1) +'.png'].get_height()))
        display_joueurs.set_colorkey(LIGHT_GREY)
        center_x = 0
        afficher_inv = False
        n=2
        i,j=0,0
        mouvement = [False,False,False,False]
        running = True
        tiles_rect = []
        display,tiles_rect = self.print_map(Map,display,center_x,center_y)
        center_x = -8100
        center_y = -1000
        player_rect.x = 9000
        seller = pygame.image.load(r'C:\Users\Antho\Desktop\Pygeon\pygeon\seller_1.png')
        entity_1.img = pygame.transform.scale(seller,(3*seller.get_width(),3*seller.get_height()))
        entity_1.update_center()
        q=0
        while running:
            screen.fill(LIGHT_GREY)
            screen.blit(display,(center_x,center_y))
            screen.blit(display_joueurs,(center_x+player_rect.x,center_y+player_rect.y))

            if abs(entity_1.center[0] - player_rect.center[0]) < 100 and abs(entity_1.center[1]- player_rect.center[1]) < 100:
                if afficher_inv: self.shop_print(player,self.perso)
                afficher_inv = False
                self.draw_text("Center_x : %i, Center_y : %i , player_x : %i,player_y : %i"%(center_y,center_y,player_rect.x,player_rect.y),ColderWeather,WHITE,screen,100,100)

            if n > len(walk_bottom)-1 :
                n=1
            n +=1

            if self.creation_img_text_click(img_next,"UP",ColderWeather,WHITE,screen,LONGUEUR//2,0,Click=False) and -1/2*center_x + center_y < 3750 and 1/2*center_x + center_y < -4650:
                center_y +=25
            if self.creation_img_text_click(img_next,'Left',ColderWeather,WHITE,screen,0,LARGEUR//2,Click=False) and 1/2*center_x + center_y < -4650 and -1/2*center_x + center_y > -4000:
                center_x += 25
            if self.creation_img_text_click(img_next,'Right',ColderWeather,WHITE,screen,LONGUEUR,LARGEUR//2,Click=False) and -1/2*center_x + center_y < 3750  and -1/2*center_x - center_y < 12600:
                center_x -=25
            if self.creation_img_text_click(img_next,'Bottom',ColderWeather,WHITE,screen,LONGUEUR//2,LARGEUR,Click=False) and -1/2*center_x + center_y > -4000 and -1/2*center_x - center_y < 12600:
                center_y -= 25
 
                
            if mouvement[0]:
                player_rect, collision = self.move(player_rect,[0,-10],tiles_rect)
                display_joueurs.fill(LIGHT_GREY)
                display_joueurs.blit(walk_top['walk_top_' + str(n) +'.png'],(0,0))
            elif mouvement[1]:
                player_rect, collision = self.move(player_rect,[0,+10],tiles_rect)
                display_joueurs.fill(LIGHT_GREY)
                display_joueurs.blit(walk_bottom['walk_bottom_' + str(n) +'.png'],(0,0))
            elif mouvement[2]:
                player_rect, collision = self.move(player_rect,[+10,0],tiles_rect)
                display_joueurs.fill(LIGHT_GREY)
                display_joueurs.blit(walk_right['walk_right_' + str(n) + '.png'],(0,0))
            elif mouvement[3]:
                player_rect, collision = self.move(player_rect,[-10,0],tiles_rect)
                display_joueurs.fill(LIGHT_GREY)
                display_joueurs.blit(walk_left['walk_left_' + str(n) + '.png'],(0,0))
            else:
                display_joueurs.fill(LIGHT_GREY)
                display_joueurs.blit(walk_bottom['walk_bottom_' + str(1) +'.png'],(0,0))

                

            for event in pygame.event.get():
                if event.type == QUIT:
                        sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        mouvement[0] = True
                    if event.key == K_DOWN:
                        mouvement[1] = True
                    if event.key == K_RIGHT:
                        mouvement[2] = True
                    if event.key == K_LEFT:
                        mouvement[3] = True
                    if event.key == K_i:
                        afficher_inv = not afficher_inv
                if event.type == KEYUP:
                    if event.key == K_UP:
                        mouvement[0] = False
                    if event.key == K_DOWN:
                        mouvement[1] = False
                    if event.key == K_RIGHT:
                        mouvement[2] = False
                    if event.key == K_LEFT:
                        mouvement[3] = False  
            pygame.display.update()
            clock.tick(64)
    def creation_img_text_click(self,img,text,font,color,display,x=0,y=0,button=1,left=0,right=0,Click = True): 
        text_width, text_height = font.size(text)
        if img.get_width() < text_width:
            img = pygame.transform.scale(img,(text_width+50,img.get_height()))
        if(left):
            x = 0
            y = display.get_height()-img.get_height()
        elif(right):
            x = display.get_width()-img.get_width()
            y = display.get_height()-img.get_height()
        else:
            x = x-img.get_width()//2
            y = y-img.get_height()//2
        display.blit(img,(x,y))
        button_crea = pygame.Rect(x,y,img.get_width(),img.get_height())
        self.draw_text(text,font,color,display,x+img.get_width()//2-text_width//2,y+img.get_height()//2-img.get_height()//2)
        if Click :
            if self.bouton_click(button_crea,display):
                return True
        else:
            mx,my = pygame.mouse.get_pos()
            return button_crea.collidepoint((mx,my))
    def draw_text(self,text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    def bouton_click(self,bouton,display,constant_click = 0):
        # TEST : BOUTON EST CLIQUE ?
        mx, my = pygame.mouse.get_pos()
        mx = display.get_width() * mx / screen.get_width()
        my = display.get_height() * my / screen.get_height()
        return bouton.collidepoint((mx,my)) and self.click
game = Game()

game.Credit()