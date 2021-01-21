from skill import Stealth
from personnage import Perso
from entity import ChatBox
from fog import Fog
from minimap import Minimap
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
from Donjon.donjon import Donjon
from map import Map,donjon
from fog import Fog
#from combat import *
# from seller_scripts import list_seller
# from monster import Monster
# from custum_map_ import list_entity_animation
from skill import *
load_inv()
grass
pygame.init()
clock = pygame.time.Clock()
time_line = pygame.time.get_ticks()
""" Une chose intéréssant que je viens d'apprendre : Il faut utiliser toujours .convert() ou .conver_alpha() 
quand on load les images pour la question de performance
"""
key = list(Wikitem.keys())


class Game():
    def __init__(self,player,map,reload=False):
        self.x = 0
        self.player = player
        self.map = map
        self.click = False #Click souris
        self.fog = Fog(self.player,self.map.display)
        self.zoom_map = False
        self.center_x, self.center_y = 0, 0
        # self.list_mooving_entity = list_mooving_entity
        self.clock = clock
        self.list_mooving_entity = self.map.list_monster
        self.current_level = 1
        self.screen = screen
        self.chat_box = ChatBox(self)
        self.list_dungeon = dict()
        if not reload:
            for i in range(len(self.map.map_decoration)):
                if self.map.map_decoration[i] != None:
                    for j in range(len(self.map.map_decoration[i])):
                            
                            if self.map.map_decoration[i][j]=='8' or self.map.map_decoration[i][j]=='9':
                                donj = Donjon(2,self.screen,self.player)
                                donj.creationDonjon()
                                self.list_dungeon[(i,j)] = donj

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
        """
        for x in list_seller:
            x.update_pos_collide()
            self.map.display.blit(x.img,(x.pos_x,x.pos_y))
            """
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
        self.minimap = Minimap(self.map.map,self.fog,self.map.display_tree,self.list_mooving_entity,self.player)
    
        for x in donjon:
            x[0],x[1] = (x[1]-x[0])*190//2+9000,(x[1]+x[0])*190//4

       
        ###
        show_inventory = False
        show_characteresheet = False
        display_1 = pygame.Surface((1980,1080))
        display_1.set_colorkey(BLACK)
        draw_interact = True
        frame = 1
        nb_crew = 0
        self.player.know_map.append(self.current_level)
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
            
            
            print_mooving_entity(self.fog, screen,self.map.list_monster,center_x,center_y)
            for x in self.map.list_monster:
                x.type_animation = "walk"
                if x.mouvement[0] < 0 :
                    x.animate_map(flip=True)
                else:
                    x.animate_map()
                x.moove_patrouille(self.player,self.map.list_monster)
            #self.map.list_monster[0].moove_patrouille(self.player,self.map.list_monster)
            
            #self.print_frog(player_rect,screen,case_connue,center_x,center_y)

            #screen.blit(player.mask_surface,(center_x+self.player.pos_x+20,center_y+self.player.pos_y+self.player.img.get_height()-15))

            '''Action si contact avec entité'''
            
            if self.player.change_level:
                if draw_interact: draw_text("Press I for go under",ColderWeather,WHITE,screen,500,500)
                if interact:
                    pygame.image.save(self.fog.surface,'fog_'+str(self.current_level)+ '.png')
                    pos_joueur = (self.player.pos_x,self.player.pos_y)
                    coordDonjon = self.closest_dungeon(self.list_dungeon.keys(),self.player)
                    if coordDonjon !=-1:
                        
                        self.list_dungeon[coordDonjon].affichageDonjon()
                        self.list_dungeon[coordDonjon].runningDonjon()
                        
                    else: #ne devrait jamais arriver
                        print("WOLA G CHAUD\n")
                    
                    self.player.pos_x = pos_joueur[0]
                    self.player.pos_y = pos_joueur[1]
                    """print(donjon)
                    for x in donjon:
                        x_ = x[0]-self.player.pos_x
                        y = x[1] - self.player.pos_y

                        if abs(x[0]-self.player.pos_x) < 200 and abs(x[1]-self.player.pos_y) < 200 :
                            self.map = list_map[x[3]-1]
                            self.current_level = x[3]
                            self.fog = Fog(self)
                            if not self.player.know_map.__contains__(self.current_level):
                                self.player.know_map.append(self.current_level)
                            else:
                                self.fog.surface = pygame.image.load('fog_' + str(self.current_level)+ '.png')


                        if self.map.spawn_point != (0,0):
                            self.player.pos_x = self.map.spawn_point[0]
                            self.player.pos_y = self.map.spawn_point[1]"""
                    
                    interact = False





            if self.player.change_hupper_level:
                if draw_interact: draw_text("Press I for go hupper",ColderWeather,WHITE,screen,500,500)

                if interact:
                    nb=0
                    pygame.image.save(self.fog.surface,'fog_'+str(self.current_level)+ '.png')

                    for x in donjon:
                        if x[3] == self.current_level:
                            nb+=1
                    if nb == 1:
                        self.map = list_map[x[2]-1]
                        self.current_level = x[2]
                        self.fog = Fog(self)
                        if not self.player.know_map.__contains__(self.current_level):
                            self.player.know_map.append(self.current_level)
                        else:
                            self.fog.surface = pygame.image.load('fog_' + str(self.current_level)+ '.png')
                    interact = False
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

            monstre = self.player.move_player(self.map.dict_collision,self.map.list_shop,self.map.list_monster)
            if self.player.entity_near:
                if draw_interact: draw_text("Press I for interact %s"%monstre.name,ColderWeather,WHITE,screen,500,500)
                if interact:
                    draw_interact = False
                    is_talking = self.interact(monstre,is_talking)
                    self.player.mouvement = [False,False,False,False]
            else:
                draw_interact = True
            """
            if self.player.monstre_near and monstre != None:

                f = Combat(self,monstre.group_monster)
                f.affichage()
                if f.player.crew_mate[0].hp > 0 or f.player.crew_mate[1].hp > 0  or f.player.hp > 0:
                    for x in monstre.group_monster:
                        print(1)
                        self.map.list_monster.remove(x)
                monstre = None
            """
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
            """
            draw_text("FPS: %i, x : %i , y : %i" % (clock.get_fps(),self.player.pos_x,self.player.pos_y
                                                    ,), ColderWeather, WHITE, screen, 100, 100)
            draw_text("Donjon.x: %i, Donjon.y : %i ,x : %i, y : %i" % (len(self.map.list_monster),donjon[0][1],self.player.pos_x,self.player.pos_y), ColderWeather, WHITE, screen, 100, 100)
            """
            self.player.spell_bar()
            
            # update skill
            for skill in self.player.skills:
                skill.update()
            
            # update + draw chatbox
            self.chat_box.update()
            self.chat_box.draw()
            
            pygame.display.update()
            clock.tick(64)
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

    #retourne le donjon le plus proche du joueur
    #retrouve les donjons les plus chauds de chez toi
    #listposdungeon est un dictionnaire
    def closest_dungeon(self,listposdungeon_keys,perso):
        print("cest")
        min = -1
        coordRetour = -1
        for coord in listposdungeon_keys:
            x = (coord[1]-coord[0])*self.map.cubesize//2+9000
            y = (coord[1]+coord[0])*self.map.cubesize//4
            print(coord)
            dist = math.sqrt((x - perso.pos_x)**2 + (y - perso.pos_y)**2)
            if min == -1 or dist < min:
                min = dist
                coordRetour = coord
                print(coord)

        print(f"MIN : {min}\n")
        print("long")
        return coordRetour
        
"""
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
        Affichage plateau + action souris
        principe de fonctionnement :
        Le principe de la carte est le suivant :
        Le jeu crée un object Case(i,j) a partir d'une map dans un text (qui contient des W)
        Ensuite la boucle for x in list_case permet d'imprimer toute les cases sur le screen
        la boucle d'après permet de voir si la souris (le mask) overlap la case c'est a dire si la souris collide avec la case, si elle overlap le programme cherche l'object Case(i,j) et utilise sa fonction select pour faire un affichage visuel de la case choisi
"""

    

#player_direct = Perso(0,0,0,0,0,0,0,0,0,[])
# game = Game(player_direct)
# while True:
#     game.main_game()
num = 1
list_map = []
while os.path.exists(os.path.join(path.dirname(__file__), 'map_level_'+str(num)+'.txt')):
    level = Map("map_level_"+str(num)+".txt","map_decoration_level_"+str(num)+".txt","map_monstre_level_"+str(num)+".json",list_static_entity)
    level.init_map()
    list_map.append(level)
    num +=1
print("Nb map : %i"%len(list_map))
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
