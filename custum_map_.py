import pygame
import pygame
import json
from math import trunc
import pygame as pg
from pygame.locals import *
from fonction import *
from items import Wikitem
from settings.screen import *
from settings.color import *
from settings.load_img import *
from settings.police import *
from script import player
from fonction import *
from entity import Entity
from monster import Monster
from Donjon.donjon import *
from inventory import Inventaire
from seller_scripts import seller_1_img,seller_2_img,seller_3_img,seller_4_img,seller_5_img
center_x = 0
center_y = 0


key = list(Wikitem.keys())
all_items = Inventaire(18,16)
for x in key:
    if x.wpn_name != "Sort":
        all_items.ajouteritems(x)

click = False




TILESIZE = 48



GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (140, 140, 140)

pg.init()
clock = pg.time.Clock()
global collide_map
collide_map = pygame.transform.scale(collide_map,(TILESIZE*2,TILESIZE))
collide_map.set_colorkey(WHITE)
collide_map_mask = pygame.mask.from_surface(collide_map)
mouse_surface = pygame.Surface((1,1))
mouse_surface.fill(RED)
mouse_mask = pygame.mask.from_surface(mouse_surface)
road = pygame.transform.scale(road,(TILESIZE*2,TILESIZE))

path_pygeon = os.path.dirname(__file__)
path_addon = os.path.join(path_pygeon, 'Addon')
# GRASS
grass_1 = pygame.transform.scale(pygame.image.load(path.join(path_addon,"tile_grass_1.png")),(TILESIZE*2,TILESIZE))
grass_2 = pygame.transform.scale(pygame.image.load(path.join(path_addon,"tile_grass_2.png")),(TILESIZE*2,TILESIZE))
grass_3 = pygame.transform.scale(pygame.image.load(path.join(path_addon,"tile_grass_3.png")),(TILESIZE*2,TILESIZE))
grass_4 = pygame.transform.scale(pygame.image.load(path.join(path_addon,"tile_grass_4.png")),(TILESIZE*2,TILESIZE))
grass_5 = pygame.transform.scale(pygame.image.load(path.join(path_addon,"tile_grass_5.png")),(TILESIZE*2,TILESIZE))

list_block = [collide_map,road,grass_1,grass_2,grass_3,grass_4,grass_5]
copy_tree = tree.copy()
transform_image(copy_tree,0,TILESIZE*2,TILESIZE*2)
list_tree = [copy_tree["tree_1.png"]]
list_other_block = [fence_1,fence_2,wall,chair,etagere,etagere_2,chair_2,chair_3,chest,table]

dict_case = dict()
dict_entity = dict()
dict_case['1'] = collide_map
dict_case['2'] = road
dict_case['3'] = grass_1
dict_case['4'] = grass_2
dict_case['5'] = grass_3
dict_case['6'] = grass_4
dict_case['7'] = grass_5
dict_case['8'] = pygame.transform.scale(rune_1,(TILESIZE*2,TILESIZE))
dict_case['9'] = pygame.transform.scale(rune,(TILESIZE*2,TILESIZE))

dict_case['a'] = copy_tree["tree_1.png"]
dict_case['b'] = pygame.transform.scale(fence_1,(TILESIZE*2,TILESIZE*2))
dict_case['c'] = pygame.transform.scale(fence_2,(TILESIZE*2,TILESIZE*2))
dict_case['d'] = pygame.transform.scale(wall,(TILESIZE*2,TILESIZE*2))
dict_case['e'] = pygame.transform.scale(chair,(TILESIZE,TILESIZE*2))
dict_case['f'] = pygame.transform.scale(etagere,(TILESIZE,TILESIZE*2))
dict_case['g'] = pygame.transform.scale(etagere_2,(TILESIZE,TILESIZE*2))
dict_case['h'] = pygame.transform.scale(chair_2,(TILESIZE,TILESIZE*2))
dict_case['i'] = pygame.transform.scale(chair_3,(TILESIZE,TILESIZE*2))
dict_case['j'] = pygame.transform.scale(chest,(TILESIZE,TILESIZE*2))
dict_case['k'] = pygame.transform.scale(table,(TILESIZE,TILESIZE*2))
dict_case['l'] = grass_1


list_entity_animation = [demon_1_idle["idle_1.png"],demon_idle["idle_1.png"],squelton_idle["idle_1.png"],wizard_hide["idle_1.png"],dark_wizard_idle["idle_1.png"]]

list_npc = [seller_1_img,seller_2_img,seller_3_img,seller_4_img,seller_5_img]

list_entity = []


class Map_editor:
    def __init__(self, Taille_x, Taille_y,path_ground='map',path_deco='map_decoration',path_monstre='map_monstre'):
        self.taille_x = Taille_x
        self.taille_y = Taille_y
        self.LONGUEUR = Taille_x * TILESIZE
        self.LARGEUR = Taille_y * TILESIZE
        self.path_deco = path_deco 
        self.path = path_ground 
        self.path_monstre = path_monstre 
        self.walls = []
        self.map_ground = [[]]
        self.map_decoration = [[]]
        self.case_select = '1'
        self.case_collide = []
        self.cord_collide = []
        self.list_donjon = []
        self.display = pygame.Surface((max(Taille_x,Taille_y)*2*TILESIZE,(max(Taille_x,Taille_y)*2*TILESIZE)))
        self.display.fill(BURGUNDY)
        self.display.set_colorkey(BURGUNDY)
        self.camera_x = -self.display.get_width()//2 + screen.get_width()//2
        self.camera_y = -self.display.get_height()//2 + screen.get_height()//2
        self.running = True
        self.current_entity = None
        self.donjon_select = False
        self.current_tree = '0'
        self.other_block = '0'
        self.enable_to_print = True
        self.click = False
        self.list_monstre = []
        self.type_monstre = 1
        self.other_click = False
        self.continious_click = False
        self.house_select = False
        self.choose_npc = False
        self.num_level = 1
        self.number_create_level = 1
        self.type_npc = ""
        self.current_npc = None
        self.list_shop = []
        self.list_kill = []
        self.list_find = []
        self.list_npc = []
        self.reset = False
    def init_custom_map(self,update=False):
        self.LONGUEUR = self.taille_x * TILESIZE 
        self.LARGEUR = self.taille_y * TILESIZE 
        self.display = pygame.Surface((max(self.taille_x,self.taille_y)*2*TILESIZE,(max(self.taille_x,self.taille_y)*2*TILESIZE)))
        self.display.fill(BURGUNDY)
        self.display.set_colorkey(BURGUNDY)
        self.camera_x = -self.display.get_width()//2 + screen.get_width()//2
        self.camera_y = -self.display.get_height()//2 + screen.get_height()//2
        self.init_collid(update)
        self.init_cord()
        self.refresh()
    def create_inv(self,case):
        loot_inv = Inventaire(7,5)
        running = True
        while running:
            screen.fill(LIGHTGRAY)
            running,self.click = basic_checkevent(self.click)
            all_items.loot_inventory(0,0,18*65,0,loot_inv,print_info_on_mouse=True)
            if creation_img_text_click(img_next,"Continuer",ColderWeather,WHITE,screen,self.click,right=1):
                running = False
            pygame.display.update()
        
        self.list_shop.append([self.current_npc,self.taille_x-1-case[0],case[1],loot_inv,self.type_img_npc,self.num_level-1])
        self.current_npc = None
        self.type_npc = ""
    
    def print_on_the_grid(self):
        if self.click or self.continious_click:
            mx,my = pg.mouse.get_pos()
            mx_on_display = mx - self.camera_x
            my_on_display = my - self.camera_y
            i=0
            if self.enable_to_print:
                for x in self.cord_collide:
                    if collide_map_mask.overlap(mouse_mask,(mx_on_display-x[0],my_on_display-x[1])):
                        if self.type_npc != "":
                            if self.type_npc == "Shop":
                                self.create_inv(self.case_collide[i])

                        elif self.house_select:
                            self.house_select = False 
                            self.map_decoration[self.case_collide[i][0]][self.case_collide[i][1]] = '8'
                            self.save_map(self.path+ '_level_'+str(self.num_level)+'.txt',self.path_deco+ '_level_'+str(self.num_level)+ '.txt',self.path_monstre+ '_level_'+str(self.num_level))
                            self.list_donjon.append([self.taille_x-1-self.case_collide[i][0],self.case_collide[i][1],self.num_level,self.number_create_level])
                            self.init_custom_map()
                            self.num_level = self.number_create_level
                            self.map_decoration[self.case_collide[i][0]][self.case_collide[i][1]] = '9'
                            self.refresh()
                            self.save_map(self.path+ '_level_'+str(self.num_level)+'.txt',self.path_deco+ '_level_'+str(self.num_level)+ '.txt',self.path_monstre+ '_level_'+str(self.num_level))
                            '''self.path = self.path + 'level_' + str(self.num_level)
                            self.path_deco = self.path_deco +  'level_' + str(self.num_level)
                            self.path_monstre = self.path_monstre + 'level_' + str(self.num_level)'''

                        elif self.map_ground[self.case_collide[i][0]][self.case_collide[i][1]] != '8' and self.map_ground[self.case_collide[i][0]][self.case_collide[i][1]] != '9':
                            if self.current_entity != None:
                                self.list_monstre.append([self.taille_x-1-self.case_collide[i][0],self.case_collide[i][1],self.type_monstre])
                                #self.list_monstre.append(Monster(self.taille_x-1-self.case_collide[i][0],self.case_collide[i][1],pygame.transform.scale(self.current_entity,(200,200)),"Define",self.type_monstre,size_collide_box=4))
                                #list_entity.append(Entity(self.cord_collide[i][0],self.cord_collide[i][1],self.current_entity,"need to define","need to define"))
                                self.map_ground[self.case_collide[i][0]][self.case_collide[i][1]] = self.case_select 
                                self.current_entity = None
                            elif self.current_tree != '0' and self.case_select != '0':
                                self.display.blit(dict_case[self.case_select],self.cord_collide[i])
                                self.display.blit(dict_case[self.current_tree],(self.cord_collide[i][0]+TILESIZE//2,self.cord_collide[i][1]-TILESIZE//2))
                                self.map_ground[self.case_collide[i][0]][self.case_collide[i][1]] = self.case_select
                                self.map_decoration[self.case_collide[i][0]][self.case_collide[i][1]] = self.current_tree
                            elif self.other_block != '0':
                                self.display.blit(dict_case[self.other_block],(self.cord_collide[i][0],self.cord_collide[i][1]-TILESIZE//2))
                                self.map_decoration[self.case_collide[i][0]][self.case_collide[i][1]] = self.other_block
                            elif self.case_select != '0':
                                self.display.blit(dict_case[self.case_select],self.cord_collide[i])
                                self.map_ground[self.case_collide[i][0]][self.case_collide[i][1]] = self.case_select 
                            else:
                                self.map_ground[self.case_collide[i][0]][self.case_collide[i][1]] = self.case_select 
                                self.map_decoration[self.case_collide[i][0]][self.case_collide[i][1]] = self.current_tree 
                    i+=1   
    def draw_entity(self):
        for x in self.list_monstre:
            self.display.blit(pygame.transform.scale(list_entity_animation[x[2]-1],(2*TILESIZE,2*TILESIZE)),(int(standard_vec_into_iso(abs(x[0]-self.taille_x+1)*TILESIZE,x[1]*TILESIZE)[0]),int(standard_vec_into_iso(abs(x[0]-self.taille_x+1)*TILESIZE,x[1]*TILESIZE)[1]+self.display.get_height()//2-TILESIZE//2-TILESIZE)))
        for x in self.list_shop:
            self.display.blit(pygame.transform.scale(x[0],(2*TILESIZE,2*TILESIZE)),(int(standard_vec_into_iso(abs(x[1]-self.taille_x+1)*TILESIZE,x[2]*TILESIZE)[0]),int(standard_vec_into_iso(abs(x[1]-self.taille_x+1)*TILESIZE,x[2]*TILESIZE)[1]+self.display.get_height()//2-TILESIZE//2-TILESIZE)))
    def draw(self):
        screen.blit(self.display,(self.camera_x,self.camera_y))
    def init_collid(self,update=False):
        x,y=0,0
        i,j = 0,0
        if not update:
            self.map_ground = [[ '0' for i in range(self.taille_y)] for j in range(self.taille_x)]
            self.map_decoration = [[ '0' for i in range(self.taille_y)] for j in range(self.taille_x)]
        else:
            inter_ground = self.map_ground
            inter_decoration = self.map_decoration
            self.map_ground = [[ '0' for i in range(self.taille_y)] for j in range(self.taille_x)]
            self.map_decoration = [[ '0' for i in range(self.taille_y)] for j in range(self.taille_x)]

            if len(inter_ground[0]) < len(self.map_ground):
                for x in inter_ground:
                    j=0
                    for l in x:
                        self.map_ground[i][j] = inter_ground[i][j] 
                        self.map_decoration[i][j] = inter_decoration[i][j]
                        j+=1
                    i+=1
            else:
                i,j=0,0
                for x in self.map_ground:
                    j=0
                    for l in x:
                        self.map_ground[i][j] = inter_ground[i][j] 
                        self.map_decoration[i][j] = inter_decoration[i][j]
                        j+=1
                    i+=1
        self.case_collide = []
        self.cord_collide = []
        for x in range(self.taille_x):
            y = 0
            for y in range(self.taille_y):
                self.case_collide.append((x,y))
                self.cord_collide.append((x,y))
    def init_cord(self):
        for i in range(len(self.case_collide)):
            self.cord_collide[i] = (int(standard_vec_into_iso(self.case_collide[i][0]*TILESIZE,self.case_collide[i][1]*TILESIZE)[0]),int(standard_vec_into_iso(self.case_collide[i][0]*TILESIZE,self.case_collide[i][1]*TILESIZE)[1]+self.display.get_height()//2-TILESIZE//2))
    def refresh(self):
        i=0
        self.display.fill(BURGUNDY)
        self.draw_grid()
        for ligne in self.map_ground:
            for case in ligne:
                if case != '0':
                    self.display.blit(dict_case[case],self.cord_collide[i])
                i += 1
        i=0
        for ligne in self.map_decoration:
            for case in ligne:
                if case != '0':
                    self.display.blit(dict_case[case],(self.cord_collide[i][0]+TILESIZE//2,self.cord_collide[i][1]-TILESIZE//2))
                i +=1
    def draw_grid(self):
        for x in range(0, self.LONGUEUR+TILESIZE, TILESIZE):
            pg.draw.line(self.display, LIGHTGRAY,  (standard_vec_into_iso(x,0)[0],standard_vec_into_iso(x,0)[1]+self.display.get_width()//2),  (standard_vec_into_iso(x,self.LARGEUR)[0],standard_vec_into_iso(x,self.LARGEUR)[1]+self.display.get_height()//2))
        for y in range(0, self.LARGEUR+TILESIZE, TILESIZE):
            pg.draw.line(self.display, LIGHTGRAY,  (standard_vec_into_iso(0,y)[0],standard_vec_into_iso(0,y)[1]+self.display.get_width()//2),  (standard_vec_into_iso(self.LONGUEUR,y)[0],standard_vec_into_iso(self.LONGUEUR,y)[1]+self.display.get_height()//2))
        screen.blit(self.display,(self.camera_x,self.camera_y))
    def check_event(self):
        i,j=0,0
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.reset = True
                if event.key == pg.K_KP_PLUS:
                    self.taille_x +=1
                    self.taille_y +=1
                    self.init_custom_map(True)
                    for x in self.list_donjon:
                        if x[2] == self.num_level:
                            x[0]+=1
                    for a in self.list_monstre:
                        a[0] +=1
                    i,j=0,0
                    
                if event.key == pg.K_KP_MINUS:
                    self.taille_x -=1
                    self.taille_y -=1
                    self.init_custom_map(True)
                    for x in self.list_donjon:
                        if x[2] == self.num_level:
                            x[0]-=1
                        if x[0] < 0:
                            self.list_donjon.remove(x)
                    for a in self.list_monstre:
                        a[0] -=1
                        if a[0] < 0:
                            self.list_monstre.remove(a)
                if event.key == pg.K_r:
                    self.refresh()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button ==1:
                    self.click = True
                else:
                    self.other_click = True
            else:
                self.click = False
                self.other_click = False
            if event.type == KEYDOWN:
                if event.key == K_n:
                    self.continious_click = not self.continious_click
                if event.key == K_UP:
                    self.camera_y +=100
                elif event.key == K_DOWN:
                    self.camera_y -=100
                elif event.key == K_RIGHT:
                    self.camera_x -=100
                elif event.key == K_LEFT:
                    self.camera_x +=100              
    def save_map(self,path,path_deco,path_monstre,is_under=False):
        have_portal = False
        if self.num_level > 1:
            is_under = True
        fichier = open(path, "w")
        for x in self.map_decoration:
            for f in x:
                if f == '9':
                    have_portal = True
        if have_portal:
            pass
        else:
            if is_under:
                self.map_decoration[int(len(self.map_decoration[0])//2)][int(len(self.map_decoration[0])//2)] = '9'
        
        for x in self.map_ground:
                for f in x:
                    fichier.write(f)
                fichier.write("\n")
        fichier.close()

        fichier_deco =open(path_deco,"w")

        for x in self.map_decoration:
            for f in x:
                fichier_deco.write(f)
            fichier_deco.write("\n")

        fichier_deco.close()


        fichier = open(path_monstre+'.json',"w")

        for x in self.list_monstre:
            json.dump(x,fichier)
            fichier.write("\n")
        fichier.close()


        fichier = open("inventaire.json",'w')
        fichier.write(str(len(self.list_shop)))
        fichier.write("\n")

        for x in self.list_shop:
            fichier.write(str(x[5]))
            fichier.write("\n")
            fichier.write(str(x[1]))
            fichier.write("\n")
            fichier.write(str(x[2]))
            fichier.write("\n")
            json.dump(x[3].backpack, fichier)
            fichier.write("\n")
            fichier.write(str(x[4]))
            fichier.write("\n")
            
        fichier.close()

        fichier = open("donjon.json","w")
        for x in self.list_donjon:
            json.dump(x,fichier)
            fichier.write("\n")
        fichier.close
    def print_menu_editor(self):
        self.init_collid()
        self.init_cord()
        choose=False
        choose_quest = False
        color_1,color_2,color_3 = WHITE

        self.map_ground = load_map(self.path+ '_level_'+str(1) + '.txt')
        self.map_decoration = load_map(self.path_deco+ '_level_'+str(1)+'.txt')
        self.list_monstre = [json.loads(line) for line in open(self.path_monstre+ '_level_'+str(1)+'.json', 'r')]
        
        self.taille_x,self.taille_y = len(self.map_ground),len(self.map_ground[0])
        self.init_custom_map(True)
        self.num_level -=1
        #self.init_monster()
        self.refresh()

        
       
        while self.running:
            
            screen.fill(DARKGRAY)
            self.draw_grid()
            self.draw()
            self.draw_entity()
            x= screen.get_width()//2-img_inventaire.get_width()//2
            y =screen.get_height()//2-img_inventaire.get_height()//2
            # SAUVEGARDER
            draw_text("x : %i, y : %i"%(self.taille_x,self.taille_y),ColderWeather,WHITE,screen,500,500)
            if creation_img_text_click(img_next,"Sauvegarder",ColderWeather,WHITE,screen,self.other_click,right=1):
                self.save_map(self.path+ '_level_'+str(self.num_level)+'.txt',self.path_deco+ '_level_'+str(self.num_level)+ '.txt',self.path_monstre+ '_level_'+str(self.num_level))

            # CHOIX BLOCKS
            if not choose:
                if creation_img_text_click(img_next,"Choisr un bloc",ColderWeather,WHITE,screen,self.other_click,img_next.get_width()-80,img_next.get_height()//2):
                    choose = True
            else:  
                screen.blit(pygame.transform.scale(img_inventaire,(screen.get_width()//2,screen.get_height()//2)),(screen.get_width()//2-img_inventaire.get_width()//2,screen.get_height()//2-img_inventaire.get_height()//2))
                i=1
                if creation_img_text_click(pygame.transform.scale(img_inventaire,(TILESIZE,TILESIZE)),"RESET",ColderWeather,WHITE,screen,self.other_click,x+100,y+100):
                    self.current_tree = '0'
                    self.case_select = '0'
                    self.current_entity = None
                    choose = False
                
                for bloc in list_other_block:
                    if creation_img_text_click(pygame.transform.scale(bloc,(TILESIZE,TILESIZE)),"",ColderWeather,WHITE,screen,self.other_click,x+100*i,y+400):
                        self.other_block = chr(97+i)
                        self.current_tree = '0'
                        choose = False
                    i+=1
                i=1
                for img in list_block:
                    if creation_img_text_click(img,"",ColderWeather,WHITE,screen,self.other_click,x+100*i,y+200):
                        self.case_select = str(i)
                        self.other_block = '0'
                        self.current_tree = '0'
                        choose = False
                    i+=1
                i=1
                for tree in list_tree:
                    if creation_img_text_click(tree,'',ColderWeather,WHITE,screen,self.other_click,x+100*i,y+200+TILESIZE*2):
                        self.current_tree = chr(97+i-1)
                        self.other_block = '0'
                        choose = False
                    i+=1
            
            # CHOIX MONSTRE / CREATION QUETES

            if not choose_quest:
                if creation_img_text_click(img_next,"Donjon / Monstres",ColderWeather,WHITE,screen, self.other_click,screen.get_width()-img_next.get_width()//2,img_next.get_height()//2):
                    self.enable_to_print = False
                    pygame.time.wait(1)
                    choose_quest = True
            else: 
                screen.blit(pygame.transform.scale(img_inventaire,(screen.get_width()//2,screen.get_height()//2)),(screen.get_width()//2-img_inventaire.get_width()//2,screen.get_height()//2-img_inventaire.get_height()//2))
                i=1
                for monstre in list_entity_animation:
                    if creation_img_text_click(pygame.transform.scale(monstre,(2*TILESIZE,2*TILESIZE)),"",ColderWeather,WHITE,screen,self.other_click,x+100*i,y+200):
                        self.current_entity = pygame.transform.scale(monstre,(2*TILESIZE,2*TILESIZE))
                        self.current_tree = '0'
                        self.type_monstre = i 
                        #self.monstre_creator()
                        choose_quest = False
                    i+=1
                if creation_img_text_click(pygame.transform.scale(rune_1,(2*TILESIZE,TILESIZE)),"",ColderWeather,WHITE,screen,self.other_click,x+100,y+300):
                    self.donjon_select = True
                    self.case_select = '8'
                    #self.donjon_creator()
                    choose_quest = False

            if creation_img_text_click(img_next,"Continuer",ColderWeather,WHITE,screen,self.other_click,left=1):
                self.running = False
            else:
                self.check_event()
            self.enable_to_print = not choose_quest
            self.print_on_the_grid()
            
            if not self.house_select:
                if creation_img_text_click(img_next,"Create level",ColderWeather,WHITE,screen,self.other_click,screen.get_width()-img_next.get_width()//2,img_next.get_height()//2+200):
                    self.house_select = True
                    self.current_tree = '0'
                    self.other_block = '0'
                    self.number_create_level +=1
                        
            if self.num_level > 1 :
                if creation_img_text_click(img_next,"Go up level",ColderWeather,WHITE,screen,self.other_click,img_next.get_width()-80,img_next.get_height()//2+200):
                    self.map_ground = load_map(self.path+ '_level_'+str(self.num_level-1) + '.txt')
                    self.map_decoration = load_map(self.path_deco+ '_level_'+str(self.num_level-1)+'.txt')
                    self.list_monstre = [json.loads(line) for line in open(self.path_monstre+ '_level_'+str(self.num_level-1)+'.json', 'r')]
                    self.taille_x,self.taille_y = len(self.map_ground[0]),len(self.map_ground[0])
                    self.init_custom_map(True)
                    self.num_level -=1
                    #self.init_monster()
                    self.refresh()
                    self.other_click = False
            if self.num_level < self.number_create_level:
                if creation_img_text_click(img_next,"Go down level",ColderWeather,WHITE,screen,self.other_click,img_next.get_width()-80,img_next.get_height()//2+400):
                    self.map_ground = load_map(self.path+ '_level_'+str(self.num_level+1) + '.txt')
                    self.map_decoration = load_map(self.path_deco+ '_level_'+str(self.num_level+1)+'.txt')
                    self.list_monstre =  [json.loads(line) for line in open(self.path_monstre+ '_level_'+str(self.num_level+1)+'.json', 'r')]
                    self.taille_x,self.taille_y = len(self.map_ground[0]),len(self.map_ground[0])
                    self.init_custom_map(True)
                    self.num_level +=1
                    #self.init_monster()
                    self.refresh()
                    self.other_click = False
            
            if not self.choose_npc:
                if creation_img_text_click(img_next,"NPC",ColderWeather,WHITE,screen,self.other_click,img_next.get_width()//2,img_next.get_height()//2+600):
                    self.choose_npc = True
                    
            else:  
                screen.blit(pygame.transform.scale(img_inventaire,(screen.get_width()//2,screen.get_height()//2)),(screen.get_width()//2-img_inventaire.get_width()//2,screen.get_height()//2-img_inventaire.get_height()//2))
                i=1
                for npc in list_npc:
                    if creation_img_text_click(pygame.transform.scale(npc,(2*TILESIZE,2*TILESIZE)),"",ColderWeather,WHITE,screen,self.other_click,x+100*i,y+200):
                        self.current_npc = pygame.transform.scale(npc,(2*TILESIZE,2*TILESIZE))
                        self.type_img_npc = i
                        self.current_tree = '0'
                        self.other_block = '0'
                        #self.monstre_creator()
                        self.choose_npc = False
                    i+=1
                
                
                if create_text_click("Quest",ColderWeather,color_2,screen,self.other_click,x+300,y+300):
                    self.type_npc = "Quest"
                    color_2=RED
                    color_1=WHITE
                    color_3=WHITE
                if self.type_npc == "Quest" or self.type_npc == "Find" or self.type_npc == "Kill":
                    if create_text_click("Find item",ColderWeather,color_1,screen,self.other_click,x,y+400):
                        self.type_npc = "Find"
                        color_1 = RED
                        color_2 = WHITE
                        color_3 = WHITE
                    if create_text_click("Kill monster",ColderWeather,color_3,screen,self.other_click,x+500,y+400):
                        self.type_npc = "Kill"
                        color_3 = RED
                        color_2 = WHITE
                        color_1 = WHITE
                if self.type_npc != "Find" and self.type_npc != "Kill":
                    if create_text_click("NPC",ColderWeather,color_1,screen,self.other_click,x+100,y+300):
                        self.type_npc = "NPC"
                        color_1=RED
                        color_2=WHITE
                        color_3=WHITE
                    if create_text_click("Shop",ColderWeather,color_3,screen,self.other_click,x+500,y+300):
                        self.type_npc = "Shop"
                        color_3=RED
                        color_2=WHITE
                        color_1=WHITE
            if self.reset:
                self.choose_npc = False
                choose = False
                self.house_select = False
                choose_quest = False
            self.reset = False
            pg.display.update()
    def init_monster(self):
        inter_list = []
        for x in self.list_monstre:
            if len(x) !=0:
                inter_list.append(Monster(int(x[0]),int(x[1]),list_entity_animation[int(x[2])-1],"",x[2]))
        self.list_monstre = inter_list
    def donjon_creator(self):
        # Choisir Largueur
        display = pygame.Surface((1980,1000))
        running = True
        self.click = False
        etage,difficulte = 0,0
        first_blit = True
        while running:
            printbackgrounds(display)
            if self.donjon_select:
                self.case_select = '0'
                self.current_entity = None
            
            text_width, text_height = ColderWeather.size("Choisir une difficulte")
            draw_text('Choisir une difficulte', ColderWeather, GREY, display, display.get_width()//4 - text_width // 2.5, display.get_height()//6)
            bouton_difficulte = pygame.Rect(display.get_width()//4 - text_width // 2.5, display.get_height()//6+1.5*text_height,text_width, text_height)
            pygame.draw.rect(display,(150,150,150),bouton_difficulte,1)

            if bouton_click(bouton_difficulte,display,self.click):
                difficulte = self.checkclaviernum((display.get_width()//4 - text_width // 2.5),(display.get_height()//6+1.5*text_height),display,bouton_difficulte)

            draw_text(str(difficulte),ColderWeather,WHITE,display,display.get_width()//4 - text_width // 2.5, display.get_height()//6+1.5*text_height)

            text_width, text_height = ColderWeather.size("Choisir un nombre d etage")
            draw_text('Choisir un nombre d etage', ColderWeather, GREY, display, display.get_width()//4 - text_width // 2.5, display.get_height()//2)
            bouton_etage = pygame.Rect(display.get_width()//4 - text_width // 2.5, display.get_height()//2+1.5*text_height,text_width, text_height)
            pygame.draw.rect(display,(150,150,150),bouton_etage,1)

            if bouton_click(bouton_etage,display,self.click):
                etage = self.checkclaviernum((display.get_width()//4 - text_width // 2.5),(display.get_height()//2+1.5*text_height),display,bouton_etage)

            draw_text(str(etage),ColderWeather,WHITE,display,display.get_width()//4 - text_width // 2.5, display.get_height()//2+1.5*text_height)
            running,self.click = basic_checkevent(self.click)
            if etage != 0 and difficulte != 0:
                if creation_img_text_click(img_next,"Suivant",ColderWeather,WHITE,display,self.click,right=1):
                    self.list_donjon.append(Donjon(difficulte,screen,player,etage))
                    running = False
            
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))

            if not first_blit:pygame.display.update()
            first_blit = transition(1,screen.copy(),first_blit)  
    def checkclaviernum(self,x,y,display,rect):
        running = True
        mot = ''

        while running:
            display.fill(LIGHT_GREY,rect)
            draw_text(mot,ColderWeather,WHITE,display,x,y)

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN :
                    if event.key == K_ESCAPE or event.key == K_RETURN:
                        return int(mot)
                        running = False
                    if event.key == K_BACKSPACE:
                        mot = mot[:len(mot)-1]
                    if len(mot)<=4:
                        if event.key == K_0:
                            mot += '0'
                        if event.key == K_1:
                            mot += '1'
                        if event.key == K_2:
                            mot += '2'
                        if event.key == K_3:
                            mot += '3'
                        if event.key == K_4:
                            mot += '4'
                        if event.key == K_5:
                            mot += '5'
                        if event.key == K_6:
                            mot += '6'
                        if event.key == K_7:
                            mot += '7'
                        if event.key == K_8:
                            mot += '8'
                        if event.key == K_9:
                            mot += '9'
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))

            pygame.display.update()

def standard_vec_into_iso(x,y):
    x_iso = x + y 
    y_iso = -0.5*x + 0.5*y
    return (x_iso,y_iso)
def iso_vec_into_standard(x,y):
    x_stand = 0.5*x - y
    y_stand = 0.5*x + y
    return (x_stand,y_stand)
"""
mapp = Map_editor(200,200)
mapp.print_menu_editor()"""
