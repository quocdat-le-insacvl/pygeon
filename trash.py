from skill import Stealth
from personnage import Perso
from entity import ChatBox, Fog, Minimap
import pygame
import sys
import pickle
import os
#import numpy
import math
import random
from pygame import mixer
from pygame.time import Clock
from script import pack, player, Wikitem, playerbis, pack_bis
from pygame.locals import *
from settings.screen import *
from settings.police import Drifftype, ColderWeather, Rumbletumble, coeff, coeff1, coeff2, ColderWeather_small
from settings.load_img import *
from settings.color import *
from script import player_for_save,player_3,list_static_entity,player_2,playerbis,sorcerer,sorcerer_2,sorcerer_3
from fonction import *
from personnage import Perso_game
from seller_scripts import list_seller,seller_1_inv
from monster import Monster
from custum_map_ import list_entity_animation,list_npc
from inventory import Shop,Inventaire
from case import *
from combat import *
# from seller_scripts import list_seller
# from monster import Monster
# from custum_map_ import list_entity_animation
from skill import *

pygame.init()
clock = pygame.time.Clock()
time_line = pygame.time.get_ticks()
""" Une chose intéréssant que je viens d'apprendre : Il faut utiliser toujours .convert() ou .conver_alpha() 
quand on load les images pour la question de performance
"""
key = list(Wikitem.keys())
dict_img_monstre = dict()
dict_animation_monstre = dict()
dict_decalage_monstre = dict()
dict_size_monstre = dict()
dict_img_npc = dict()
dict_img_monstre['1']= list_entity_animation[0]
dict_img_monstre['2']= list_entity_animation[1]
dict_img_monstre['3']= list_entity_animation[2]
dict_img_monstre['4']= list_entity_animation[3]
dict_img_monstre['5']= list_entity_animation[4]

dict_img_npc['1']= list_npc[0]
dict_img_npc['2']= list_npc[1]
dict_img_npc['3']= list_npc[2]
dict_img_npc['4']= list_npc[3]
dict_img_npc['5']= list_npc[4]

dict_animation_monstre['1'] = demon_1_animation
dict_animation_monstre['2'] = demon_animation
dict_animation_monstre['3'] = squelton_animation
dict_animation_monstre['4'] = wizard_animation
dict_animation_monstre['5'] = dark_wizard_animation

dict_decalage_monstre['1'] = [0,0]
dict_decalage_monstre['2'] = [0,0]
dict_decalage_monstre['3'] = [-30,-30]
dict_decalage_monstre['4'] = [-30,-30]
dict_decalage_monstre['5'] = [70,20]

dict_size_monstre['1'] = (500,400)
dict_size_monstre['2'] = (500,400)
dict_size_monstre['3'] = (300,300)
dict_size_monstre['4'] = (300,300)
dict_size_monstre['5'] = (600,500)

donjon =  [json.loads(line) for line in open('donjon.json', 'r')]

class Map():
    def __init__(self,path,path_deco,path_monstre,list_static_entity,cubesize=190):
        self.path = path
        self.path_deco = path_deco
        self.path_monster = path_monstre
        self.map_decoration = load_map(path_deco,reverse=True)
        self.all_monstre = load_map(path_monstre,reverse=True)
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
        self.dict_collision = dict()
        
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
            if len(x) !=0:
                self.list_monster.append(Monster(int(x[0]),int(x[1]),dict_img_monstre[x[2]],"",x[2],size_collide_box=4,size=dict_size_monstre[x[2]],animation_dict=dict_animation_monstre[x[2]],decalage=dict_decalage_monstre[x[2]]))
    def init_shop(self):
        line=1
        self.list_shop = []
        for i in range(self.all_shop[0]):
            inv = Inventaire(7,5)
            for x in self.all_shop[line+2]:
                if self.all_shop[line+2][x] != None:
                    inv.ajouteritems(key[self.all_shop[line+2][x]])
            inter_x = int(self.all_shop[line])
            inter_y = int(self.all_shop[line+1])
            x,y = (inter_y-inter_x)*190//2+9000,(inter_y+inter_x)*190//4
            list_seller.append(Shop(inv,x,y,list_npc[self.all_shop[line+3]],"Marc",'Seller',talking="Bienvenue dans mon magasin !",size_collide_box=2))
            line+=4
    def print_ground(self):
        i=0
        for layer in self.map:
            j=0
            for tile in layer:
                x = (j-i)*self.cubesize//2+9000
                y = (j+i)*self.cubesize//4
                if self.map[i][j] != None:
                    '''if self.map[i][j] == '1' or self.map[i][j] == '2' :
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
                        self.display.blit(void,(x,y-100))'''
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
                        self.display.blit(pygame.transform.scale(rune,(190,95)),(x,y))
                j+=1
            i+=1
        i=0
    def print_building(self):
        for i in range(len(self.static_entity)):
            self.display.blit(self.static_entity[i].display,(self.static_entity[i].pos_x,self.static_entity[i].pos_y))

class Game():
    def __init__(self,player,map):
        self.x = 0
        self.player = player
        self.map = map
        self.click = False #Click souris
        self.fog = Fog(self)
        self.zoom_map = False
        self.center_x, self.center_y = 0, 0
        # self.list_mooving_entity = list_mooving_entity
        self.clock = clock
        self.list_mooving_entity = self.map.list_monster
        self.current_level = 1
        self.screen = screen
        self.chat_box = ChatBox(self)
        
    def main_game(self):
        global time_line
        self.player.name = 'gh'
        self.player.classe = 'l'
        center_x,center_y=0,0
        '''Set de toute les variables d'actions'''
        transition = pygame.Surface((screen.get_width(),screen.get_height()))
        transition.fill((0,0,0))
        interact = False
        pause_menu = False
        running = True
        
        for x in list_seller:
            x.update_pos_collide()
            self.map.display.blit(x.img,(x.pos_x,x.pos_y))
        n= 1
        f=0
        g=0
        is_talking = False
        self.player.pos_x = 8680
        self.player.pos_y = 800
        self.player.crew_mate[0].pos_x = 8680
        self.player.crew_mate[0].pos_y = 1000
        self.player.crew_mate[1].pos_x = 8680
        self.player.crew_mate[1].pos_y = 1100
        ### Minimap
        self.minimap = Minimap(self, self.map.display)
        for x in self.map.list_monster:
            inter_x = x.pos_x
            inter_y = x.pos_y
            x.pos_x,x.pos_y = (inter_y-inter_x)*190//2+9000,(inter_y+inter_x)*190//4
            x.init()
        for x in self.map.list_monster:
            x.set_group_monster(self.map.list_monster)
        ###
        show_inventory = False
        show_characteresheet = False
        display_1 = pygame.Surface((1980,1080))
        display_1.set_colorkey(BLACK)
        draw_interact = True
        frame = 1
        nb_crew = 0
        while running:
            if pygame.time.get_ticks() > time_line:
                time_line += 160
                frame = (frame)%6 +1 

            #""" If Press M : Zoom map === PAUSE"""
            
            if self.zoom_map:
                screen.fill(BLACK)
                self.minimap.zoom_minimap()
                draw_text("MAP", ColderWeather, RED, screen, screen.get_width() / 2 - 100, 50)
                draw_text("FPS: %i, x : %i , y : %i" % (clock.get_fps(), self.player.pos_x,
                                                    self.player.pos_y), ColderWeather, WHITE, screen, 100, 100)

                """Check event classique"""
                for event in pygame.event.get():
                    if event.type == KEYUP:
                        if event.key == K_m:
                            self.zoom_map = False
                pygame.display.update()
                clock.tick(64)
                continue
            
            screen.fill(LIGHT_GREY)
            """Changer l'affichage pour respecter vue joueurs"""
            if pause_menu:
                self.print_pause_menu()
                pause_menu = False
            if self.player.swap:
                 # Print nature, map, tree ...
                screen.blit(self.map.display,(center_x,center_y))
                # Print animation player
                screen.blit(self.player.img,(center_x+self.player.pos_x,center_y+self.player.pos_y))
                for x in self.player.crew_mate:
                    screen.blit(x.img,(center_x+x.pos_x,center_y+x.pos_y))
                screen.blit(self.map.display_tree,(center_x,center_y))
                # Print FOG
                screen.blit(self.fog.surface, (center_x, center_y),
                            special_flags=pygame.BLEND_MULT)
            else:
                # Print nature, map, tree ...
                screen.blit(self.map.display,(center_x,center_y))
                # Print animation player
                screen.blit(self.player.img,(center_x+self.player.pos_x,center_y+self.player.pos_y))
                for x in self.player.crew_mate:
                    screen.blit(x.img,(center_x+x.pos_x,center_y+x.pos_y))
                # Print FOG
                screen.blit(self.fog.surface, (center_x, center_y),
                            special_flags=pygame.BLEND_MULT)
            if self.player.swap_entity:
                entity_re_print = self.player.find_nearest_entity(list_static_entity)
                screen.blit(entity_re_print.img,(entity_re_print.pos_x+center_x,entity_re_print.pos_y+center_y))
            
            
            print_mooving_entity(self, screen,self.map.list_monster,center_x,center_y)
            for x in self.map.list_monster:
                x.type_animation = "walk"
                if x.mouvement[0] < 0 :
                    x.animate_map(flip=True)
                else:
                    x.animate_map()
                x.moove_patrouille(self.player,self.map.list_monster)
            #self.map.list_monster[0].moove_patrouille(self.player,self.map.list_monster)
            

            '''for entity in self.list_mooving_entity:
                if entity.name == "test_demon":
                    entity.pos_y += 1
                    entity.pos_x += 3'''
            #self.print_frog(player_rect,screen,case_connue,center_x,center_y)

            #screen.blit(player.mask_surface,(center_x+self.player.pos_x+20,center_y+self.player.pos_y+self.player.img.get_height()-15))

            '''Action si contact avec entité'''
            if self.player.entity_near:
                entity = self.player.find_nearest_entity(list_seller)
                if draw_interact: draw_text("Press I for interact %s"%entity.name,ColderWeather,WHITE,screen,500,500)
                if interact:
                    draw_interact = False
                    is_talking = self.interact(entity,is_talking)
                    self.player.mouvement = [False,False,False,False]
            else:
                draw_interact = True
            if self.player.change_level:
                if draw_interact: draw_text("Press I for go under",ColderWeather,WHITE,screen,500,500)
                if interact:
                    print(self.current_level)
                    nb = 0
                    for x in donjon:
                        if x[2] == self.current_level:
                            nb +=1
                    if nb == 1: 
                        self.map = list_map[x[3]-1]
                        self.current_level = x[3]
                    else:
                        for x in donjon:
                            print(self.current_level)
            if self.player.change_hupper_level:
                if draw_interact: draw_text("Press I for go hupper",ColderWeather,WHITE,screen,500,500)
                if interact:
                    print(self.current_level)
                    nb=0
                    for x in donjon:
                        if x[3] == self.current_level:
                            nb+=1
                    if nb == 1:
                        self.map = list_map[x[2]-1]
                        self.current_level = x[2]
                    
                    print(self.current_level)
            '''Set caméra / player pos pour sauvegarde'''

            center_x -= (self.player.pos_x + center_x - 900)//20
            center_y -= (self.player.pos_y + center_y - 540) //20
            
            self.center_x = center_x 
            self.center_y = center_y
            
            """ Draw Fog """
            self.fog.draw_fog()
            """ Draw minimap + Fog"""
            self.minimap.draw_minimap()

            """Check event classique"""
            for event in pygame.event.get():
                # handle chatbox
                chatting = self.chat_box.handle_event(event)
                if not chatting:
                    self.player.check_user(event)
                    if event.type == QUIT:
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_i:
                            interact = not interact
                        if event.key == K_m:
                            self.zoom_map = True
                        if event.key == K_j:
                            show_inventory = not show_inventory
                        """if event.key == K_ESCAPE:
                            self.map.load_map()
                            self.map.init_map()"""
                        if event.key == K_u:
                            show_characteresheet = not show_characteresheet
                        # Error !!! @Anthony
                        # if event.key == K_l:
                        #     self.map = map_2
                        #     self.map.init_map()
                        if event.key == K_v:
                            
                            self.player = self.player.crew_mate[0]
                            self.fog.player = self.player
                            nb_crew+=1
                            if nb_crew ==2:
                                nb_crew = 0
                            #pygame.image.save(self.fog.surface,'test_fog.png')
                        if event.key == K_ESCAPE:
                            self.print_pause_menu()
                            
                        # Handle skill cast
                        # if event.key == K_q:
                        #     self.player.skills[0].cast()
                        # if event.key == K_w:
                        #     self.player.skills[1].cast()
                        
                    if event.type == KEYUP:
                        if event.key == K_m:
                            self.zoom_map = False

            monstre = self.player.move_player(self.map.dict_collision,list_seller,self.map.list_monster)
            if monstre != None:
                f = Combat(self,monstre.group_monster)
                f.affichage()
                self.print_combat_screen(monstre.group_monster)



            self.player.animate_map(frame%2+1)
            """
            if g != 255:
                for x in range(255):
                    f+=0.008
                    transition.set_alpha(int(255-f))
                screen.blit(transition,(0,0))"""
            if show_inventory:
                self.player.print_equipement(100,100,500,500)
                #pack_bis.loot_inventory(1000,500,self.player.inventaire)
            if show_characteresheet:
                self.player.caracter_sheet()
                show_characteresheet = False
            
            draw_text("FPS: %i, x : %i , y : %i" % (clock.get_fps(),self.player.pos_x,self.player.pos_y
                                                    ,), ColderWeather, WHITE, screen, 100, 100)
            self.player.spell_bar()
            
            # update skill
            for skill in self.player.skills:
                skill.update()
            
            # update + draw chatbox
            self.chat_box.update()
            self.chat_box.draw()
            
            pygame.display.update()
            clock.tick(64)

    def print_combat_screen(self, list_monstre):
        running = True
        pixel_mask = pygame.mask.from_surface(pixel_red)
        souris_surf = pygame.Surface((1, 1))
        souris_surf.fill(RED)
        souris_mask = pygame.mask.from_surface(souris_surf)
        pixel_red.set_alpha(0)
        Map = [['a', 'a', 'a'], ['a', 'a', 'a']]
        case.set_colorkey(WHITE)
        display = pygame.Surface((screen.get_width(), screen.get_height()))
        display.set_colorkey(BLACK)
        l = load_map('map2.txt')
        case_select.set_alpha(100)
        list_case = []
        transition = pygame.Surface((screen.get_width(),screen.get_height()))
        transition.fill((0,0,0))
        f=0
        current_selec = None
        i, j = 0, 0
        for h in l:
            j = 0
            for g in h:
                if l[i][j] == 'w':
                    list_case.append(Case(i, j))
                j += 1
            i += 1
        i = 10
        for x in list_monstre:
            list_case[i].in_case = x
            i+=1
        self.player.transform_display_for_combat()
        '''
        list_case[59].in_case = self.player
        list_case[60].in_case = self.player.crew_mate[0]
        list_case[61].in_case = self.player.crew_mate[1]'''
        while running:
            mx, my = pygame.mouse.get_pos()
            screen.fill(LIGHT_GREY)
            screen.blit(fond, (0, 0))
            screen.blit(souris_surf, (mx, my))
            i = 0

            for x in list_case:
                screen.blit(x.display, x.cordo())
                if x.in_case != None and not x.is_select:
                    x.in_case.type_animation = "walk"
                if x.in_case != None and x.is_select:
                    x.in_case.type_animation = "idle"
                if x.in_case != None:
                    x.in_case.animate()

            for x in list_case:
                x.print_contains()
            i, j = 0, 0
            for h in l:
                j = 0
                for g in h:
                    if l[i][j] == 'w':
                        if pixel_mask.overlap(souris_mask, ((mx-((j-i)*(pixel_red.get_width()+45)//2+screen.get_width()//2-pixel_red.get_width()//2), my-((j+i)*(pixel_red.get_width()+45)//4-100)))):
                            if self.click:
                                for x in list_case:
                                    if x.i == i and x.j == j:
                                        if current_selec != None and current_selec.in_case != None:
                                            if x.is_select and x.in_case == None:
                                                x.in_case = current_selec.in_case
                                                x.in_case.type_animation = "walk"
                                                current_selec.in_case = None
                                        current_selec = x

                                        # x.select(True)
                                        # x.select_neighbour(list_case)
                                # print(i, j)
                    j += 1
                i += 1
            draw_text("i =%i j=%i %i" % (i, j, len(list_case)),
                      ColderWeather, WHITE, screen, 100, 100)

            draw_text("%i" % list_case[0].is_select,
                      ColderWeather, WHITE, screen, 500, 500)
            if current_selec != None:

                #current_selec.in_case = list_mooving_entity[0]
                # current_selec.print_contains()
                current_selec.select(True)
                current_selec.select_neighbour(list_case)


            if f != 255:
                for x in range(255):
                    f+=0.008
                    transition.set_alpha(int(255-f))
                screen.blit(transition,(0,0))


            pygame.display.update()
            running, self.click = basic_checkevent(self.click)
        """Affichage plateau + action souris
        principe de fonctionnement :
        Le principe de la carte est le suivant :
        Le jeu crée un object Case(i,j) a partir d'une map dans un text (qui contient des W)
        Ensuite la boucle for x in list_case permet d'imprimer toute les cases sur le screen
        la boucle d'après permet de voir si la souris (le mask) overlap la case c'est a dire si la souris collide avec la case, si elle overlap le programme cherche l'object Case(i,j) et utilise sa fonction select pour faire un affichage visuel de la case choisi"""

    def print_pause_menu(self):
        display = pygame.Surface((1980, 1000))
        display.set_colorkey(LIGHT_GREY)
        running = True
        while running:
            display.fill(LIGHT_GREY)
            printbackgrounds(display)
            if create_text_click("Resume", Drifftype, GREY, display, self.click, display.get_width()//2, display.get_height()//3):
                break
            if create_text_click('Sauvegarder', Drifftype, GREY, display, self.click, display.get_width()//2, display.get_height()//2.1):
                global player_for_save
                player_for_save.load_player(self.player)
                player_for_save,self.fog.surface = load_game(self.click, player_for_save,self.fog.surface)
                print(player_for_save.name)
                self.player.load_player(player_for_save)
            if create_text_click('Quit', Drifftype, GREY, display, self.click, display.get_width()//2, display.get_height()//1.6):
                if Validation_screen("Voulez-vous quittez sans sauvegarder ?", display, self.click):
                    sys.exit()
            screen.blit(pygame.transform.scale(display, WINDOWS_SIZE), (0, 0))
            pygame.display.update()
            running, self.click = basic_checkevent(self.click)
        self.click = False
        """Affiche un menu pause classique"""
    def load_fog(self,display_fog):
        self.fog.display = display_fog
    def interact(self,entity,is_talking):
        display_talk = pygame.Surface((1800,1080))
        display_talk.set_colorkey((0,0,0))
        if entity.type == "Seller":
            if entity.talking != None:
                if is_talking == True or Validation_screen(entity.talking,display_talk,self.click):
                    is_talking = True
                    entity.print_shop(self.player,self.click)
                screen.blit(display_talk,(0,0))
        return is_talking

#player_direct = Perso(0,0,0,0,0,0,0,0,0,[])
# game = Game(player_direct)
# while True:
#     game.main_game()
num = 1
list_map = []
while os.path.exists(os.path.join(path.dirname(__file__), 'map_level_'+str(num)+'.txt')):
    level = Map("map_level_"+str(num)+".txt","map_decoration_level_"+str(num)+".txt","map_monstre_level_"+str(num)+".txt",list_static_entity)
    level.init_map()
    list_map.append(level)
    num +=1

#map_1 = Map("map_level_1.txt","map_decoration_level_1.txt","map_monstre_level_1.txt",list_static_entity)
#map_2 = Map("map_level_2.txt","map_decoration_level_2.txt","map_monstre_level_2.txt",list_static_entity)

#map_1.init_map()
#map_2 = Map(r"tavern_1",[])
#map_2.init_map()

"""
player.crew_mate.append(player_2)
print(player_3.decalage[0])
print(player_2.decalage[0])

player.crew_mate.append(player_3)

player_2.crew_mate.append(player_3)
player_2.crew_mate.append(player)

player_3.crew_mate.append(player)
player_3.crew_mate.append(player_2)
"""

sorcerer.crew_mate.append(sorcerer_2)
sorcerer.crew_mate.append(sorcerer_3)

sorcerer_2.crew_mate.append(sorcerer_3)
sorcerer_2.crew_mate.append(sorcerer)

sorcerer_3.crew_mate.append(sorcerer)
sorcerer_3.crew_mate.append(sorcerer_2)



#map_1.init_map()
game = Game(sorcerer,list_map[0])
#c = Combat(game,[])
#c.affichage()
player.skills.append(Stealth(game))
player.skills.append(Perception(game))
game.main_game()
#running = True
#click = False
#while running:
# game.main_game()
#game.print_combat_screen([entity_2])

"""running = True
click = False
while running:
#    screen.blit(map_1.display,(-8000,0))
    print(player_3.name)
    player_5 = load_game(click,player_5)
    print(player_5.STR)
    pygame.display.update()
    running,click= basic_checkevent(click)"""
#game.main_game()# Pour lancer la carte
#game.print_combat_screen([]) #pour lancer le plateau combat
