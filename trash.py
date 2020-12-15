import pygame, sys,pickle,os
#import numpy
import math
import random
from pygame import mixer
from script import pack,player,Wikitem,playerbis,pack_bis
from pygame.locals import *
from settings.screen import *
from settings.police import Drifftype,ColderWeather,Rumbletumble,coeff,coeff1,coeff2,ColderWeather_small
from settings.load_img import *
from settings.color import *
from script import list_mooving_entity,list_static_entity
from fonction import *

pygame.init()
clock = pygame.time.Clock()

class Case():
    def __init__(self,i,j):
        self.in_case = None
        self.display = pygame.Surface((pixel_red.get_width(),pixel_red.get_height()))
        self.display.blit(case,(0,0))
        self.display.set_colorkey(BLACK)
        self.i = i
        self.j = j
        self.is_select = False
    def print_contains(self):
        if self.in_case != None:
            #screen.blit(self.in_case.display,(self.cordo()[0]+self.in_case.display.get_width()//2,self.cordo()[1]-self.in_case.display.get_height()//2))
            screen.blit(self.in_case.display,(self.cordo()[0]-self.in_case.img.get_width()//2,self.cordo()[1]-self.in_case.display.get_height()+self.in_case.img.get_height()//2+self.in_case.decalage_display[1]))
    def cordo(self):
        return ((self.j-self.i)*(pixel_red.get_width()+45)//2+screen.get_width()//2-pixel_red.get_width()//2,(self.j+self.i)*(pixel_red.get_width()+45)//4-100)
    def select(self,is_select):
        if is_select:
            screen.blit(case_select,self.cordo())
            self.is_select = True
        else :
            self.display.blit(case,(0,0))
            screen.blit(self.display,(0,0))
            self.is_select = False
    def select_neighbour(self,list_case):
        #if self.in_case != None:
        for x in list_case:
            x.is_select = False
            if x.j == self.j and x.i == self.i - 1 :
                x.select(True)
            if x.j == self.j and x.i == self.i + 1:
                x.select(True)
            if x.i == self.i and x.j == self.j -1 :
                x.select(True)
            if x.i == self.i and x.j == self.j +1 :
                x.select(True)
    #def print_sort(self,list_case):

class Game():
    def __init__(self,player):
        self.x = 0
        self.player = player
        self.click = False #Click souris
    def main_game(self):
        '''Choisis la postion de player, crée un rect / display joueur'''
        player_x,player_y=self.player.pos_x,self.player.pos_y
        player_rect = pygame.Rect(player_x,player_y,walk_bottom['walk_bottom_' + str(1) +'.png'].get_width(),walk_bottom['walk_bottom_' + str(1) +'.png'].get_height())
        display_joueurs = pygame.Surface((walk_bottom['walk_bottom_' + str(1) +'.png'].get_width(),walk_bottom['walk_bottom_' + str(1) +'.png'].get_height()))
        display_joueurs.set_colorkey(LIGHT_GREY)

        '''Set des display pour affichage carte'''
        display_arbre = pygame.Surface((18000,10000))
        display_arbre.set_colorkey(BLACK)
        Map = load_map(r"map.txt")
        display_with_nature = pygame.Surface((18000,10000))
        display_with_nature.set_colorkey(BLACK)
        display_with_nature,collision,collision_change_camera,tree_position,collision_entity = print_map(Map,display_with_nature)

        print_static_entity(display_with_nature,list_static_entity)
        
        #display,collision,collision_change_camera,tree_position,collision_entity = self.print_map(Map,display)
        display_arbre = print_nature(Map,display_arbre,tree_position)
        display_with_nature =print_nature(Map,display_with_nature,tree_position)
        display_with_nature.set_colorkey(LIGHT_GREY)

        perso_img = walk_bottom['walk_bottom_' + str(1) +'.png']

        ''' Set des masks pour collisions'''
        pieds = pygame.Surface((perso_img.get_width()-40,10))
        pieds.fill(RED)
        pieds_mask = pygame.mask.from_surface(pieds)
        pixel_mask = pygame.mask.from_surface(pixel_red)
        
        center_x,center_y = 0,0
        case_connue =[]
        
        '''Set de toute les variables d'actions'''
        swap = False
        entity_near = False
        interact = False
        pause_menu = False
        mouvement = [False,False,False,False]
        running = True
        n= 1
        f=0
        list_mooving_entity[1].update_interact()
        list_mooving_entity[1] = self.move_entity(list_mooving_entity[1],[0,0],collision_entity,collision,pieds_mask,player_rect)
        while running:
            mx,my = pygame.mouse.get_pos()
            screen.fill(LIGHT_GREY)

            """Changer l'affichage pour respecter vue joueurs"""
            if pause_menu:
                self.print_pause_menu()
                pause_menu = False
            if swap:
                screen.blit(display_with_nature,(center_x,center_y))
                screen.blit(rune_1,(11000+center_x,3000+center_y))
                screen.blit(display_joueurs,(center_x+player_rect.x,center_y+player_rect.y))
                screen.blit(display_arbre,(center_x,center_y))
            else:
                screen.blit(display_with_nature,(center_x,center_y))
                screen.blit(rune_1,(11000+center_x,3000+center_y))
                screen.blit(display_joueurs,(center_x+player_rect.x,center_y+player_rect.y))
            #screen.blit(grass["grass_yellow_2.png"],((self.ligne_colonne(mx-center_x,my-center_y)[1]-self.ligne_colonne(mx-center_x,my-center_y)[0])*190//2,(self.ligne_colonne(mx-center_x,my-center_y)[1]+self.ligne_colonne(mx-center_x,my-center_y)[0])*190//4))
            #draw_text("X: %i,Y:%i"%(self.ligne_colonne(mx-center_x,my-center_y)[0],self.ligne_colonne(mx-center_x,my-center_y)[1]),ColderWeather,WHITE,screen,300,300)
            '''Actualiser case interaction + animations'''
            for x in list_mooving_entity:
                x.animate_map()
                x.update_interact()
            
            deplacement = [0,0]
            f += 1

            if f < 150:
                list_mooving_entity[0] = self.move_entity(list_mooving_entity[0],[2,-1],collision_entity,collision,pieds_mask,player_rect)
                list_mooving_entity[2] = self.move_entity(list_mooving_entity[2],[2,-1],collision_entity,collision,pieds_mask,player_rect)
                #list_mooving_entity[1] = self.move_entity(list_mooving_entity[1],[2,-1],collision_entity,collision,pieds_mask,player_rect)
            elif f > 150:
                list_mooving_entity[0] = self.move_entity(list_mooving_entity[0],[-2,1],collision_entity,collision,pieds_mask,player_rect)
                list_mooving_entity[2] = self.move_entity(list_mooving_entity[2],[-2,1],collision_entity,collision,pieds_mask,player_rect)
                #list_mooving_entity[1] = self.move_entity(list_mooving_entity[1],[-2,1],collision_entity,collision,pieds_mask,player_rect)
            if f == 300:
                f=0
            
            

            print_mooving_entity(screen,list_mooving_entity,center_x,center_y)
            #self.ajouter_case_connue(player_rect,case_connue)
            #self.print_frog(player_rect,screen,case_connue,center_x,center_y)

            screen.blit(pieds,(center_x+player_rect.x+20,center_y+player_rect.y+perso_img.get_height()-15))
            entity = self.find_nearest_entity(player_rect,list_mooving_entity)
            #screen.blit(pixel_red,(center_x+list_mooving_entity[0].pos_x- pixel_red.get_width()//2+list_mooving_entity[0].img.get_width()//2,center_y+list_mooving_entity[0].pos_y+list_mooving_entity[0].img.get_height()-pixel_red.get_height()//1.5))
            #screen.blit(pixel_red,(95+center_x+list_mooving_entity[0].pos_x- pixel_red.get_width()//2+list_mooving_entity[0].img.get_width()//2,-47+center_y+list_mooving_entity[0].pos_y+list_mooving_entity[0].img.get_height()-pixel_red.get_height()//1.5))
            '''Action si contact avec entité'''
            if entity_near:
                draw_text("Press I for interact %s"%entity.name,ColderWeather,WHITE,screen,500,500)
                if entity.type == "Monster":
                    list_monster = []
                    list_monster.append(entity)
                    self.print_combat_screen(list_monster)
                if interact:
                    entity = self.find_nearest_entity(player_rect,list_mooving_entity)
                    self.interact_with_entity(entity)
                    mouvement[0],mouvement[1],mouvement[2],mouvement[3] = False,False,False,False
                    interact = False
            #list_mooving_entity[2] = self.move_entity(list_mooving_entity[2],[(player_rect.x-list_mooving_entity[2].pos_x)//100,(player_rect.y-list_mooving_entity[2].pos_y)//100],collision,pieds_mask,player_rect,perso_img)
            
            '''Affichage minimap'''
            screen.blit(pygame.transform.scale(display_with_nature,(300,100)),(LONGUEUR-300,LARGEUR-200))
            screen.blit(pygame.transform.scale(display_with_nature,(300,100)),(LONGUEUR-300,LARGEUR-200))
            draw_text(" player_x : %i,player_y : %i, %i , %i"%(len(collision_entity),list_mooving_entity[0].interaction[0][1],collision_entity[0][0],collision_entity[0][1]),ColderWeather,WHITE,screen,100,100)            
            '''Animation Frame'''
            if n > len(walk_bottom)-1 :
                n=1
            n+=0.1
            '''Set caméra / player pos pour sauvegarde'''
            center_x -= (player_rect.x + center_x -900)//20
            center_y -= (player_rect.y + center_y- 400) //20
            self.player.pos_x = player_rect.x
            self.player.pos_y = player_rect.y
            """ Déplacement joueurs"""
            if mouvement[0]:
                player_rect,swap,entity_near = self.move_player(player_rect,[10,-5],collision,collision_change_camera,pieds_mask,perso_img,center_x,center_y,swap,collision_entity,entity_near)
                display_joueurs.fill(LIGHT_GREY)
                display_joueurs.blit(walk_top['walk_top_' + str(int(n)) +'.png'],(0,0))
            elif mouvement[1]:
                player_rect,swap,entity_near = self.move_player(player_rect,[-10,+5],collision,collision_change_camera,pieds_mask,perso_img,center_x,center_y,swap,collision_entity,entity_near)
                display_joueurs.fill(LIGHT_GREY)
                display_joueurs.blit(walk_bottom['walk_bottom_' + str(int(n)) +'.png'],(0,0))
            elif mouvement[2]:
                player_rect,swap,entity_near  = self.move_player(player_rect,[+10,+5],collision,collision_change_camera,pieds_mask,perso_img,center_x,center_y,swap,collision_entity,entity_near)
                display_joueurs.fill(LIGHT_GREY)
                display_joueurs.blit(walk_right['walk_right_' + str(int(n)) + '.png'],(0,0))
            elif mouvement[3]:
                player_rect,swap,entity_near = self.move_player(player_rect,[-10,-5],collision,collision_change_camera,pieds_mask,perso_img,center_x,center_y,swap,collision_entity,entity_near)
                display_joueurs.fill(LIGHT_GREY)
                display_joueurs.blit(walk_left['walk_left_' + str(int(n)) + '.png'],(0,0))
            else:
                display_joueurs.fill(LIGHT_GREY)
                display_joueurs.blit(walk_bottom['walk_bottom_' + str(1) +'.png'],(0,0))

            """Check event classique"""
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
                    if event.key == K_ESCAPE:
                        pause_menu = True
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
    def print_combat_screen(self,list_monstre):
        running = True
        pixel_mask = pygame.mask.from_surface(pixel_red)
        souris_surf= pygame.Surface((1,1))
        souris_surf.fill(RED)
        souris_mask = pygame.mask.from_surface(souris_surf)
        pixel_red.set_alpha(0)
        Map = [['a','a','a'],['a','a','a']]
        case.set_colorkey(WHITE)
        display = pygame.Surface((screen.get_width(),screen.get_height()))
        display.set_colorkey(BLACK)
        l=load_map('map2.txt')
        case_select.set_alpha(100)
        list_case = []
        transition = pygame.Surface((screen.get_width(),screen.get_height()))
        transition.fill((0,0,0))
        f=0
        current_selec = None
        i,j= 0,0
        for h in l:
            j=0
            for g in h:
                if l[i][j] == 'w':
                    list_case.append(Case(i,j))
                j +=1
            i+=1
        i=0
        for x in list_monstre:
            list_case[i].in_case = x
            i+=1

        list_case[0].in_case = list_mooving_entity[0]
        list_case[1].in_case = list_mooving_entity[1]
        list_case[2].in_case = list_mooving_entity[2]
        while running:
            mx,my = pygame.mouse.get_pos()
            screen.fill(LIGHT_GREY)
            screen.blit(fond,(0,0))
            screen.blit(souris_surf,(mx,my))
            i=0
            
            for x in list_case:
                screen.blit(x.display,x.cordo())
                if x.in_case != None and not x.is_select:
                    x.in_case.type_animation = "idle"
                if x.in_case != None and x.is_select:
                    x.in_case.type_animation = "attack"
                if x.in_case != None:
                    x.in_case.animate()
                
            for x in list_case:
                x.print_contains()
            i,j= 0,0
            for h in l:
                j=0
                for g in h:
                    if l[i][j] =='w':
                        if pixel_mask.overlap(souris_mask,((mx-((j-i)*(pixel_red.get_width()+45)//2+screen.get_width()//2-pixel_red.get_width()//2),my-((j+i)*(pixel_red.get_width()+45)//4-100)))):
                            if self.click:
                                for x in list_case:
                                    if x.i == i and x.j == j:
                                        if current_selec != None and current_selec.in_case != None:
                                            if x.is_select and x.in_case == None:
                                                x.in_case = current_selec.in_case 
                                                current_selec.in_case = None
                                        current_selec = x
                                        
                                        #x.select(True)
                                        #x.select_neighbour(list_case)
                                print(i,j)
                    j +=1
                i+=1
            draw_text("i =%i j=%i %i"%(i,j,len(list_case)),ColderWeather,WHITE,screen,100,100)

            draw_text("%i"%list_case[0].is_select,ColderWeather,WHITE,screen,500,500)
            if current_selec != None:
                
                #current_selec.in_case = list_mooving_entity[0]
                #current_selec.print_contains()
                current_selec.select(True)
                current_selec.select_neighbour(list_case)
            if f != 255:
                for x in range(255):
                    f+=0.008
                    transition.set_alpha(int(255-f))
                screen.blit(transition,(0,0))
            pygame.display.update()
            running,self.click = basic_checkevent(self.click)
        """Affichage plateau + action souris
        principe de fonctionnement : 
        Le principe de la carte est le suivant : 
        Le jeu crée un object Case(i,j) a partir d'une map dans un text (qui contient des W) 
        Ensuite la boucle for x in list_case permet d'imprimer toute les cases sur le screen 
        la boucle d'après permet de voir si la souris (le mask) overlap la case c'est a dire si la souris collide avec la case, si elle overlap le programme cherche l'object Case(i,j) et utilise sa fonction select pour faire un affichage visuel de la case choisi"""
    def print_pause_menu(self):
        display = pygame.Surface((1980,1000))
        display.set_colorkey(LIGHT_GREY)
        running = True
        while running :
            display.fill(LIGHT_GREY)
            printbackgrounds(display)
            if create_text_click("Resume",Drifftype,GREY,display,self.click,display.get_width()//2,display.get_height()//3):
                break
            if create_text_click('Sauvegarder',Drifftype,GREY,display,self.click,display.get_width()//2,display.get_height()//2.1):
                load_game(self.click,self.player)
            if create_text_click('Quit',Drifftype,GREY,display,self.click,display.get_width()//2,display.get_height()//1.6):
                if Validation_screen("Voulez-vous quittez sans sauvegarder ?",display,self.click):
                    sys.exit()
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            pygame.display.update()
            running,self.click = basic_checkevent(self.click)
        self.click = False
        """Affiche un menu pause classique"""
    def ligne_colonne(self,pos_x,pos_y):
        return [math.trunc(1/(2*190)*(4*pos_y-2*(pos_x-9000))),math.trunc(1/(2*190)*(4*pos_y+2*(pos_x-9000)))]   
        """Retourne la ligne et la colonne en fonction de la position"""
    def move_player(self,rect,mouvement,collision,collision_change_camera,pieds_mask,perso_img,center_x,center_y,swap,collision_entity,entity_near):
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
        """def move_player():
        Permet de déplcer le player_rect de mouvement check si le joeurs ne collide pas avec un chamgement de caméra ou une entité"""
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
    def move_entity(self,entity,mouvement,collision_entity,collision,pieds_mask,joueurs):
        pixel_mask = pygame.mask.from_surface(pixel_red) 
        
        if collision.__contains__((entity.pos_x- pixel_red.get_width()//2+entity.img.get_width()//2,entity.pos_y-int(pixel_red.get_height()//1.5)+entity.img.get_height())):
            collision.remove((entity.pos_x- pixel_red.get_width()//2+entity.img.get_width()//2,entity.pos_y-int(pixel_red.get_height()//1.5)+entity.img.get_height()))
        if not pieds_mask.overlap(pixel_mask,((entity.pos_x- pixel_red.get_width()//2+entity.img.get_width()//2 + mouvement[0])-joueurs.x,entity.pos_y-int(pixel_red.get_height()//1.5)+entity.img.get_height()+ mouvement[1]-(joueurs.y+130))):
            for x in entity.interaction:
                if collision_entity.__contains__((int(x[0]),int(x[1]))):
                    collision_entity.remove((int(x[0]),int(x[1])))
                collision_entity.append((int(x[0])+mouvement[0],int(x[1])+mouvement[1]))
            collision.append((entity.pos_x- pixel_red.get_width()//2+entity.img.get_width()//2+ mouvement[0],entity.pos_y-int(pixel_red.get_height()//1.5)+entity.img.get_height()+ mouvement[1]))
            entity.pos_x += mouvement[0]
            entity.pos_y += mouvement[1]
            return entity
        else:
            #collision.remove((entity.pos_x+mouvement[0]+20,entity.pos_y+mouvement[1]+130))
            collision.append((entity.pos_x- pixel_red.get_width()//2+entity.img.get_width()//2,entity.pos_y-int(pixel_red.get_height()//1.5)+entity.img.get_height()))
            return entity
        """def move_entity(self,entity,mouvement,collision_entity,collision,pieds_mask,joueurs):
        Permet de décplacer une entité, gère les cases d'intéraction de l'entité + collision avec joueurs, retourne soit l'entité modifié soit l'entité non modifié de mouvement"""
    def find_nearest_entity(self,player_rect,list_entity):
        distance = abs(player_rect.x - list_entity[0].pos_x) + abs(player_rect.y - list_entity[0].pos_y)
        entity = list_entity[0]
        for i in range(len(list_entity)):
            if abs(player_rect.x - list_entity[i].pos_x) + abs(player_rect.y - list_entity[i].pos_y) < distance:
                distance = abs(player_rect.x - list_entity[i].pos_x) + abs(player_rect.y - list_entity[i].pos_y)
                entity = list_entity[i]
        return entity
        """def find_nearest_entity(self,player_rect,list_entity):
        Permet de trouver l'entité dans list_entity la plus proche de player_rect
        return Entity la plus proche de player_rect"""
    def interact_with_entity(self,entity):
        display_talk = pygame.Surface((1800,1080))
        display_talk.set_colorkey((0,0,0))
        
        if entity.type == "Seller":
            if entity.talking != None:
                if Validation_screen(entity.talking,display_talk,self.click):
                    entity.print_shop(self.player,self.click)
                screen.blit(display_talk,(0,0))
        '''def interact_with_entity(self,entity):
        Effectue les actions en fonctions du type de l'entité la fonction est à compléter elle ne traite pas tout les types entités'''   

game = Game(player)
#game.main_game()# Pour lancer la carte
game.print_combat_screen([]) #pour lancer le plateau combat
