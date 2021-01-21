from monster import Monster
import random
import pickle
import pygame
import settings.load_img
from fonction import load_map,load_inv
from inventory import Inventaire,Shop,key
from settings.color import BURGUNDY,BLACK
from monster import Monster
from custum_map_ import list_entity_animation,list_npc
from settings.load_img import grass,demon_1_animation,demon_animation,squelton_animation,wizard_animation,dark_wizard_animation,pixel_red,etagere,end_game,road,wall,void,tree,fence_1,fence_2,chair,etagere_2,chair_2,chair_3,chest,table,rune_1,rune

import json
dict_img_npc = dict()

list_img_monstre = [list_entity_animation[0],list_entity_animation[1],list_entity_animation[2],list_entity_animation[3],list_entity_animation[4]]
list_animation_monstre = [demon_1_animation,demon_animation,squelton_animation,wizard_animation,dark_wizard_animation]
list_decalage_monstre = [[0,0],[0,0],[-30,-30],[-30,-30],[70,20]]
list_size_monstre = [(500,400),(500,400),(300,300),(300,300),(600,500)]

dict_img_npc['1']= list_npc[0]
dict_img_npc['2']= list_npc[1]
dict_img_npc['3']= list_npc[2]
dict_img_npc['4']= list_npc[3]
dict_img_npc['5']= list_npc[4]


donjon =  [json.loads(line) for line in open('donjon.json', 'r')]

class Map():
    def __init__(self,path,path_deco,path_monstre,list_static_entity,cubesize=190):
        self.path = path
        self.path_deco = path_deco
        self.path_monster = path_monstre
        self.map_decoration = load_map(path_deco,reverse=True)
        self.all_monstre = [json.loads(line) for line in open(path_monstre, 'r')]
        self.all_shop = load_inv()
        self.collision = []
        self.collision_change_camera = []
        self.collision_entity = []
        self.tree_position = []
        self.collision_under_level = []
        self.change_camera_entity = []
        self.map = load_map(path,reverse=True)
        self.display = pygame.Surface((18000,10000))
        self.display_tree = pygame.Surface((18000,10000))
        self.cubesize = cubesize
        self.static_entity = list_static_entity
        self.collision_hupper_level = []
        self.list_monster = []
        self.list_shop = []
        self.dict_collision = dict()
        self.spawn_point = (0,0)
    def load_map(self):
        self.map = load_map(self.path,reverse=True)
        self.map_decoration = load_map(self.path_deco,reverse=True)
        self.collision = []
        self.collision_change_camera = []
        self.collision_entity = []
        self.tree_position = []
        self.change_camera_entity = []
    def init_map(self):
        self.display.fill(BURGUNDY)
        self.display.set_colorkey(BLACK)
        self.display_tree.set_colorkey(BLACK)
        self.print_ground()
        self.print_building()
        self.print_tree()
        self.init_monster()
        self.init_shop()
        self.dict_collision["change_camera_entity"] = self.change_camera_entity
        self.dict_collision["collision_entity"] = self.collision_entity
        self.dict_collision["collision"] = self.collision
        self.dict_collision["collision_change_camera"] = self.collision_change_camera
        self.dict_collision["collision_under_level"] = self.collision_under_level
        self.dict_collision["collision_hupper_level"] = self.collision_hupper_level

        #self.display.blit(self.display_tree,(0,0))
    def init_monster(self):
        self.list_monster = []
        for x in self.all_monstre:
            self.list_monster.append(Monster(x[0],x[1],list_img_monstre[x[2]-1],"",str(x[2]),size_collide_box=4,size=list_size_monstre[x[2]-1],animation_dict=list_animation_monstre[x[2]-1],decalage=list_decalage_monstre[x[2]-1]))
        for x in self.list_monster:
            inter_x = x.pos_x
            inter_y = x.pos_y
            x.pos_x,x.pos_y = (inter_y-inter_x)*190//2+9000,(inter_y+inter_x)*190//4
            x.init()
        for x in self.list_monster:
            x.set_group_monster(self.list_monster)

    """    for x in self.all_monstre:
            print(x[1])
            if len(x) !=0:
                self.list_monster.append(Monster(x[0],x[1],dict_img_monstre[str(x[2])],"",x[2],size_collide_box=4,size=dict_size_monstre[str(x[2])],animation_dict=dict_animation_monstre[x[2]],decalage=dict_decalage_monstre[str(x[2])]))
    """
    def init_shop(self):
        line=1
        self.list_shop = []
        for i in range(self.all_shop[0]):
            if self.all_shop[line+4] == int(self.path[10]):
                inv = Inventaire(7,5)
                for x in self.all_shop[line+3]:
                    if self.all_shop[line+3][x] != None:
                        inv.ajouteritems(key[self.all_shop[line+3][x]])
                inter_x = int(self.all_shop[line+1])
                inter_y = int(self.all_shop[line+2])
                x,y = (inter_y-inter_x)*190//2+9000,(inter_y+inter_x)*190//4
                self.list_shop.append(Shop(inv,x,y,list_npc[self.all_shop[line+4]],"Marc",'Seller',talking="Bienvenue dans mon magasin !",size_collide_box=2))
                self.list_shop[len(self.list_shop)-1].update_pos_collide()
                self.display.blit(self.list_shop[len(self.list_shop)-1].img,(self.list_shop[len(self.list_shop)-1].pos_x,self.list_shop[len(self.list_shop)-1].pos_y))
            line+=5
    def print_ground(self):
        i=0
        for layer in self.map:
            j=0
            for tile in layer:
                x = (j-i)*self.cubesize//2+9000
                y = (j+i)*self.cubesize//4
                if self.map[i][j] != None:
                    if self.map[i][j] == '1' or self.map[i][j] == '2' :
                        n = random.randint(1,5)
                        self.display.blit(grass['grass_' + str(n) + '.png'],(x,y))
                    if self.map[i][j] == '2' :
                        self.collision_change_camera.append(((j-i+1)*self.cubesize//2+9000,(j+i-1)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i)*self.cubesize//2+9000,(j+i-2)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i-1)*self.cubesize//2+9000,(j+i-1)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i+1)*self.cubesize//2+9000,(j+i-3)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i-1)*self.cubesize//2+9000,(j+i-3)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i)*self.cubesize//2+9000,(j+i-4)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i+1)*self.cubesize//2+9000,(j+i-5)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i)*self.cubesize//2+9000,(j+i-5)*self.cubesize//4))

                        self.collision.append((x,y))
                        self.tree_position.append((x,y))
                        self.display.blit(pixel_red,(((j-i-1)*self.cubesize//2+9000,(j+i+1)*self.cubesize//4)))
                    if self.map[i][j] == '5' :
                        self.display.blit(end_game,(x,y))
                        self.collision.append((x,y))
                        #display.blit(pixel_red,(x,y))
                    if self.map[i][j] == '3' or self.map[i][j] == '9' or self.map[i][j] == '7':
                        self.display.blit(grass['grass_' + str(1) + '.png'],(x,y))
                        self.collision.append((x,y))
                    if self.map[i][j] == '4':
                        self.display.blit(road,(x,y))
                    if self.map[i][j] == '6':
                        self.display.blit(grass['grass_' + str(1) + '.png'],(x,y))
                        self.collision_entity.append((x,y))
                    if self.map[i][j] == '8':
                        self.display.blit(grass["grass_blue_1.png"],(x,y))
                    if self.map[i][j] == 'c':
                        n = random.randint(1,5)
                        self.display.blit(grass['grass_' + str(n) + '.png'],(x,y))
                        self.change_camera_entity.append((x,y))
                    if self.map[i][j] == 'a':
                        self.collision.append((x,y))
                        self.display.blit(wall,(x,y-100))
                    if self.map[i][j] == 'b':
                        self.display.blit(void,(x,y-100))
                    if self.map[i][j] == '1':
                        self.collision.append((x,y))
                        self.display.blit(void,(x,y))
                    if self.map[i][j] == '2':
                        self.display.blit(road,(x,y))
                    if self.map[i][j] == '3':
                        n = random.randint(1,5)
                        self.display.blit(grass['grass_red_' + str(n) + '.png'],(x,y))
                    if self.map[i][j] == '4':
                        n = random.randint(1,5)
                        self.display.blit(grass['grass_' + str(n) + '.png'],(x,y))
                    if self.map[i][j] == '5':
                        n = random.randint(1,5)
                        self.display.blit(grass['grass_light_green_' + str(n) + '.png'],(x,y))
                    if self.map[i][j] == '6':
                        n = random.randint(1,5)
                        self.display.blit(grass['grass_yellow_' + str(n) + '.png'],(x,y))
                    if self.map[i][j] == '7':
                        n = random.randint(1,5)
                        self.display.blit(grass['grass_blue_' + str(n) + '.png'],(x,y))
                    
                j+=1
            i+=1
        i=0
    def print_tree(self):
        i=0
        for layer in self.map:
            j=0
            for tile in layer:
                x = (j-i)*self.cubesize//2+9000
                y = (j+i)*self.cubesize//4
                if(0<=i<=3 and 15<=j<=3):
                    self.map_decoration[i][j] = '8'
                if self.map_decoration[i][j] != None:
                    if self.map_decoration[i][j] == 'a' :
                        self.collision_change_camera.append(((j-i+1)*self.cubesize//2+9000,(j+i-1)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i)*self.cubesize//2+9000,(j+i-2)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i-1)*self.cubesize//2+9000,(j+i-1)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i+1)*self.cubesize//2+9000,(j+i-3)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i-1)*self.cubesize//2+9000,(j+i-3)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i)*self.cubesize//2+9000,(j+i-4)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i+1)*self.cubesize//2+9000,(j+i-5)*self.cubesize//4))
                        self.collision_change_camera.append(((j-i)*self.cubesize//2+9000,(j+i-5)*self.cubesize//4))
                        self.collision.append((x,y))
                        self.tree_position.append((x,y))
                        n = random.randint(1,10)
                        self.display_tree.blit(tree["tree_" + str(n) + ".png"],(x,y-250))
                        self.display.blit(tree["tree_" + str(n) + ".png"],(x,y-250))
                    if self.map_decoration[i][j] == 'b':
                        self.collision.append((x,y))
                        self.collision.append(((j-i+1)*self.cubesize//2+9000,(j+i+1)*self.cubesize//4))
                        self.display_tree.blit(fence_1,(x,y-50))
                        self.display.blit(fence_1,(x,y-50))
                    if self.map_decoration[i][j] == 'c':
                        self.collision.append((x,y))
                        self.collision.append(((j-i-1)*self.cubesize//2+9000,(j+i+1)*self.cubesize//4))
                        self.display_tree.blit(fence_2,(x,y-50))
                        self.display.blit(fence_2,(x,y-50))
                    if self.map_decoration[i][j] == 'd':
                        self.collision.append((x,y))
                        self.display.blit(wall,(x,y-100))
                    if self.map_decoration[i][j] == 'e':
                        self.collision.append((x,y))
                        self.display.blit(chair,(x,y-100))
                    if self.map_decoration[i][j] == 'f':
                        self.collision.append((x,y))
                        self.display.blit(etagere,(x,y-200)) 
                    if self.map_decoration[i][j] == 'g':
                        self.collision.append((x,y))
                        self.display.blit(etagere_2,(x,y-200)) 
                    if self.map_decoration[i][j] == 'h':
                        self.collision.append((x,y))
                        self.display.blit(chair_2,(x,y-100)) 
                    if self.map_decoration[i][j] == 'i':
                        self.collision.append((x,y))
                        self.display.blit(chair_3,(x,y-100)) 
                    if self.map_decoration[i][j] == 'j':
                        self.collision.append((x,y))
                        self.display.blit(chest,(x+50,y)) 
                    if self.map_decoration[i][j] == 'k':
                        self.collision.append((x,y))
                        self.display.blit(table,(x,y)) 
                    if self.map_decoration[i][j] == '8':
                        
                        self.collision_under_level.append((x,y))
                        self.display.blit(pygame.transform.scale(rune_1,(190,95)),(x,y))
                    if self.map_decoration[i][j] == '9':
                        self.collision_hupper_level.append((x,y))
                        self.spawn_point = (x,y)
                        self.display.blit(pygame.transform.scale(rune,(190,95)),(x,y))
                j+=1
            i+=1
        i=0
    def print_building(self):
        for i in range(len(self.static_entity)):
            self.display.blit(self.static_entity[i].display,(self.static_entity[i].pos_x,self.static_entity[i].pos_y))
