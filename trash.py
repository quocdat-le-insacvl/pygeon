from skill import Stealth
from personnage import Perso
from entity import ChatBox,Chest,NPC
from fog import Fog
from minimap import Minimap
import pygame
import sys
import pickle
import os
import unittest
#import numpy
import math
import random
from pygame import mixer
from pygame.time import Clock
from script import pack, player, Wikitem, playerbis, pack_bis,NPC_quest
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
from combat import *
# from seller_scripts import list_seller
# from monster import Monster
# from custum_map_ import list_entity_animation
from skill import *
from quete import *
load_inv()
grass
pygame.init()
clock = pygame.time.Clock()
time_line = pygame.time.get_ticks()
""" Une chose intéréssant que je viens d'apprendre : Il faut utiliser toujours .convert() ou .conver_alpha() 
quand on load les images pour la question de performance
"""
key = list(Wikitem.keys())

dict_img_npc = dict()



donjon =  [json.loads(line) for line in open('donjon.json', 'r')]
print(f'TAILLE DU SCREEN {screen.get_width()},{screen.get_height()}')


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
        self.list_coffre = []
        self.key = dict()
        self.key["move right"] = K_RIGHT
        self.key["move left"] = K_LEFT
        self.key["move up"] = K_UP
        self.key["move down"] = K_DOWN
        self.key["interact"] = K_e
        self.key["inventaire"] = K_i
        self.key["charactere sheet"] = K_c 
        self.key["swap"] = K_s
        self.key["map"] = K_m
        self.list_dungeon = dict()
        bequille = True
        if not reload:
            for i in range(len(self.map.map_decoration)):
                if self.map.map_decoration[i] != None:
                    for j in range(len(self.map.map_decoration[i])):
                            
                            if (self.map.map_decoration[i][j]=='8' or self.map.map_decoration[i][j]=='9') and bequille:
                                bequille= False
                                donj = Donjon(0,self.screen,self.player,game=self)
                                donj.creationDonjon()
                                self.list_dungeon[(i,j)] = donj
    
    def main_game(self):
        global time_line
        self.init_skill()
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
            self.map.list_shop.append(x)
            
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
        self.minimap = Minimap(self.map.map,self.fog,self.map.display,self.list_mooving_entity,self.player)
    
        for x in donjon:
            x[0],x[1] = (x[1]-x[0])*190//2+9000,(x[1]+x[0])*190//4
        look_level = False
        mp = 0 
        ###
        show_inventory = False
        show_characteresheet = False
        display_1 = pygame.Surface((1980,1080))
        display_1.set_colorkey(BLACK)
        draw_interact = True
        frame = 1
        nb_crew = 0
        self.player.know_map.append(self.current_level)
        self.player.xp += 12000
        self.player.levelupchange()
        self.player.levelupchange()
        self.player.levelupchange()
        self.player.levelupchange()
        self.player.levelupchange()
        self.player.levelupchange()
        self.player.levelupchange()
        self.player.levelupchange()
        self.player.levelupchange()

        self.map.list_shop.append(NPC_quest)


        while running:
            for x in self.map.list_shop:
                self.map.display.blit(x.img,(x.pos_x,x.pos_y))
            


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
                    if x.hp > 0 :
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
                    if x.hp > 0 :
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
            if self.player.collision_donjon:
                if draw_interact: draw_text("Press Interact",ColderWeather,WHITE,screen,500,500)
                if interact:
                    pygame.image.save(self.fog.surface,'fog_'+str(self.current_level)+ '.png')
                    pos_joueur = (self.player.pos_x,self.player.pos_y)
                    coordDonjon = self.closest_dungeon(self.list_dungeon.keys(),self.player)
                    if coordDonjon !=-1:
                        
                        self.list_dungeon[coordDonjon].affichageDonjon()
                        a=self.list_dungeon[coordDonjon].runningDonjon()
                        if a==-1:
                            self.game_over()
                        if a==1:
                            difficulte = self.list_dungeon[coordDonjon].difficulty
                            self.list_dungeon[coordDonjon] =  Donjon(difficulte+1,self.screen,self.player,game=self)
                            self.list_dungeon[coordDonjon].creationDonjon()

                    else: #ne devrait jamais arriver
                        pass
                    self.player.pos_x = pos_joueur[0]
                    self.player.pos_y = pos_joueur[1]
                    interact = False
            if self.player.change_level:
                if draw_interact: draw_text("Press I for go under",ColderWeather,WHITE,screen,500,500)
                if interact:
                   
                    
                    
                    for x in donjon:
                        x_ = x[0]-self.player.pos_x
                        y = x[1] - self.player.pos_y

                        if abs(x[0]-self.player.pos_x) < 200 and abs(x[1]-self.player.pos_y) < 200 :
                            self.map = list_map[x[3]-1]
                            self.current_level = x[3]
                            self.fog = Fog(self.player,self.map.display)
                            self.minimap.display_with_nature = self.map.display
                            self.minimap.fog = self.fog
                            if not self.player.know_map.__contains__(self.current_level):
                                self.player.know_map.append(self.current_level)
                            else:
                                self.fog.surface = pygame.image.load('fog_' + str(self.current_level)+ '.png').convert()


                        if self.map.spawn_point != (0,0):
                            self.player.pos_x = self.map.spawn_point[0]
                            self.player.pos_y = self.map.spawn_point[1]
                    
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
                        self.fog = Fog(self.player,self.map.display)
                        self.minimap.display_with_nature = self.map.display
                        self.minimap.fog = self.fog
                        if not self.player.know_map.__contains__(self.current_level):
                            self.player.know_map.append(self.current_level)
                        else:
                            self.fog.surface = pygame.image.load('fog_' + str(self.current_level)+ '.png').convert()
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
                self.click = False

                # handle chatbox
                chatting = self.chat_box.handle_event(event)
                if not chatting:
                    self.player.check_user(event,self.key)
                    if event.type == QUIT:
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == self.key["interact"]:
                            interact = not interact
                        if event.key == self.key["map"]:
                            self.zoom_map = True
                        if event.key == self.key["inventaire"]:
                            show_inventory = not show_inventory
                       
                        if event.key == self.key["charactere sheet"]:
                            show_characteresheet = not show_characteresheet
                        
                        if event.key == self.key["swap"]:
                            
                            self.player = self.player.crew_mate[0]
                            self.fog.player = self.player
                            self.minimap.player = self.player
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
                        if event.key == self.key["map"]:
                            self.zoom_map = False
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.click = True
            monstre = self.player.move_player(self.map.dict_collision,self.map.list_shop,self.map.list_monster,self.list_coffre)
            self.player.animate_map()
            if self.player.entity_near:
                if draw_interact: draw_text("Press Interact key",ColderWeather,WHITE,screen,500,500)
                if interact:
                    draw_interact = False
                    is_talking = self.interact(monstre,is_talking)
                    if not is_talking:
                        interact = False

                    self.player.mouvement = [False,False,False,False]
            else:
                draw_interact = True
            
            if self.player.monstre_near and monstre != None:

                f = Combat(self,monstre.group_monster)
                f.affichage()
                self.player.mouvement = [False,False,False,False]
                dec = 0
                
                if f.player.crew_mate[0].hp > 0 or f.player.crew_mate[1].hp > 0  or f.player.hp > 0:
                    for x in monstre.group_monster:
                        if self.player.levelupchange():
                            look_level = True
                        self.player.xp += x.xp
                        inv_chest = Inventaire(7,7)
                        inv_chest.add_random_drop(3)
                        self.list_coffre.append(Chest(self.player.pos_x+dec,self.player.pos_y+dec,monstre_loot,"Coffre","Coffre",inv_chest))
                        self.list_coffre[len(self.list_coffre)-1].update_pos_collide()
                        self.map.list_monster.remove(x)
                        dec += 70
            if self.player.hp <=0 and self.player.crew_mate[0].hp <=0 and self.player.crew_mate[1].hp <=0:
                self.game_over()
                running = False
            elif self.player.hp <=0:
                self.player = self.player.crew_mate[0]
                self.fog.player = self.player
                
                nb_crew+=1
                if nb_crew ==2:
                    nb_crew = 0
                monstre = None
            
            for x in self.list_coffre:
                screen.blit(x.img,(center_x +x.pos_x,center_y +x.pos_y))
            
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
            if len(self.list_coffre) > 0:
                draw_text("Coffre: %i Pos_x : %i Pos_y : %i" % (mp,self.list_coffre[0].pos_x,self.list_coffre[0].pos_y), ColderWeather, WHITE, screen, 100, 100)
            
            # update skill
            self.player.spell_bar(self.click)
            for skill in self.player.skill:
                skill.update()
    
            if look_level:
                mp +=1
            if mp >= 50 and mp <= 200:
                screen.blit(pygame.transform.scale(pygame.image.load(path.join(path_addon,'Image/lvl_up.png')),(WINDOWS_SIZE[0]//20,WINDOWS_SIZE[1]//20)),(self.player.pos_x+100+center_x,self.player.pos_y+center_y))
            elif mp>200:
                look_level = False
                mp =0

            # update + draw chatbox
            self.chat_box.update()
            self.chat_box.draw()
            pygame.display.update()
            clock.tick(64)
    def game_over(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        running=False
                screen.fill(BLACK)
                text_width, text_height = ColderWeather.size("GAME OVER")
                draw_text("GAME OVER",ColderWeather,WHITE,screen,screen.get_width()//2-text_width//2,screen.get_height()//2-text_height//2)
                running,self.click = basic_checkevent(self.click)
                pygame.display.update()
        
    def print_pause_menu(self):
        display = pygame.Surface((1980, 1000))
        display.set_colorkey(LIGHT_GREY)
        
        running = True
        while running:
            display.fill(LIGHT_GREY)
            printbackgrounds(display)
            if create_text_click("Resume", Drifftype, GREY, display, self.click, display.get_width()//2, display.get_height()-800):
                break
            if create_text_click('Sauvegarder', Drifftype, GREY, display, self.click, display.get_width()//2, display.get_height()-600):
                global player_for_save
                player_for_save.load_player(self.player)
                player_for_save,self.fog.surface = load_game(self.click, player_for_save,self.fog.surface,list_map=list_map)
                self.map = list_map[0]
                self.minimap = Minimap(self.map.map,self.fog,self.map.display,[],self.player)
                print(player_for_save.name)
                self.player.load_player(player_for_save)
            if create_text_click('Options', Drifftype, GREY, display, self.click, display.get_width()//2, display.get_height()-400):
                self.key_menu()
            if create_text_click('Quit', Drifftype, GREY, display, self.click, display.get_width()//2, display.get_height()-200):
                if Validation_screen("Voulez-vous quittez sans sauvegarder ?", display, self.click):
                    sys.exit()
            screen.blit(pygame.transform.scale(display, WINDOWS_SIZE), (0, 0))
            pygame.display.update()
            running, self.click = basic_checkevent(self.click)
        self.click = False
        """Affiche un menu pause classique"""
    def key_menu(self):
        running = True
        display = pygame.Surface((1980,1000))
        list_key = list(self.key.keys())
        i=0
        j=0
        while running:
            printbackgrounds(display)
            i=0
            j=0
            for x in list_key:
                if i == 5:
                    i=0
                    j+=1
                
                text_width, text_height = ColderWeather.size("A")
                draw_text(x, ColderWeather, GREY, display, display.get_width()//4 - text_width // 2.5+j*500, display.get_height()//6+100*i)
                bouton_longueur = pygame.Rect(display.get_width()//4 - text_width // 2.5+j*500, display.get_height()//6+1.5*text_height+100*(i-1)+50,text_width, text_height//2)
                pygame.draw.rect(display,(150,150,150),bouton_longueur,1)
                
                i+=1
                if bouton_click(bouton_longueur,display,self.click):

                    choice = self.checkclavier(display.get_width()//4 - text_width // 2.5+j*500, display.get_height()//6+100*(i-1)+50,display,bouton_longueur)
                    self.key[x] = pygame.key.key_code(choice)
                
                draw_text(pygame.key.name(self.key[x]),ColderWeather,WHITE,display,display.get_width()//4 - text_width // 2.5+j*500, display.get_height()//6+100*(i-1)+50)
                
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            pygame.display.update()
            running,self.click = basic_checkevent(self.click)

    def checkclavier(self,x,y,display,rect):
        running = True
        mot = ''
        all_key = (K_a,K_b,K_c,K_d,K_e,K_f,K_g,K_h,K_i,K_j,K_k,K_l,K_m,K_n,K_o,K_p,K_q,K_r,K_s,K_t,K_u,K_v,K_w,K_x,K_y,K_z)
        
        while running:
            display.fill(LIGHT_GREY,rect)

            draw_text(mot,ColderWeather,WHITE,display,x,y)

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN :
                    if event.key == K_ESCAPE or event.key == K_RETURN:
                        return mot
                        running = False
                    if event.key == K_BACKSPACE:
                        mot = mot[:len(mot)-1]
                    if len(mot)<=0:
                        for i in range(len(all_key)):
                            if event.key == all_key[i]:
                                mot += chr(97+i)
                        if event.key == K_SPACE:
                            mot += ' '
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))

            pygame.display.update()
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
        elif entity.type == "Coffre":
            entity.inventaire.loot_inventory(100,100,700,100,self.player.inventaire)
            if entity.inventaire.is_empty():
                entity.img = monstre_loot_open
            else:
                entity.img = monstre_loot_light
        elif isinstance(entity,NPC):
            if entity.quest != None:
                if not entity.quest.is_accomplish:
                    if entity.quest.print_text(self.click):
                        return 0
                    entity.quest.print_reward()
                    if isinstance(entity.quest,Quest_find_items):
                        entity.quest.print_items()
                        if entity.quest.is_accept:
                            if entity.quest.got_items(self.player):
                                entity.quest.quest_accomplish(self.player)
                            else:
                                return False
                    elif isinstance(entity.quest,Quest_kill_monster):
                        entity.quest.print_monster()
                        if entity.quest.is_accept:
                            if entity.quest.is_alive():
                                entity.quest.quest_accomplish(self.player)
                            else:
                                return False
        return 1

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

            dist = math.sqrt((x - perso.pos_x)**2 + (y - perso.pos_y)**2)
            if min == -1 or dist < min:
                min = dist
                coordRetour = coord



        return coordRetour
    def init_skill(self):
        if self.player.classe == 'rogue':
            self.player.skill.append(Stealth(self))
            self.player.skill.append(Perception(self))
        else:
            self.player.skill.append(Perception(self))
        if self.player.crew_mate[0].classe == 'rogue':
            self.player.crew_mate[0].skill.append(Stealth(self))
            self.player.crew_mate[0].skill.append(Perception(self))
        else:
            self.player.crew_mate[0].skills.append(Perception(self))
        if self.player.crew_mate[1].classe == 'rogue':
            self.player.crew_mate[1].skill.append(Stealth(self))
            self.player.crew_mate[1].skill.append(Perception(self))
        else:
            self.player.crew_mate[1].skill.append(Perception(self))
    def init_crewmate(self):
        pass


    


num = 1
list_map = []
while os.path.exists(os.path.join(path.dirname(__file__), 'map_level_'+str(num)+'.txt')):
    level = Map("map_level_"+str(num)+".txt","map_decoration_level_"+str(num)+".txt","map_monstre_level_"+str(num)+".json",[])
    level.init_map()
    list_map.append(level)
    num +=1
print("Nb map : %i"%len(list_map))

sorcerer.crew_mate.append(sorcerer_2)
sorcerer.crew_mate.append(sorcerer_3)

sorcerer_2.crew_mate.append(sorcerer_3)
sorcerer_2.crew_mate.append(sorcerer)

sorcerer_3.crew_mate.append(sorcerer)
sorcerer_3.crew_mate.append(sorcerer_2)



#map_1.init_map()
#game = Game(sorcerer,list_map[0])
#c = Combat(game,[])
#c.affichage()

#game.main_game()
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
