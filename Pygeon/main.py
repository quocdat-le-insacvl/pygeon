import pygame, sys,pickle,os
import numpy
import math
import random
from pygame import mixer
from script import pack,player,Wikitem,playerbis,pack_bis,entity_1
from pygame.locals import *
from settings.screen import *
from settings.police import Drifftype,ColderWeather,Rumbletumble,coeff,coeff1,coeff2,ColderWeather_small
from settings.load_img import *
from settings.color import *

key = list(Wikitem.keys())

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Projet Pygeon')

pygame.mouse.set_cursor(*pygame.cursors.broken_x)
fullscreen = False

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
        mixer.music.load(r'Pygeon\Addon\Son\background.wav')
        mixer.music.play(-1) 
        while running:
            Xdd, Ydd, Xdragon, Ydragon = Xdd + 1, Ydd + 1, Xdragon - 1.5, Ydragon + 1.5
            display.fill(BURGUNDY)
            self.draw_text('Press ESC to continue', ColderWeather_small,WHITE,display, LONGUEUR_1 / 4.5, LARGEUR_1 / 11)
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
        while running:

            # SETUP BACKGROUNDS POLICE
            
            self.printbackgrounds(display)
           
            # CHOISIR UN MENU : CREATION BOUTON / AFFICHAGE 
            text_width, text_height = Drifftype.size("Projet Pygeon")
            self.draw_text('Projet Pygeon', Drifftype, GREY, display, display.get_width()//2 - text_width // 2, display.get_height()//6)

            if self.create_text_click('Play',Drifftype,GREY,display,display.get_width()//2,display.get_height()//3):
                self.Play()
            if self.create_text_click('Option',Drifftype,GREY,display,display.get_width()//2,display.get_height()//2.1):
                self.Option()
            if self.create_text_click('Credit',Drifftype,GREY,display,display.get_width()//2,display.get_height()//1.6):
                self.Credit()
            if self.create_text_click('Quit',Drifftype,GREY,display,display.get_width()//2,display.get_height()//1.3):
                sys.Quit()
           
            # REFRESH + END EVENT
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            running = self.checkevent()
            pygame.display.update()
    def Play(self) :
        running = True
        display = pygame.Surface((1980,1024))
        while running:
            # SETUP BACKGROUNDS POLICE 
            self.printbackgrounds(display)
            # BOUTON img_next 

            if self.perso.name != None and self.perso.classe != None:
                if self.creation_img_text_click(img_next,"Suivant",ColderWeather,WHITE,display,right=1):
                    self.Credit() # HERE GAME LUNCHER 
                    
            if self.creation_img_text_click(img_next,"Reprendre",ColderWeather,WHITE,display,left=1):
                self.click = False
                self.load_game()
                
                 # HERE GAME LUNCHER 


            # CHOISIR UNE CLASSE : CREATION BOUTON

            text_width, text_height = ColderWeather.size("Choisir une classe :")
            self.draw_text('Choisir une classe',ColderWeather,GREY,display,display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 3 * text_height)
            
            text_width, text_height = ColderWeather.size("Sorcerer")
            button_1 = pygame.Rect(display.get_width()//4 - text_width // 2.5, display.get_height()//6 + 4*text_height, text_width, text_height)
            button_2 = pygame.Rect(display.get_width()//4 - text_width // 2.5, display.get_height()//6 + 5*text_height, text_width, text_height)
            button_3 = pygame.Rect(display.get_width()//4 - text_width // 2.5, display.get_height()//6 + 6*text_height, text_width, text_height)

            # CHOISIR UNE CLASSE : CHANGEMENT DE COULEUR QUAND SELECTIONNER 

            if self.bouton_click(button_1,display) or self.perso.classe == 'Fighter':
                self.draw_text('Fighter', ColderWeather, RED, display, display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 4*text_height)
                self.perso.classe = 'Fighter'
            else:
                self.draw_text('Fighter', ColderWeather, WHITE, display, display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 4*text_height)


            if self.bouton_click(button_2,display) or self.perso.classe == 'Sorcerer':
                self.draw_text('Sorcerer',ColderWeather,RED,display,display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 5*text_height)
                self.perso.classe = 'Sorcerer'
            else:
                self.draw_text('Sorcerer',ColderWeather,WHITE,display,display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 5*text_height)


            if self.bouton_click(button_3,display) or self.perso.classe == 'Rogue':
                self.draw_text('Rogue',ColderWeather,RED,display,display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 6*text_height)
                self.perso.classe = 'Rogue'
            else:
                self.draw_text('Rogue',ColderWeather,WHITE,display,display.get_width()//4 - text_width // 2.5,display.get_height()//6 + 6*text_height)
        
            # CHANGEMENTS CAPACITES JOUEURS : AFFICHAGE 

            text_width, text_height = ColderWeather.size("Points Disponible")
            self.draw_text('Points Disponible : %d'%(self.perso.difficulty), ColderWeather, GREY, display, display.get_width() - display.get_width()//4 - text_width // 1.5,display.get_height()//6 )
            text_width, text_height = ColderWeather.size("STR")
            self.draw_text('STR : %d'%(self.perso.STR), ColderWeather, WHITE, display, display.get_width() - display.get_width()//4 - 2.5*text_width,display.get_height()//6 + 1*text_height )
            self.draw_text('DEX : %d'%(self.perso.DEX), ColderWeather, WHITE, display, display.get_width() - display.get_width()//4 - 2.5*text_width,display.get_height()//6 + 2*text_height)
            self.draw_text('CON : %d'%(self.perso.CON), ColderWeather, WHITE, display,display.get_width() - display.get_width()//4 - 2.5*text_width,display.get_height()//6 + 3*text_height)
            self.draw_text('INT : %d'%(self.perso.INT), ColderWeather, WHITE, display, display.get_width() - display.get_width()//4 - 2.5*text_width,display.get_height()//6 + 4*text_height)
            self.draw_text('WIS : %d'%(self.perso.WIS), ColderWeather, WHITE, display, display.get_width() - display.get_width()//4 - 2.5*text_width,display.get_height()//6 + 5*text_height)
            self.draw_text('CHA : %d'%(self.perso.CHA), ColderWeather, WHITE, display,display.get_width() - display.get_width()//4 - 2.5*text_width ,display.get_height()//6 + 6*text_height)

            # CHANGEMENTS CAPACITES JOUEURS : MISE A JOUR 

            self.perso.STR = self.affichage_set_point(display.get_width() - display.get_width()//4 + 0.5*text_width,display.get_height()//6 + 1*text_height,self.perso.STR,display)
            self.perso.DEX = self.affichage_set_point(display.get_width() - display.get_width()//4 + 0.5*text_width,display.get_height()//6 + 2*text_height,self.perso.DEX,display)
            self.perso.CON = self.affichage_set_point(display.get_width() - display.get_width()//4 + 0.5*text_width,display.get_height()//6 + 3*text_height,self.perso.CON,display)
            self.perso.INT = self.affichage_set_point(display.get_width() - display.get_width()//4 + 0.5*text_width,display.get_height()//6 + 4*text_height,self.perso.INT,display)
            self.perso.WIS = self.affichage_set_point(display.get_width() - display.get_width()//4 + 0.5*text_width,display.get_height()//6 + 5*text_height,self.perso.WIS,display)
            self.perso.CHA = self.affichage_set_point(display.get_width() - display.get_width()//4 + 0.5*text_width,display.get_height()//6 + 6*text_height,self.perso.CHA,display)

            # CHANGEMENTS NOM 

            text_width, text_height = ColderWeather.size("Choisir un Nom")
            self.draw_text('Choisir un Nom', ColderWeather, GREY, display, display.get_width()//4 - text_width // 2.5, display.get_height()//6)
            bouton_nom = pygame.Rect(display.get_width()//4 - text_width // 2.5, display.get_height()//6+1.5*text_height,text_width, text_height)
            pygame.draw.rect(display,(150,150,150),bouton_nom,1)

            if self.bouton_click(bouton_nom,display):
                self.perso.name = self.checkclavier((display.get_width()//4 - text_width // 2.5),(display.get_height()//6+1.5*text_height),display,bouton_nom)

            self.draw_text(self.perso.name,ColderWeather,WHITE,display,display.get_width()//4 - text_width // 2.5, display.get_height()//6+1.5*text_height)
            if self.perso.name != None:
                if len(self.perso.name) < 2 :
                    self.perso.name = None
                    self.Validation_screen("Erreur : Nom incorrect",display)

            # REFRESH + END EVENT
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            running = self.checkevent()
            pygame.display.update()
    def Option(self):
        running = True
        display = pygame.Surface((1980,1020))
        while running:
            global LONGUEUR
            global LARGEUR
            global screen
            global WINDOWS_SIZE
            display.fill(LIGHT_GREY)
            self.printbackgrounds(display)
            global fullscreen
            # Partie Choisir résolution 
            if fullscreen:
                color = RED 
            else:
                color = WHITE
            text_width, text_height = ColderWeather.size("Choisir la résolution")
            self.draw_text('Choisir la resolution', ColderWeather, GREY, display, display.get_width()//4 - text_width // 2.5, display.get_height()//6)

            if self.create_text_click("1980 x 1020",ColderWeather,WHITE,display,display.get_width()//4,display.get_height()//6+1*text_height):
                WINDOWS_SIZE = (1980,1020)
                screen = pygame.display.set_mode(WINDOWS_SIZE,pygame.RESIZABLE,32)
            if self.create_text_click("1536 x 684",ColderWeather,WHITE,display,display.get_width()//4,display.get_height()//6+2.5*text_height):
                WINDOWS_SIZE = (1536,684)
                screen = pygame.display.set_mode(WINDOWS_SIZE,pygame.RESIZABLE,32)
            if self.create_text_click("1152 x 645",ColderWeather,WHITE,display,display.get_width()//4,display.get_height()//6+4*text_height):
                WINDOWS_SIZE = (1152,645)
                screen = pygame.display.set_mode(WINDOWS_SIZE,pygame.RESIZABLE,32)
            if self.create_text_click("768 x 432",ColderWeather,WHITE,display,display.get_width()//4,display.get_height()//6+5.5*text_height):
                WINDOWS_SIZE = (768 , 432)
                screen = pygame.display.set_mode(WINDOWS_SIZE,pygame.RESIZABLE,32)
            if self.create_text_click("Full Screen",ColderWeather,color,display,display.get_width()//4,display.get_height()//6+7*text_height):
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
            pygame.display.update()     
    def draw_text(self,text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect) 
    def affichage_set_point(self,x,y,cap,display):
       
        # CREATION/AFFICHAGE : BOUTON + et -

        t_width, t_height = Rumbletumble.size("+")
        self.draw_text('+', Rumbletumble, WHITE, display, x,y)
        button_ = pygame.Rect(x,y+0.90*t_width, t_width, t_width)

        self.draw_text('-', Rumbletumble, WHITE, display, x+3*t_width,y)
        button_2 = pygame.Rect(x+2.9*t_width,y+0.90*t_width, t_width, t_width)

        # REGLE POUR LES POINTS : https://www.d20pfsrd.com/basics-ability-scores/ability-scores

        if self.bouton_click(button_,display):
            if cap < 7 or cap >= 18:
                return cap
            elif self.perso.difficulty - self.point_attrib[cap - 7] < 0:
                return cap
            else:
                self.perso.difficulty = self.perso.difficulty - self.point_attrib[cap - 7]
                return cap + 1    
        if self.bouton_click(button_2,display):         
            if cap <= 7 or cap >= 19  :
                return cap
            else:
                self.perso.difficulty = self.perso.difficulty + self.point_attrib[cap - 8]
                return cap -1
        return cap
    def afficherinventaire(self,pack,pos_x,pos_y,display,Is_perso = True,Is_shop = False):
            #AFFICHAGE BACKGROUNDS 
            pack = pack 
            mouse_slot = pack.nb_x*pack.nb_y

            
            #screen.fill(LIGHT_GREY)
            menu_inventaire = pygame.transform.scale(menu_background,(LONGUEUR//2,LARGEUR//2))
            display.blit(menu_inventaire,(pos_x//2-LONGUEUR//4,pos_y//2-LARGEUR//4))
            display.blit(title,(pos_x//2-title.get_width()//2,pos_y//2-LARGEUR//3.5))
        
            #CREATION BOUTON INVENTAIRE
            bouton_test = dict()
            h=0
            for y in range(50,50+(pack.nb_x*50),50):
                for i in range(0,pack.nb_y,1):
                    bouton_test[h+i] = pygame.Rect(53*i+pos_x//2-LONGUEUR//5, 1.05*y+pos_y//2-LARGEUR//7, 50, 50)
                h += pack.nb_y

            # AFFICHER LES BOUTONS INVENTAIRE   
            if Is_perso:
                text_width, text_height = Drifftype.size("Inventaire")

                self.draw_text('Inventaire', ColderWeather, WHITE, display, pos_x//2-text_width//4,pos_y//2-text_height//2-menu_inventaire.get_height()//2.1)
                text_width, text_height = ColderWeather_small.size("Piece :  ")

                self.draw_text('Pieces : %i'%self.perso.argent,ColderWeather_small,WHITE,display,pos_x//2-text_width//2,pos_y//2+LARGEUR//6)
                self.draw_text('Poids : %i / %i'%(self.perso.poid_actuel,self.perso.poid_max),ColderWeather_small,WHITE,display,pos_x//2-LARGEUR//3,pos_y//2+LARGEUR//6)

            
            for i in range(0,pack.nb_x*pack.nb_y):
                pygame.draw.rect(display,LIGHT_GREY,bouton_test[i],1)
           
            # AFFICHER LES ITEMS INVENTAIRE
            h = 0
            for y in range(50,50+(pack.nb_x*50),50):
                for i in range(0,pack.nb_y,1):
                    if pack.backpack[h+i] != None :
                       display.blit(key[pack.backpack[h+i]].wpn_img,(bouton_test[h+i].x, bouton_test[h+i].y))     
                h += pack.nb_y
            
            if Is_perso:
                #CREATION BOUTONS JOUEURS ET AFFICHAGE
                bouton_arm = dict()

                for i in range(0,4):
                    bouton_arm[i] = pygame.Rect(pos_x//2-LONGUEUR//5+pack.nb_y*50*1.4, 1.05*(50*(i+1))+pos_y//2-LARGEUR//7,50,50)
                # pygame.draw.rect(display,WHITE,bouton_arm[i])
                    pygame.draw.rect(display,LIGHT_GREY,bouton_arm[i],1)
                    
                for i in range(0,2):
                    bouton_arm[4+i] = pygame.Rect(pos_x//2-LONGUEUR//5+pack.nb_y*50*1.6+53*i,1.05*50+pos_y//2-LARGEUR//7,50,50)
                    pygame.draw.rect(display,LIGHT_GREY,bouton_arm[4+i],1)
                
                for i in range(0,6):
                    if self.perso.armor[i] != None:
                        display.blit(key[self.perso.armor[i]].wpn_img,(bouton_arm[i].x,bouton_arm[i].y))
                        #self.draw_text(self.perso.armor[i].armor_name,Drifftype,WHITE,display,100,100)  


            #AFFICHER ITEMS CORPS JOUEURS

            #DRAG AND DROP
            
            mx,my = pygame.mouse.get_pos()
            mx = display.get_width() * mx / screen.get_width()
            my = display.get_height() * my / screen.get_height()
            #button_drag = pygame.Rect(mx,my,50,50)
            #pygame.draw.rect(display,RED,button_drag)

            # TEST : PRENDRE UN OBJECT DANS LA MOUSE
            if pack.backpack[mouse_slot] != None:
                have_object = True
                

            else:
                have_object = False
            i = 0
            while pack.backpack[i] != None:
                i += 1
            last_moove = i

            for i in range(pack.nb_x*pack.nb_y):
                if self.bouton_click(bouton_test[i],display):
                    if pack.backpack[i] != None and have_object == False:
                        pack.backpack[mouse_slot] = pack.backpack[i]
                        pack.backpack[i] = None
                        last_moove = i
                        have_object = True
                if Is_perso:
                    if i < 6 and self.bouton_click(bouton_arm[i],display):
                        if self.perso.armor[i] != None and have_object == False:
                            pack.backpack[pack.nb_x*pack.nb_y] = self.perso.armor[i]
                            self.perso.armor[i] = None
                            last_moove = mouse_slot+i+1
                            have_object = True
            if Is_shop :Is_buying = self.creation_img_text_click(img_next,"Acheter",ColderWeather,WHITE,display,pos_x//2+img_next.get_width()//2,pos_y//2,Click=False) and pack.backpack[mouse_slot] != None
            # TEST : DEPOSER UN OBJECT DE LA MOUSE VERS L INVENTAIRE 
            if pack.backpack[mouse_slot] != None:
                if any(pygame.mouse.get_pressed()):
                    have_object =True
                    display.blit(key[pack.backpack[mouse_slot]].wpn_img,(mx,my))
                elif not(any(pygame.mouse.get_pressed())):
                    if Is_shop and Is_buying: 
                        items = pack.backpack[mouse_slot]
                        pack.backpack[mouse_slot] = None
                        return items
                    else:
                        for i in range(pack.nb_y*pack.nb_x):
                            
                            if bouton_test[i].collidepoint((mx,my)) :
                                pack.backpack[last_moove] = pack.backpack[i]
                                pack.backpack[i] = pack.backpack[mouse_slot]
                                pack.backpack[mouse_slot] = None
                                last_moove = mouse_slot
                            if Is_perso:
                                if i < 6 and bouton_arm[i].collidepoint((mx,my)) and key[pack.backpack[mouse_slot]].wpn_type == i:
                                    pack.backpack[last_moove] = self.perso.armor[i]
                                    self.perso.armor[i] = pack.backpack[mouse_slot]
                                    pack.backpack[mouse_slot] = None
                                    last_moove = mouse_slot

                        if last_moove <= mouse_slot:
                            pack.backpack[last_moove] = pack.backpack[mouse_slot]
                            pack.backpack[mouse_slot] = None
                            have_object = False
                        else:
                            if Is_perso:
                                self.perso.armor[last_moove-mouse_slot-1] = pack.backpack[mouse_slot]
                                pack.backpack[mouse_slot] =None
                                have_object = False
            else:
                last_moove = -1
                #pygame.draw.rect(screen,RED,button_drag)
                have_object = False  
    def bouton_click(self,bouton,display,constant_click = 0):
        # TEST : BOUTON EST CLIQUE ?
        mx, my = pygame.mouse.get_pos()
        mx = display.get_width() * mx / screen.get_width()
        my = display.get_height() * my / screen.get_height()
        return bouton.collidepoint((mx,my)) and self.click
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

            self.draw_text(mot,ColderWeather,WHITE,display,x,y)
            
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
            self.draw_text(mot,ColderWeather,WHITE,display,x,y)
            
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
    def printbackgrounds(self,display):
        display.fill(LIGHT_GREY)
        global menu_background 
        menu_background = pygame.transform.scale(menu_background,(display.get_width(),display.get_height()))
        display.blit(menu_background,(0,0))     
    def load_game(self):
        running = True
        Choose = False
        self.click=False
        num = 0
        display = pygame.Surface((1980,1024))
        while running:

            self.printbackgrounds(display)
            #screen.blit(img_next,(LONGUEUR-338  ,LARGEUR-112))
            #screen.blit(img_next,(0,LARGEUR-112))

            button_save_1 = pygame.Rect(100,100,display.get_width()//2-150,display.get_height()//2-150)
            button_save_2 = pygame.Rect(display.get_width()//2,100,display.get_width()//2-150,display.get_height()//2-150)
            button_save_3 = pygame.Rect(100,display.get_height()//2,display.get_width()//2-150,display.get_height()//2-150)
            button_save_4 = pygame.Rect(display.get_width()//2,display.get_height()//2,display.get_width()//2-150,display.get_height()//2-150)

            if num == 1 : pygame.draw.rect(display,RED,button_save_1)
            else : pygame.draw.rect(display,LIGHT_GREY,button_save_1,1)
            if num == 2 : pygame.draw.rect(display,RED,button_save_2)
            else : pygame.draw.rect(display,LIGHT_GREY,button_save_2,1)
            if num == 3 : pygame.draw.rect(display,RED,button_save_3)
            else : pygame.draw.rect(display,LIGHT_GREY,button_save_3,1)
            if num == 4 : pygame.draw.rect(display,RED,button_save_4)
            else : pygame.draw.rect(display,LIGHT_GREY,button_save_4,1)

            text_width, text_height = ColderWeather.size("Sauvegarde 1")
            path = r'\Pygeon\\Save\\'
            if os.path.getsize(r'Pygeon\Save\sauvegarde') > 0 :
                with open(r'Pygeon\Save\sauvegarde','rb') as fichier:
                    mon_depickler = pickle.Unpickler(fichier)
                    inter = mon_depickler.load()
                    self.draw_text("Sauvegarde 1",ColderWeather,LIGHT_GREY,display,button_save_1.width//2-text_width//4,100+text_height//4)
                    self.draw_text("Nom : %s"%(inter.name),ColderWeather,LIGHT_GREY,display,button_save_1.width//2-text_width//4,200+text_height)
                    if self.bouton_click(button_save_1,display):
                        Choose = True
                        num = 1
                        choose_path = path + 'sauvegarde'
            else : self.draw_text("VIDE",ColderWeather,LIGHT_GREY,display,button_save_1.width//2-text_width//4,100+text_height//4)

            if os.path.getsize(r'Pygeon\Save\sauvegarde2') > 0 :
                with open(r'Pygeon\Save\sauvegarde2','rb') as fichier:
                    mon_depickler = pickle.Unpickler(fichier)
                    inter = mon_depickler.load()
                    self.draw_text("Sauvegarde 2",ColderWeather,LIGHT_GREY,display,(100-text_width//2+(display.get_width()//2-100)//2)+display.get_width()//2-100,100+text_height//4)
                    self.draw_text("Nom : %s"%(inter.name),ColderWeather,LIGHT_GREY,display,(100-text_width//2+(display.get_width()//2-100)//2)+display.get_width()//2-100,200+text_height)
                    if self.bouton_click(button_save_2,display):
                        Choose = True
                        num = 2
                        choose_path = path + 'sauvegarde2'
            else : self.draw_text("VIDE",ColderWeather,LIGHT_GREY,display,button_save_1.width//2-text_width//4,100+text_height//4)

            if os.path.getsize(r'Pygeon\Save\sauvegarde3') > 0 :
                with open(r'Pygeon\Save\sauvegarde3','rb') as fichier:
                    mon_depickler = pickle.Unpickler(fichier)
                    inter = mon_depickler.load()
                    self.draw_text("Sauvegarde 3",ColderWeather,LIGHT_GREY,display,100-text_width//2+(display.get_width()//2-100)//2,text_height//4+display.get_height()//2)
                    self.draw_text("Nom : %s"%(inter.name),ColderWeather,LIGHT_GREY,display,100-text_width//2+(display.get_width()//2-100)//2,text_height//4+display.get_height()//2+200)
                    if self.bouton_click(button_save_3,display):
                        Choose = True
                        num = 3
                        choose_path = path + 'sauvegarde3'
            else : self.draw_text("VIDE",ColderWeather,LIGHT_GREY,display,button_save_1.width//2-text_width//4,100+text_height//4)
        
            if os.path.getsize(r'Pygeon\Save\sauvegarde4') > 0 :
                with open(r'Pygeon\Save\sauvegarde4','rb') as fichier:
                    mon_depickler = pickle.Unpickler(fichier)
                    inter = mon_depickler.load()
                    self.draw_text("Sauvegarde 4",ColderWeather,LIGHT_GREY,display,(100-text_width//2+(display.get_width()//2-100)//2)+display.get_width()//2-100,text_height//4+display.get_height()//2)
                    self.draw_text("Nom : %s"%(inter.name),ColderWeather,LIGHT_GREY,display,(100-text_width//2+(display.get_width()//2-100)//2)+display.get_width()//2-100,text_height//4+display.get_height()//2+200)
                    if self.bouton_click(button_save_4,display):
                        Choose = True
                        num = 4
                        choose_path = path + 'sauvegarde4'
            else : self.draw_text("VIDE",ColderWeather,LIGHT_GREY,display,button_save_1.width//2-text_width//4,100+text_height//4)
            

            if (Choose):
                if self.creation_img_text_click(img_next,"Sauvegarder",ColderWeather,WHITE,display,0,0,right=1):
                    if self.perso.name == None:
                        self.Validation_screen("Erreur : Nom incorrect",display)
                    else:
                        self.click = False
                        text = 'Etes vous sur de vouloir sauvegarder ?'
                        if(self.Validation_screen(text,display)):
                            with open(choose_path,'wb') as fichier:
                                mon_pickler = pickle.Pickler(fichier)
                                mon_pickler.dump(self.perso)

                if self.creation_img_text_click(img_next,"Charger",ColderWeather,WHITE,display,0,0,left=1):
                    self.click = False
                    if (self.Validation_screen('Etes vous sur de vouloir charger ?',display)):
                        with open(choose_path,'rb') as fichier:
                            mon_depickler = pickle.Unpickler(fichier)
                            self.perso = mon_depickler.load()
                        return 

            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            running = self.checkevent()
            pygame.display.update()
    def Validation_screen(self,text,display):
        running = True
        while running:
            # Backgrounds :
            global img_backgrounds_warning 
            #self.printbackgrounds(display)
            display.fill(LIGHT_GREY)
            img_backgrounds_warning = pygame.transform.scale(img_backgrounds_warning,(display.get_width()//2,display.get_height()//4))
            display.blit(img_backgrounds_warning,(display.get_width()//2-img_backgrounds_warning.get_width()//2,display.get_height()//2-img_backgrounds_warning.get_height()))
            display.blit(exclamation,(display.get_width()//2+img_backgrounds_warning.get_width()//2.5,display.get_height()//2-1.1*img_backgrounds_warning.get_height()))
            text_width, text_height = ColderWeather_small.size(text)
            self.draw_text(text,ColderWeather_small,WHITE,display,display.get_width()//2-text_width//2,display.get_height()//2-text_height//2-img_backgrounds_warning.get_height()//2)
            pygame.display.update()
            if self.creation_img_text_click(validation_button,"Valider",ColderWeather,WHITE,display,display.get_width()//2,display.get_height()//2):
                return True
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            running = self.checkevent() 
            pygame.display.update()
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
    def create_text_click(self,text,font,color,display,x=0,y=0):
        text_width, text_height = font.size(text)
        button_1 = pygame.Rect(x - text_width // 2, y, text_width, text_height)
        self.draw_text(text,font,color,display,x - text_width // 2,y)
        if self.bouton_click(button_1,display):
            return True
    def shop_print(self,perso1,perso2,just_print = False):
        running = True
        display = pygame.Surface((1980,1024))
        while running:
            display.fill(LIGHT_GREY)
            items = None
            items = self.afficherinventaire(perso1.inventaire,display.get_width(),display.get_height()//2,display,False,Is_shop=True)
            if items != None:
                print(key[items].value)
                if (perso2.argent - key[items].value) < 0 :
                    self.Validation_screen("Vous avez pas assez d'argent",display)
                    #self.afficherinventaire(perso2.inventaire,display.get_width(),1.5*display.get_height())

                    perso1.inventaire.ajouteritems(perso1,key[items])
                else:
                    perso2.argent -= key[items].value
                    perso2.inventaire.ajouteritems(perso2,key[items])
            self.afficherinventaire(perso2.inventaire,display.get_width(),1.5*display.get_height(),display)


            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            pygame.display.update()
            running = self.checkevent()

menu = Menu(player)

menu.main_menu()
