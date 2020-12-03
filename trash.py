import pygame, sys,pickle,os
#import numpy
import math
import random
from pygame import mixer
from script import pack,player,Wikitem,playerbis,pack_bis
from pygame.locals import *
from settings.screen import LARGEUR, LONGUEUR, screen,WINDOWS_SIZE
from settings.police import Drifftype,ColderWeather,Rumbletumble,coeff,coeff1,coeff2,ColderWeather_small
from settings.load_img import *
from settings.color import *
from entity import list_entity
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
            image = pygame.image.load(path + i).convert_alpha()
            image.set_colorkey(LIGHT_GREY)
            yield (i,image) 
    def transform_image(self,walk,multi=1):
        for x in walk:
            walk[x] = pygame.transform.scale(walk[x],(multi*3*walk[x].get_width(),multi*3*walk[x].get_height()))
    def print_map(self,Map,display):
        cubesize=190
        grass = dict(self.image_loader('Addon/grass/'))
        display.fill(LIGHT_GREY)
        #arbre.set_colorkey(LIGHT_GREY)
        for x in grass:
            grass[x] = pygame.transform.scale(grass[x],(200,200))
        collision=[]
        collision_change_camera = []
        collision_entity = []
        tree_position = []
        i=0
        for layer in Map:
            j=0
            for tile in layer:
                x = (j-i)*cubesize//2+9000
                y = (j+i)*cubesize//4
                if Map[i][j] != None:
                    if Map[i][j] == '1' or Map[i][j] == '2' :
                        n = random.randint(1,5)
                        display.blit(grass['grass_' + str(2) + '.png'],(x,y))
                    if Map[i][j] == '2' :
                        collision_change_camera.append(((j-i+1)*cubesize//2+9000,(j+i-1)*cubesize//4))
                        collision_change_camera.append(((j-i)*cubesize//2+9000,(j+i-2)*cubesize//4))
                        collision_change_camera.append(((j-i-1)*cubesize//2+9000,(j+i-1)*cubesize//4))
                        collision_change_camera.append(((j-i+1)*cubesize//2+9000,(j+i-3)*cubesize//4))
                        collision_change_camera.append(((j-i-1)*cubesize//2+9000,(j+i-3)*cubesize//4))
                        collision_change_camera.append(((j-i)*cubesize//2+9000,(j+i-4)*cubesize//4))
                        collision.append((x,y))
                        tree_position.append((x,y))
                        display.blit(pixel_red,(((j-i-1)*cubesize//2+9000,(j+i+1)*cubesize//4)))
                    if Map[i][j] == '5' :
                        display.blit(end_game,(x,y))
                        collision.append((x,y))
                        #display.blit(pixel_red,(x,y))
                    if Map[i][j] == '3':
                        display.blit(grass['grass_' + str(1) + '.png'],(x,y))
                        collision.append((x,y))
                    if Map[i][j] == '4':
                        display.blit(road,(x,y))
                    if Map[i][j] == '6':
                        display.blit(grass['grass_' + str(1) + '.png'],(x,y))

                        collision_entity.append((x,y))
                j+=1    
            i+=1
        i=0
        return display,collision,collision_change_camera,tree_position,collision_entity
    def print_nature(self,Map,display,center_x,center_y,tree_position,all = True):
        cubesize=190
        i=0
        if all:
            for layer in Map:
                j=0
                for tile in layer:
                    x = (j-i)*cubesize//2+9000
                    y = (j+i)*cubesize//4
                    if Map[i][j] != None:
                        if Map[i][j] == '2' :
                            display.blit(arbre_2,(center_x+x,center_y+y-200))
                    j+=1    
                i+=1
            i=0
        else:
            for x in tree_position:
                display.blit(arbre_2,(center_x+x[0],center_y+x[1]-200))
        return display
    def print_entity(self,display,list_entity):
        for i in range(len(list_entity)):
            display.blit(list_entity[i].display,(list_entity[i].pos_x,list_entity[i].pos_y))
    def add_entity(self,entity,list_display_entity):
        entity.display.fill(LIGHT_GREY)
        entity.display.set_colorkey(LIGHT_GREY)
        entity.display.blit(entity.img,(0,0))
        list_display_entity.append(entity.display)
        return list_display_entity
    def Credit(self):
        
        walk_bottom =dict(self.image_loader('Addon/walk_bottom/'))
        self.transform_image(walk_bottom)
        walk_right = dict(self.image_loader('Addon/walk_right/'))
        self.transform_image(walk_right)
        walk_left = dict(self.image_loader('Addon/walk_left/'))
        self.transform_image(walk_left)
        walk_top = dict(self.image_loader('Addon/walk_top/'))
        self.transform_image(walk_top)

        demon_walk = dict(self.image_loader('Addon/demon_walk/'))
        self.transform_image(demon_walk,3)


        arbre.set_colorkey(LIGHT_GREY)

        player_x,player_y=9000,2000
        player_rect = pygame.Rect(player_x,player_y,walk_bottom['walk_bottom_' + str(1) +'.png'].get_width(),walk_bottom['walk_bottom_' + str(1) +'.png'].get_height())
        display_joueurs = pygame.Surface((walk_bottom['walk_bottom_' + str(1) +'.png'].get_width(),walk_bottom['walk_bottom_' + str(1) +'.png'].get_height()))
        display_joueurs.set_colorkey(LIGHT_GREY)

        n=2
        mouvement = [False,False,False,False]
        running = True

        Map = self.load_map(r"map.txt")
        display = pygame.Surface((18000,10000))
        display_with_nature = pygame.Surface((18000,10000))

        display_with_nature,collision,collision_change_camera,tree_position,collision_entity = self.print_map(Map,display_with_nature)
        display,collision,collision_change_camera,tree_position,collision_entity = self.print_map(Map,display)
        self.print_entity(display_with_nature,list_entity)
        display_with_nature = self.print_nature(Map,display_with_nature,0,0,tree_position)

        self.print_entity(display,list_entity)
        display_brouillard = pygame.Surface((1800,1050))
        display_brouillard.fill(LIGHT_GREY)
        display_brouillard.set_colorkey(LIGHT_GREY)

        
        display.set_colorkey(LIGHT_GREY)

        perso_img = walk_bottom['walk_bottom_' + str(1) +'.png']
        pieds = pygame.Surface((perso_img.get_width()-40,10))
        pieds.fill(RED)
        pieds_mask = pygame.mask.from_surface(pieds)
        g = True
        pixel_mask = pygame.mask.from_surface(pixel_red) 
        center_x,center_y = 0,0
        case_connue =[]
        frame = 0
        swap = False
        entity_near = False
        while running:
            screen.fill(LIGHT_GREY)
            
            if swap:
                screen.blit(display,(center_x,center_y))
                screen.blit(display_joueurs,(center_x+player_rect.x,center_y+player_rect.y))
                self.print_nature(Map,screen,center_x,center_y,tree_position,all=False)
            else:
                screen.blit(display_with_nature,(center_x,center_y))
                screen.blit(display_joueurs,(center_x+player_rect.x,center_y+player_rect.y))
                
            self.ajouter_case_connue(player_rect,case_connue)
            self.print_effect(player_rect,screen,case_connue,center_x,center_y)
            #screen.blit(display_entity,(center_x+tavern.pos_x,center_y+tavern.pos_y))
            #screen.blit(pieds,(center_x+player_rect.x+20,center_y+player_rect.y+perso_img.get_height()-15))
            #screen.blit(display_joueurs,(center_x+player_rect.x,center_y+player_rect.y))
            if entity_near:
                self.draw_text("Press I for interact",ColderWeather,WHITE,screen,500,500)
            list_entity[1] = self.moove_entity(list_entity[1],[-10,+5],collision,pieds_mask,player_rect,perso_img)
            

            screen.blit(pygame.transform.scale(display,(300,100)),(LONGUEUR-300,LARGEUR-200))
            screen.blit(pygame.transform.scale(display,(300,100)),(LONGUEUR-300,LARGEUR-200))
            self.draw_text(" player_x : %i,player_y : %i"%(player_rect.x,player_rect.y),ColderWeather,WHITE,screen,100,100)            
            if n > len(demon_walk)-1 :
                n=1
            if frame == 4 :
                n +=1
                frame = 0
            frame +=1
            center_x -= (player_rect.x + center_x -900)//20
            center_y -= (player_rect.y + center_y- 400) //20
            if mouvement[0]:
                player_rect,swap,entity_near = self.move_alternative(player_rect,[10,-5],collision,collision_change_camera,pieds_mask,perso_img,center_x,center_y,swap,collision_entity,entity_near)
                display_joueurs.fill(LIGHT_GREY)
                display_joueurs.blit(walk_top['walk_top_' + str(n) +'.png'],(0,0))
            elif mouvement[1]:
                player_rect,swap,entity_near = self.move_alternative(player_rect,[-10,+5],collision,collision_change_camera,pieds_mask,perso_img,center_x,center_y,swap,collision_entity,entity_near)
                display_joueurs.fill(LIGHT_GREY)
                display_joueurs.blit(walk_bottom['walk_bottom_' + str(n) +'.png'],(0,0))
            elif mouvement[2]:
                player_rect,swap,entity_near  = self.move_alternative(player_rect,[+10,+5],collision,collision_change_camera,pieds_mask,perso_img,center_x,center_y,swap,collision_entity,entity_near)
                display_joueurs.fill(LIGHT_GREY)
                display_joueurs.blit(walk_right['walk_right_' + str(n) + '.png'],(0,0))
            elif mouvement[3]:
                player_rect,swap,entity_near = self.move_alternative(player_rect,[-10,-5],collision,collision_change_camera,pieds_mask,perso_img,center_x,center_y,swap,collision_entity,entity_near)
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
                        interact = True
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
    def which_lane(self,pos_x,pos_y):
        return [math.trunc(1/(2*190)*(4*pos_y-2*(pos_x-9000))),math.trunc(1/(2*190)*(4*pos_y+2*(pos_x-9000)))]
    def move_alternative(self,rect,mouvement,collision,collision_change_camera,pieds_mask,perso_img,center_x,center_y,swap,collision_entity,entity_near):
        pixel_mask = pygame.mask.from_surface(pixel_red)
        swap = False
        entity_near = False
        for x in collision_entity:
            if pixel_mask.overlap(pieds_mask,((rect.x+mouvement[0]+10)-x[0],(rect.y+mouvement[1]+perso_img.get_height()-15)-x[1])):
                entity_near = True
        for x in collision_change_camera:
            if pixel_mask.overlap(pieds_mask,((rect.x+mouvement[0]+10)-x[0],(rect.y+mouvement[1]+perso_img.get_height()-15)-x[1])):
                swap = True
        for x in collision:
            if pixel_mask.overlap(pieds_mask,((rect.x+mouvement[0]+10)-x[0],(rect.y+mouvement[1]+perso_img.get_height()-15)-x[1])):
                return rect,swap,entity_near
        

        else:
            rect.x += mouvement[0]
            rect.y += mouvement[1]
            return rect,swap,entity_near
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
    def print_effect(self,rect,display,case_connue,center_x,center_y):
        #display.fill(LIGHT_GREY)
        ligne_colonne = self.which_lane(rect.x,+rect.y+135)
        for j in range(-13,13,1):
            for i in range(-13,13,1):
                if not case_connue.__contains__([ligne_colonne[0]+i,ligne_colonne[1]+j]) :
                   display.blit(pixel_red,(((ligne_colonne[1]+j-ligne_colonne[0]-i)*190//2+9000+center_x,(ligne_colonne[1]+j+ligne_colonne[0]+i)*190//4+center_y)))      
    def ajouter_case_connue(self,rect,case_connue):
        ligne_colonne = self.which_lane(rect.x,rect.y+135)
        for j in range(-5,5,1):
            for i in range(-5,5,1):
                if not case_connue.__contains__([ligne_colonne[0]+i,ligne_colonne[1]+j]) :
                   case_connue.append([ligne_colonne[0]+i,ligne_colonne[1]+j])
    def moove_entity(self,entity,mouvement,collision,pieds_mask,joueurs,perso_img):
        pixel_mask = pygame.mask.from_surface(pixel_red) 
        if collision.__contains__((entity.pos_x- pixel_red.get_width()//2+entity.img.get_width()//2,entity.pos_y-pixel_red.get_height()+entity.img.get_height())):
            collision.remove((entity.pos_x- pixel_red.get_width()//2+entity.img.get_width()//2,entity.pos_y-pixel_red.get_height()+entity.img.get_height()))
        if not pieds_mask.overlap(pixel_mask,((entity.pos_x- pixel_red.get_width()//2+entity.img.get_width()//2 + mouvement[0])-joueurs.x,entity.pos_y-pixel_red.get_height()+entity.img.get_height()+ mouvement[1]-(joueurs.y+130))):
            collision.append((entity.pos_x- pixel_red.get_width()//2+entity.img.get_width()//2+ mouvement[0],entity.pos_y-pixel_red.get_height()+entity.img.get_height()+ mouvement[1]))
            entity.pos_x += mouvement[0]
            entity.pos_y += mouvement[1]
            return entity
        else:
            #collision.remove((entity.pos_x+mouvement[0]+20,entity.pos_y+mouvement[1]+130))
            collision.append((entity.pos_x- pixel_red.get_width()//2+entity.img.get_width()//2,entity.pos_y-pixel_red.get_height()+entity.img.get_height()))
            return entity
       
        
        
        
        
        
        
        

        

game = Game()

game.Credit()