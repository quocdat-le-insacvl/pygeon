from personnage import Perso
from entity import Fog, Minimap
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
from script import list_mooving_entity,list_static_entity,entity_2
from fonction import *
from personnage import *
from seller_scripts import list_seller
pygame.init()
clock = pygame.time.Clock()
time_line = pygame.time.get_ticks()
""" Une chose intéréssant que je viens d'apprendre : Il faut utiliser toujours .convert() ou .conver_alpha() 
quand on load les images pour la question de performance
"""

class Case():
    def __init__(self, i, j):
        self.in_case = None
        self.display = pygame.Surface(
            (pixel_red.get_width(), pixel_red.get_height()))
        self.display.blit(case, (0, 0))
        self.display.set_colorkey(BLACK)
        self.i = i
        self.j = j
        self.is_select = False

    def print_contains(self):
        if self.in_case != None:
            #screen.blit(self.in_case.display,(self.cordo()[0]+self.in_case.display.get_width()//2,self.cordo()[1]-self.in_case.display.get_height()//2))
            screen.blit(self.in_case.display,(self.cordo()[0]-self.in_case.img.get_width()//2,self.cordo()[1]-self.in_case.display.get_height()+self.in_case.img.get_height()//2+self.in_case.decalage_display[1]))
    def cordo(self):
        return ((self.j-self.i)*(pixel_red.get_width()+45)//2+screen.get_width()//2-pixel_red.get_width()//2, (self.j+self.i)*(pixel_red.get_width()+45)//4-100)

    def select(self, is_select):
        if is_select:
            screen.blit(case_select, self.cordo())
            self.is_select = True
        else:
            self.display.blit(case, (0, 0))
            screen.blit(self.display, (0, 0))
            self.is_select = False

    def select_neighbour(self, list_case):
        # if self.in_case != None:
        for x in list_case:
            x.is_select = False
            if x.j == self.j and x.i == self.i - 1:
                x.select(True)
            if x.j == self.j and x.i == self.i + 1:
                x.select(True)
            if x.i == self.i and x.j == self.j - 1:
                x.select(True)
            if x.i == self.i and x.j == self.j + 1:
                x.select(True)
    # def print_sort(self,list_case):


class Map():
    def __init__(self,path,list_static_entity,cubesize=190):
        self.path = path
        self.collision = []
        self.collision_change_camera = []
        self.collision_entity = []
        self.tree_position = []
        self.change_camera_entity = []
        self.map = load_map(path)
        self.display = pygame.Surface((18000,10000))
        self.display_tree = pygame.Surface((18000,10000))
        self.cubesize = cubesize
        self.static_entity = list_static_entity
        self.mooving_entity = list_mooving_entity
        self.dict_collision = dict()
    def load_map(self):
        self.map = load_map(self.path)
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
        self.dict_collision["change_camera_entity"] = self.change_camera_entity
        self.dict_collision["collision_entity"] = self.collision_entity
        self.dict_collision["collision"] = self.collision
        self.dict_collision["collision_change_camera"] = self.collision_change_camera
        #self.display.blit(self.display_tree,(0,0))
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
                    if self.map[i][j] == 'd':
                        self.display.blit(road,(x,y))
                        #self.display.blit(comptoir,(x,y))
                    if self.map[i][j] == 'a':
                        self.collision.append((x,y))
                        self.display.blit(wall,(x,y-100))
                    if self.map[i][j] == 'b':
                        self.display.blit(void,(x,y-100))
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
                if self.map[i][j] != None:
                    if self.map[i][j] == '2' :
                        n = random.randint(1,10)
                        self.display_tree.blit(tree["tree_" + str(n) + ".png"],(x,y-250))
                        self.display.blit(tree["tree_" + str(n) + ".png"],(x,y-250))
                    if self.map[i][j] == '7':
                        #collision.append((x,y))
                        self.display_tree.blit(fence_1,(x,y-50))
                        self.display.blit(fence_1,(x,y-50))
                    if self.map[i][j] == '9':
                        self.display_tree.blit(fence_2,(x,y-50))
                        self.display.blit(fence_2,(x,y-50))
                j+=1
            i+=1
        i=0
    def print_building(self):
        for i in range(len(self.static_entity)):
            self.display.blit(self.static_entity[i].display,(self.static_entity[i].pos_x,self.static_entity[i].pos_y))
#create 
#HUD functions
def draw_player_health(screen,x ,y , percent):
    if percent < 0 :
        percent = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 40
    fill = percent * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if percent > 0.7:
        color = GREEN
    elif percent >0.4:
        color = YELLOW
    else:
        color = RED
    pygame.draw.rect(screen, color, fill_rect)
    pygame.draw.rect(screen, WHITE, outline_rect, 2)

       
class Game():
    def __init__(self,player,map):
        self.x = 0
        self.player = player
        self.map = map
        self.click = False #Click souris
        self.fog = Fog(self)
        self.zoom_map = False
        self.center_x, self.center_y = 0, 0
        self.list_mooving_entity = list_mooving_entity
        self.screen = screen
    

    def main_game(self):
        
        global time_line
        self.player.name = 'f'
        self.player.classe = 'l'
        center_x,center_y=0,0
        '''Set de toute les variables d'actions'''
        transition = pygame.Surface((screen.get_width(),screen.get_height()))
        transition.fill((0,0,0))
        interact = False
        pause_menu = False
        running = True
        for x in list_seller:
            x.update_interact()
            for y in x.interaction:
                self.map.dict_collision['collision_entity'].append(y)
            self.map.display.blit(x.img,(x.pos_x,x.pos_y))
        n= 1
        f=0
        g=0
        is_talking = False
        self.player.pos_x = 8680
        self.player.pos_y = 800
        ### Minimap
        self.minimap = Minimap(self, self.map.display)
        
        ###
        show_inventory = False
        show_characteresheet = False
        display_1 = pygame.Surface((1980,1080))
        display_1.set_colorkey(BLACK)
        draw_interact = True
        frame = 1
        self.player.add_game(self)
        
        while running:
            if pygame.time.get_ticks() > time_line:
                time_line += 160
                frame = (frame)%6 +1 

            # pygame.display.update()
            # clock.tick(60)    


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
                screen.blit(rune_1,(11000+center_x,3000+center_y))
                # Print animation player
                screen.blit(self.player.img,(center_x+self.player.pos_x,center_y+self.player.pos_y))
                screen.blit(self.map.display_tree,(center_x,center_y))
                # Print FOG
                screen.blit(self.fog.surface, (center_x, center_y),
                            special_flags=pygame.BLEND_MULT)
            else:
                # Print nature, map, tree ...
                screen.blit(self.map.display,(center_x,center_y))
                screen.blit(rune_1,(11000+center_x,3000+center_y))
                # Print animation player
                screen.blit(self.player.img,(center_x+self.player.pos_x,center_y+self.player.pos_y))
                # Print FOG
                screen.blit(self.fog.surface, (center_x, center_y),
                            special_flags=pygame.BLEND_MULT)
            if self.player.swap_entity:
                entity_re_print = self.player.find_nearest_entity(list_static_entity)
                screen.blit(entity_re_print.img,(entity_re_print.pos_x+center_x,entity_re_print.pos_y+center_y))
            
            
            '''Actualiser case interaction + animations'''
            
            #for x in list_mooving_entity:
            #     x.animate_map()
            #     x.update_interact()

            
            # f += 1
            # if f < 150:
            #     list_mooving_entity[0].move_entity([2,-1],self.map,self.player)
            #     list_mooving_entity[2].move_entity([2,-1],self.map,self.player)
            # elif f > 150:
            #     list_mooving_entity[0].move_entity([-2,1],self.map,self.player)
            #     list_mooving_entity[2].move_entity([-2,1],self.map,self.player)
            # if f == 300:
            #     f=0
            #for x in list_mooving_entity:
            #    x.animate_map(frame)
            print_mooving_entity(self, screen,list_mooving_entity,center_x,center_y)
            for entity in self.list_mooving_entity:
                if entity.name == "test_demon":
                    entity.pos_y += 1
                    entity.pos_x += 3
            #self.print_fog(player_rect,screen,case_connue,center_x,center_y)

            #screen.blit(player.mask_surface,(center_x+self.player.pos_x+20,center_y+self.player.pos_y+self.player.img.get_height()-15))

            '''Action si contact avec entité'''
            if self.player.entity_near:
                entity = self.player.find_nearest_entity(list_seller)
                if draw_interact: draw_text("Press I for interact %s"%entity.name,ColderWeather,WHITE,screen,500,500)
                if entity.type == "Monster":
                    list_monster = []
                    list_monster.append(entity)
                    self.print_combat_screen(list_monster)
                if interact:
                    draw_interact = False
                    is_talking = self.interact(entity,is_talking)
                    self.player.mouvement = [False,False,False,False]
            else:
                draw_interact = True
        
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
                    if event.key == K_l:
                        self.map = map_2
                        self.map.init_map()
                    if event.key == pygame.K_q:
                        self.player.press_q = True
                        
                if event.type == KEYUP:
                    if event.key == K_m:
                        self.zoom_map = False
                    if event.key == K_q:
                        self.player.press_q = False

            self.player.move_player(self.map.dict_collision)
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
            userInput = pygame.key.get_pressed()
            screen.blit(avatarImg, (450, 800))
            draw_player_health(screen, 500, 800, self.player.hp / self.player.hp_max)
            screen.blit(skillQ, (500, 750))
            screen.blit(skillW, (550, 750))
            screen.blit(skillE, (600, 750))
            draw_text("FPS: %i, x : %i , y : %i" % (clock.get_fps(), self.player.pos_x,
                                                    self.player.pos_y), ColderWeather, WHITE, screen, 100, 100)
            
            #### Skill
            if self.player.press_q:
                self.player.print_skill()

            
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
        i = 0
        for x in list_monstre:
            list_case[10].in_case = x
            i+=1
        self.player.transform_display_for_combat()
        list_case[59].in_case = self.player

        #VOIR TOUT LES MONSTRES
        list_case[0].in_case = list_mooving_entity[0]
        list_case[1].in_case = list_mooving_entity[1]
        list_case[2].in_case = list_mooving_entity[2]
        list_case[3].in_case = list_mooving_entity[3]
        list_case[4].in_case = list_mooving_entity[4]
        while running:
            mx, my = pygame.mouse.get_pos()
            screen.fill(LIGHT_GREY)
            screen.blit(fond, (0, 0))
            screen.blit(souris_surf, (mx, my))
            i = 0

            for x in list_case:
                screen.blit(x.display, x.cordo())
                if x.in_case != None and not x.is_select:
                    x.in_case.type_animation = "idle"
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
                load_game(self.click, self.player)
            if create_text_click('Quit', Drifftype, GREY, display, self.click, display.get_width()//2, display.get_height()//1.6):
                if Validation_screen("Voulez-vous quittez sans sauvegarder ?", display, self.click):
                    sys.exit()
            screen.blit(pygame.transform.scale(display, WINDOWS_SIZE), (0, 0))
            pygame.display.update()
            running, self.click = basic_checkevent(self.click)
        self.click = False
        """Affiche un menu pause classique"""

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

# player_direct = Perso(0,0,0,0,0,0,0,0,0)
# game = Game(player_direct)
# while True:
#     game.main_game()

map_1 = Map("map.txt",list_static_entity)
map_1.init_map()
map_2 = Map(r"tavern_1",[])
map_2.init_map()
game = Game(player,map_1)
game.main_game()
game.print_combat_screen([entity_2])
#game.main_game()
#running = True
#click = False
#while running:
#    screen.blit(map_1.display,(-8000,0))
#    pygame.display.update()
#    running,click= basic_checkevent(click)
#game.main_game()# Pour lancer la carte
#game.print_combat_screen([]) #pour lancer le plateau combat
