import pygame, sys,pickle,os
import math
import random
from pygame import mixer
from script import pack,player,Wikitem,playerbis,pack_bis
from pygame.locals import *
from settings.screen import *
from settings.police import Drifftype,ColderWeather,Rumbletumble,coeff,coeff1,coeff2,ColderWeather_small
from settings.load_img import *
from settings.color import *
from fonction import *
from trash import Game
from custum_map_ import Map_editor
key = list(Wikitem.keys())

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Projet Pygeon')

pygame.mouse.set_cursor(*pygame.cursors.broken_x)
fullscreen = False

### Fixing path
path_pygeon = path.dirname(__file__)
path_addon = path.join(path_pygeon, 'Addon')
path_son = path.join(path_addon, 'Son')
path_police = path.join(path_addon, 'Police')
path_menu = path.join(path_addon, 'Menu')
path_demon_walk = path.join(path_addon, 'demon_walk')
path_seller = path.join(path_addon, 'seller')
###------------------------

class Menu():
    def __init__(self,player):
        self.perso = player
        self.click = False
        self.point_attrib = (4,2,1,1,2,3,5,7,10,13,17)
    def game_loop(self):
        running = True
        Xdd, Ydd, Xdragon, Ydragon = -150, -150, 800, -400
        LONGUEUR_1 = 1000
        LARGEUR_1 = 600
        global screen
        display = pygame.Surface((LONGUEUR_1,LARGEUR_1))
        mixer.music.load(path.join(path_son, 'background.wav'))
        mixer.music.play(-1)
        while running:
            Xdd, Ydd, Xdragon, Ydragon = Xdd + 1, Ydd + 1, Xdragon - 1.5, Ydragon + 1.5
            display.fill(BURGUNDY)
            draw_text('Press ESC to continue', ColderWeather_small,WHITE,display, LONGUEUR_1 / 4.5, LARGEUR_1 / 11)
            if Xdd >= -50: Xdd = -50
            if Ydd >= -50: Ydd = -50
            if Xdragon <= 450: Xdragon = 450
            if Ydragon >= -LONGUEUR / 14: Ydragon = -LONGUEUR / 14
            display.blit(DD, (Xdd, Ydd))
            display.blit(DK, (-240, 100))
            display.blit(D, (Xdragon, Ydragon))
            screen.blit(pygame.transform.scale(display,(LONGUEUR,LARGEUR)),(0,0))
            running = self.checkevent()
            pygame.display.update()

        mixer.music.stop()
        screen = pygame.display.set_mode((LONGUEUR,LARGEUR),pygame.RESIZABLE)
        self.main_menu()
    def main_menu(self):
        running = True
        display = pygame.Surface((1980,1000))
        first_blit=True
        while running:
            # SETUP BACKGROUNDS POLICE
            printbackgrounds(display)
            # CHOISIR UN MENU : CREATION BOUTON / AFFICHAGE
            text_width, text_height = Drifftype.size("Projet Pygeon")
            draw_text('Projet Pygeon', Drifftype, GREY, display, display.get_width()//2 - text_width // 2, display.get_height()//6)

            if create_text_click('Play',Drifftype,GREY,display,self.click,display.get_width()//2,display.get_height()//3):
                self.map_creator()
            if create_text_click('Charger',Drifftype,GREY,display,self.click,display.get_width()//2,display.get_height()//2.1):
                self.perso = load_game(self.click,self.perso)
            if create_text_click('Option',Drifftype,GREY,display,self.click,display.get_width()//2,display.get_height()//1.6):
                self.option()
            if create_text_click('Quit',Drifftype,GREY,display,self.click,display.get_width()//2,display.get_height()//1.3):
                sys.Quit()
            # REFRESH + END EVENT
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            running = self.checkevent()
            if not first_blit:pygame.display.update()
            first_blit = transition(2,screen.copy(),first_blit)
    def intermediaire_play(self):
        display = pygame.Surface((1980,1000))
        running = True
        self.click = False
        while running:
            # SETUP BACKGROUNDS POLICE
            printbackgrounds(display)
            # CHOISIR UN MENU : CREATION BOUTON / AFFICHAGE
            text_width, text_height = Drifftype.size("Projet Pygeon")
            draw_text('Projet Pygeon', Drifftype, GREY, display, display.get_width()//2 - text_width // 2, display.get_height()//6)
            if create_text_click('Campaign',Drifftype,GREY,display,self.click,display.get_width()//2,display.get_height()//3):
                self.play()
            if create_text_click('Create Campaign',Drifftype,GREY,display,self.click,display.get_width()//2,display.get_height()//2.1):
                self.map_creator()
            if create_text_click('Quit',Drifftype,GREY,display,self.click,display.get_width()//2,display.get_height()//1.3):
                sys.Quit()
            # REFRESH + END EVENT
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            running = self.checkevent()
            pygame.display.update()
    def map_creator(self):
        # Choisir Largueur
        display = pygame.Surface((1980,1000))
        running = True
        self.click = False
        longueur,largeur = 0,0
        first_blit = True
        while running:
            printbackgrounds(display)
            
            text_width, text_height = ColderWeather.size("Choisir une longueur")
            draw_text('Choisir une LONGUEUR', ColderWeather, GREY, display, display.get_width()//4 - text_width // 2.5, display.get_height()//6)
            bouton_longueur = pygame.Rect(display.get_width()//4 - text_width // 2.5, display.get_height()//6+1.5*text_height,text_width, text_height)
            pygame.draw.rect(display,(150,150,150),bouton_longueur,1)

            if bouton_click(bouton_longueur,display,self.click):
                longueur = self.checkclaviernum((display.get_width()//4 - text_width // 2.5),(display.get_height()//6+1.5*text_height),display,bouton_longueur)

            draw_text(str(longueur),ColderWeather,WHITE,display,display.get_width()//4 - text_width // 2.5, display.get_height()//6+1.5*text_height)

            text_width, text_height = ColderWeather.size("Choisir une Largeur")
            draw_text('Choisir une largeur', ColderWeather, GREY, display, display.get_width()//4 - text_width // 2.5, display.get_height()//2)
            bouton_longueur = pygame.Rect(display.get_width()//4 - text_width // 2.5, display.get_height()//2+1.5*text_height,text_width, text_height)
            pygame.draw.rect(display,(150,150,150),bouton_longueur,1)

            if bouton_click(bouton_longueur,display,self.click):
                largeur = self.checkclaviernum((display.get_width()//4 - text_width // 2.5),(display.get_height()//2+1.5*text_height),display,bouton_longueur)

            draw_text(str(largeur),ColderWeather,WHITE,display,display.get_width()//4 - text_width // 2.5, display.get_height()//2+1.5*text_height)

            if longueur != 0 and largeur != 0:
                if creation_img_text_click(img_next,"Suivant",ColderWeather,WHITE,display,self.click,right=1):
                    map_editor = Map_editor(longueur,largeur)
                    map_editor.print_menu_editor()
                    self.play()
            
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))

            if not first_blit:pygame.display.update()
            first_blit = transition(1,screen.copy(),first_blit)
            
            running = self.checkevent()
            
        # Choisir Longueur



    def play(self) :
        running = True
        self.click = False
        display = pygame.Surface((1980,1024))
        first_blit = False
        while running:
            # SETUP BACKGROUNDS POLICE
            printbackgrounds(display)
            # BOUTON img_next
            if self.perso == None:
                self.perso = player
            if self.perso.name != None and self.perso.classe != None:
                if creation_img_text_click(img_next,"Suivant",ColderWeather,WHITE,display,self.click,right=1):
                    game = Game(self.perso)
                    game.main_game()


            #for x in Wikitem:
            #    screen.blit(x.im)
            # CHOISIR UNE CLASSE : CREATION BOUTON

            text_width, text_height = ColderWeather.size("Choisir une classe :")
            draw_text('Choisir une classe',ColderWeather,GREY,display,display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 3 * text_height)

            text_width, text_height = ColderWeather.size("Sorcerer")
            button_1 = pygame.Rect(display.get_width()//4 - text_width // 2.5, display.get_height()//6 + 4*text_height, text_width, text_height)
            button_2 = pygame.Rect(display.get_width()//4 - text_width // 2.5, display.get_height()//6 + 5*text_height, text_width, text_height)
            button_3 = pygame.Rect(display.get_width()//4 - text_width // 2.5, display.get_height()//6 + 6*text_height, text_width, text_height)

            # CHOISIR UNE CLASSE : CHANGEMENT DE COULEUR QUAND SELECTIONNER

            if bouton_click(button_1,display,self.click) or self.perso.classe == 'Fighter':
                draw_text('Fighter', ColderWeather, RED, display, display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 4*text_height)
                self.perso.classe = 'Fighter'
            else:
                draw_text('Fighter', ColderWeather, WHITE, display, display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 4*text_height)


            if bouton_click(button_2,display,self.click) or self.perso.classe == 'Sorcerer':
                draw_text('Sorcerer',ColderWeather,RED,display,display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 5*text_height)
                self.perso.classe = 'Sorcerer'
            else:
                draw_text('Sorcerer',ColderWeather,WHITE,display,display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 5*text_height)


            if bouton_click(button_3,display,self.click) or self.perso.classe == 'Rogue':
                draw_text('Rogue',ColderWeather,RED,display,display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 6*text_height)
                self.perso.classe = 'Rogue'
            else:
                draw_text('Rogue',ColderWeather,WHITE,display,display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 6*text_height)

            # CHANGEMENTS CAPACITES JOUEURS : AFFICHAGE

            text_width, text_height = ColderWeather.size("Points Disponible")
            draw_text('Points Disponible : %d'%(self.perso.difficulty), ColderWeather, GREY, display, display.get_width() - display.get_width()//4 - text_width // 1.5,display.get_height()//6 )
            text_width, text_height = ColderWeather.size("STR")
            draw_text('STR : %d'%(self.perso.STR), ColderWeather, WHITE, display, display.get_width() - display.get_width()//4 - 2.5*text_width,display.get_height()//6 + 1*text_height )
            draw_text('DEX : %d'%(self.perso.DEX), ColderWeather, WHITE, display, display.get_width() - display.get_width()//4 - 2.5*text_width,display.get_height()//6 + 2*text_height)
            draw_text('CON : %d'%(self.perso.CON), ColderWeather, WHITE, display,display.get_width() - display.get_width()//4 - 2.5*text_width,display.get_height()//6 + 3*text_height)
            draw_text('INT : %d'%(self.perso.INT), ColderWeather, WHITE, display, display.get_width() - display.get_width()//4 - 2.5*text_width,display.get_height()//6 + 4*text_height)
            draw_text('WIS : %d'%(self.perso.WIS), ColderWeather, WHITE, display, display.get_width() - display.get_width()//4 - 2.5*text_width,display.get_height()//6 + 5*text_height)
            draw_text('CHA : %d'%(self.perso.CHA), ColderWeather, WHITE, display,display.get_width() - display.get_width()//4 - 2.5*text_width ,display.get_height()//6 + 6*text_height)

            # CHANGEMENTS CAPACITES JOUEURS : MISE A JOUR

            self.perso.STR = self.affichage_set_point(display.get_width() - display.get_width()//4 + 0.5*text_width,display.get_height()//6 + 1*text_height,self.perso.STR,display)
            self.perso.DEX = self.affichage_set_point(display.get_width() - display.get_width()//4 + 0.5*text_width,display.get_height()//6 + 2*text_height,self.perso.DEX,display)
            self.perso.CON = self.affichage_set_point(display.get_width() - display.get_width()//4 + 0.5*text_width,display.get_height()//6 + 3*text_height,self.perso.CON,display)
            self.perso.INT = self.affichage_set_point(display.get_width() - display.get_width()//4 + 0.5*text_width,display.get_height()//6 + 4*text_height,self.perso.INT,display)
            self.perso.WIS = self.affichage_set_point(display.get_width() - display.get_width()//4 + 0.5*text_width,display.get_height()//6 + 5*text_height,self.perso.WIS,display)
            self.perso.CHA = self.affichage_set_point(display.get_width() - display.get_width()//4 + 0.5*text_width,display.get_height()//6 + 6*text_height,self.perso.CHA,display)

            # CHANGEMENTS NOM

            text_width, text_height = ColderWeather.size("Choisir un Nom")
            draw_text('Choisir un Nom', ColderWeather, GREY, display, display.get_width()//4 - text_width // 2.5, display.get_height()//6)
            bouton_nom = pygame.Rect(display.get_width()//4 - text_width // 2.5, display.get_height()//6+1.5*text_height,text_width, text_height)
            pygame.draw.rect(display,(150,150,150),bouton_nom,1)

            if bouton_click(bouton_nom,display,self.click):
                self.perso.name = self.checkclavier((display.get_width()//4 - text_width // 2.5),(display.get_height()//6+1.5*text_height),display,bouton_nom)

            draw_text(self.perso.name,ColderWeather,WHITE,display,display.get_width()//4 - text_width // 2.5, display.get_height()//6+1.5*text_height)
            if self.perso.name != None:
                if len(self.perso.name) < 2 :
                    self.perso.name = None
                    Validation_screen("Erreur : Nom incorrect",display,self.click)

            # REFRESH + END EVENT
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            running = self.checkevent()
            if not first_blit:pygame.display.update()
            first_blit = transition(2,screen.copy(),first_blit)
    def option(self):
        running = True
        display = pygame.Surface((1980,1020))
        first_blit = True
        while running:
            global LONGUEUR
            global LARGEUR
            global screen
            global WINDOWS_SIZE
            display.fill(LIGHT_GREY)
            printbackgrounds(display)
            global fullscreen
            # Partie Choisir résolution
            if fullscreen:
                color = RED
            else:
                color = WHITE
            text_width, text_height = ColderWeather.size("Choisir la résolution")
            draw_text('Choisir la resolution', ColderWeather, GREY, display, display.get_width()//4 - text_width // 2.5, display.get_height()//6)

            if create_text_click("1980 x 1020",ColderWeather,WHITE,display,self.click,display.get_width()//4,display.get_height()//6+1*text_height):
                WINDOWS_SIZE = (1980,1020)
                screen = pygame.display.set_mode(WINDOWS_SIZE,pygame.RESIZABLE,32)
                fullscreen = False
            if create_text_click("1536 x 684",ColderWeather,WHITE,display,self.click,display.get_width()//4,display.get_height()//6+2.5*text_height):
                WINDOWS_SIZE = (1536,684)
                screen = pygame.display.set_mode(WINDOWS_SIZE,pygame.RESIZABLE,32)
                fullscreen = False
            if create_text_click("1152 x 645",ColderWeather,WHITE,display,self.click,display.get_width()//4,display.get_height()//6+4*text_height):
                WINDOWS_SIZE = (1152,645)
                screen = pygame.display.set_mode(WINDOWS_SIZE,pygame.RESIZABLE,32)
                fullscreen = False
            if create_text_click("768 x 432",ColderWeather,WHITE,display,self.click,display.get_width()//4,display.get_height()//6+5.5*text_height):
                WINDOWS_SIZE = (768 , 432)

                screen = pygame.display.set_mode(WINDOWS_SIZE,pygame.RESIZABLE,32)
                fullscreen = False
            if create_text_click("Full Screen",ColderWeather,color,display,self.click,display.get_width()//4,display.get_height()//6+7*text_height):
                if not fullscreen:
                    screen = pygame.display.set_mode(user_size,pygame.FULLSCREEN,32)
                    WINDOWS_SIZE = (pygame.display.Info().current_w,pygame.display.Info().current_h)
                if fullscreen:
                    WINDOWS_SIZE = (1152,645)
                    screen = pygame.display.set_mode(WINDOWS_SIZE,pygame.RESIZABLE,32)
                fullscreen = not fullscreen



            # Partie son
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            running = self.checkevent()
            if not first_blit:pygame.display.update()
            first_blit = transition(2,screen.copy(),first_blit)
    def affichage_set_point(self,x,y,cap,display):

        # CREATION/AFFICHAGE : BOUTON + et -

        t_width, t_height = Rumbletumble.size("+")
        draw_text('+', Rumbletumble, WHITE, display, x,y)
        button_ = pygame.Rect(x,y+0.90*t_width, t_width, t_width)

        draw_text('-', Rumbletumble, WHITE, display, x+3*t_width,y)
        button_2 = pygame.Rect(x+2.9*t_width,y+0.90*t_width, t_width, t_width)

        # REGLE POUR LES POINTS : https://www.d20pfsrd.com/basics-ability-scores/ability-scores

        if bouton_click(button_,display,self.click):
            if cap < 7 or cap >= 18:
                return cap
            elif self.perso.difficulty - self.point_attrib[cap - 7] < 0:
                return cap
            else:
                self.perso.difficulty = self.perso.difficulty - self.point_attrib[cap - 7]
                return cap + 1
        if bouton_click(button_2,display,self.click):
            if cap <= 7 or cap >= 19  :
                return cap
            else:
                self.perso.difficulty = self.perso.difficulty + self.point_attrib[cap - 8]
                return cap -1
        return cap
    def checkevent(self):
        global screen
        global WINDOWS_SIZE
        global fullscreen
        self.click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
            if event.type == VIDEORESIZE:
                if not fullscreen:
                    WINDOWS_SIZE = (event.w,event.h)
                    screen = pygame.display.set_mode(WINDOWS_SIZE,pygame.RESIZABLE,32)
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

        return True
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
                    if len(mot)<=8:
                        for i in range(len(all_key)):
                            if event.key == all_key[i]:
                                mot += chr(97+i)
                        if event.key == K_SPACE:
                            mot += ' '
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))

            pygame.display.update()
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

menu = Menu(player)
menu.map_creator()
