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
from personnage import Perso_game
from case import *
from combat import *
pygame.init()
clock = pygame.time.Clock()

""" Une chose intéréssant que je viens d'apprendre : Il faut utiliser toujours .convert() ou .conver_alpha() 
quand on load les images pour la question de performance
"""

"""Anthony j'ai mis la classe Case dans un fichier tout seul qui s'apelle case.py car j en ai besoin et j ai importé le fichier la"""


class Map():
    def __init__(self,path,list_static_entity):
        self.path = path
        self.collision = []
        self.collision_change_camera = []
        self.collision_entity = []
        self.tree_position = []
        self.change_camera_entity = []
        self.map = load_map(path)
        self.display = pygame.Surface((18000,10000))
        self.display_tree = pygame.Surface((18000,10000))
        self.cubesize = 190
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

    def main_game(self):
        center_x,center_y=0,0
        '''Set de toute les variables d'actions'''
        transition = pygame.Surface((screen.get_width(),screen.get_height()))
        transition.fill((0,0,0))
        interact = False
        pause_menu = False
        running = True
        n= 1
        f=0
        g=0

        ### Minimap
        self.minimap = Minimap(self, self.map.display)
        ###
        show_inventory = False
        while running:
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
                screen.blit(self.player.display,(center_x+self.player.pos_x,center_y+self.player.pos_y))
                screen.blit(self.map.display_tree,(center_x,center_y))
                # Print FOG
                screen.blit(self.fog.surface, (center_x, center_y),
                            special_flags=pygame.BLEND_MULT)
            else:
                # Print nature, map, tree ...
                screen.blit(self.map.display,(center_x,center_y))
                screen.blit(rune_1,(11000+center_x,3000+center_y))
                # Print animation player
                screen.blit(self.player.display,(center_x+self.player.pos_x,center_y+self.player.pos_y))
                # Print FOG
                screen.blit(self.fog.surface, (center_x, center_y),
                            special_flags=pygame.BLEND_MULT)
            if self.player.swap_entity:
                entity_re_print = self.player.find_nearest_entity(list_static_entity)
                screen.blit(entity_re_print.display,(entity_re_print.pos_x+center_x,entity_re_print.pos_y+center_y))
            '''Actualiser case interaction + animations'''
            #self.player.animate_map()
            # for x in list_mooving_entity:
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
            
            #print_mooving_entity(screen,list_mooving_entity,center_x,center_y)
            

            #self.print_frog(player_rect,screen,case_connue,center_x,center_y)

            #screen.blit(player.mask_surface,(center_x+self.player.pos_x+20,center_y+self.player.pos_y+self.player.img.get_height()-15))

            '''Action si contact avec entité'''
            if self.player.entity_near:
                entity = self.player.find_nearest_entity(list_mooving_entity)
                draw_text("Press I for interact %s"%entity.name,ColderWeather,WHITE,screen,500,500)
                if entity.type == "Monster":
                    list_monster = []
                    list_monster.append(entity)
                    self.print_combat_screen(list_monster)
                if interact:
                    self.interact(entity)
                    self.player.mouvement = [False,False,False,False]
                    interact = False

            '''Set caméra / player pos pour sauvegarde'''
            center_x -= (self.player.pos_x + center_x - 900+self.player.img.get_width()//2)//20
            center_y -= (self.player.pos_y + center_y - 540+self.player.img.get_height()//2) //20
            
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
                        interact = True
                    if event.key == K_m:
                        self.zoom_map = True
                    if event.key == K_j:
                        show_inventory = not show_inventory
                    """if event.key == K_ESCAPE:
                        self.map.load_map()
                        self.map.init_map()"""

                if event.type == KEYUP:
                    if event.key == K_m:
                        self.zoom_map = False

            self.player.move_player(self.map.dict_collision)
            """
            if g != 255:
                for x in range(255):
                    f+=0.008
                    transition.set_alpha(int(255-f))
                screen.blit(transition,(0,0))"""
            if show_inventory:
                self.player.print_equipement(100,100)
                #pack_bis.loot_inventory(1000,500,self.player.inventaire)

            draw_text("FPS: %i, x : %i , y : %i" % (clock.get_fps(), self.player.pos_x,
                                                    self.player.pos_y), ColderWeather, WHITE, screen, 100, 100)
            
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

    def ligne_colonne(self, pos_x, pos_y):
        return [math.trunc(1/(2*190)*(4*pos_y-2*(pos_x-9000))), math.trunc(1/(2*190)*(4*pos_y+2*(pos_x-9000)))]
        """Retourne la ligne et la colonne en fonction de la position"""
    def print_frog(self,rect,display,case_connue,center_x,center_y):
        #display.fill(LIGHT_GREY)
        ligne_colonne = self.ligne_colonne(rect.x,+rect.y+135)
        for j in range(-5,5,1):
            for i in range(-5,5,1):
                if not case_connue.__contains__([ligne_colonne[0]+i,ligne_colonne[1]+j]) :
                   case_connue.append([ligne_colonne[0]+i,ligne_colonne[1]+j])
        j,i = 0,0
        for j in range(-13,13,1):
            for i in range(-13,13,1):
                if not case_connue.__contains__([ligne_colonne[0]+i,ligne_colonne[1]+j]) :
                   display.blit(pixel_red,(((ligne_colonne[1]+j-ligne_colonne[0]-i)*190//2+9000+center_x,(ligne_colonne[1]+j+ligne_colonne[0]+i)*190//4+center_y)))
        """Actualise les case_connues de joueur et affiche les cases map seulement sur les cases non connue de joueur
        le brouillard n'est actualiser que sur la surface de Screnne et pas sur tout la map"""
    def interact(self,entity):
        display_talk = pygame.Surface((1800,1080))
        display_talk.set_colorkey((0,0,0))
        if entity.type == "Seller":
            if entity.talking != None:
                if Validation_screen(entity.talking,display_talk,self.click):
                    entity.print_shop(self.player,self.click)
                screen.blit(display_talk,(0,0))


# player_direct = Perso(0,0,0,0,0,0,0,0,0)
# game = Game(player_direct)
# while True:
#     game.main_game()

map_1 = Map("map.txt",list_static_entity)
map_1.init_map()
game = Game(player,map_1)
c = Combat(game,[])
c.affichage()
#game.main_game()
#running = True
#click = False
#while running:
#    screen.blit(map_1.display,(-8000,0))
#    pygame.display.update()
#    running,click= basic_checkevent(click)
#game.main_game()# Pour lancer la carte
#game.print_combat_screen([]) #pour lancer le plateau combat
