import pygame, sys,pickle,os
import numpy
import math
from pygame import mixer
from script import pack,player,Wikitem
from pygame.locals import *
from settings.screen import LARGEUR, LONGUEUR, screen
from settings.police import Drifftype,ColderWeather,Rumbletumble,coeff,coeff1,coeff2,ColderWeather_small
from settings.load_img import *
from settings.color import *

key = list(Wikitem.keys())


pygame.init()
pygame.display.set_caption('Projet Pygeon')

pygame.mouse.set_cursor(*pygame.cursors.broken_x)


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
        screen = pygame.display.set_mode((LONGUEUR_1, LARGEUR_1),pygame.RESIZABLE)
        mixer.music.load(r'Pygeon\Addon\Son\background.wav')
        mixer.music.play(-1) 
        while running:
            Xdd, Ydd, Xdragon, Ydragon = Xdd + 1, Ydd + 1, Xdragon - 1.5, Ydragon + 1.5
            screen.fill(BURGUNDY)
            self.draw_text('Press ESC to continue', ColderWeather_small,WHITE,screen, LONGUEUR_1 / 4.5, LARGEUR_1 / 11)
            if Xdd >= -50: Xdd = -50
            if Ydd >= -50: Ydd = -50
            if Xdragon <= 450: Xdragon = 450
            if Ydragon >= -LONGUEUR / 14: Ydragon = -LONGUEUR / 14
            screen.blit(DD, (Xdd, Ydd))
            screen.blit(DK, (-240, 100))
            screen.blit(D, (Xdragon, Ydragon))
            
            running = self.checkevent()
            pygame.display.update()
    
        mixer.music.stop()
        screen = pygame.display.set_mode((LONGUEUR,LARGEUR),pygame.RESIZABLE)
        self.main_menu()

    def main_menu(self):
        running = True
        while running:

            # SETUP BACKGROUNDS POLICE
            
            self.printbackgrounds()
            
            # CHOISIR UN MENU : CREATION BOUTON / AFFICHAGE 

            text_width, text_height = Drifftype.size("Projet Pygeon")
            self.draw_text('Projet Pygeon', Drifftype, GREY, screen, LONGUEUR//2 - text_width // 2, LARGEUR//6)

            text_width, text_height = Drifftype.size("Play")
            button_1 = pygame.Rect(LONGUEUR//2 - text_width // 2, LARGEUR//3, text_width, text_height)
            self.draw_text('Play',Drifftype,GREY,screen,LONGUEUR//2 - text_width // 2,LARGEUR//3)

            text_width, text_height = Drifftype.size("Option")
            button_2 = pygame.Rect(LONGUEUR//2 - text_width // 2, LARGEUR//2.1, text_width, text_height)
            self.draw_text('Option',Drifftype,GREY,screen,LONGUEUR//2 - text_width // 2,LARGEUR//2.1)

            text_width, text_height = Drifftype.size("Credit")
            self.draw_text('Credit',Drifftype,GREY,screen,LONGUEUR//2 - text_width // 2,LARGEUR//1.6)
            button_3 = pygame.Rect(LONGUEUR//2 - text_width // 2, LARGEUR//1.6, text_width, text_height)

            text_width, text_height = Drifftype.size("Quit")
            button_4 = pygame.Rect(LONGUEUR//2 - text_width // 2, LARGEUR//1.3, text_width, text_height)
            self.draw_text('Quit',Drifftype,GREY,screen,LONGUEUR//2 - text_width // 2,LARGEUR//1.3)

            # CHOISIR UN MENU : DETECTION DE CLICK 

            if self.bouton_click(button_1):
                self.Play()
            if self.bouton_click(button_2):
                self.Option()
            if self.bouton_click(button_3):
                self.Credit()
            if self.bouton_click(button_4):
                self.Quit()

            # REFRESH + END EVENT

            running = self.checkevent()
            pygame.display.update()
    def Play(self) :
        running = True
        while running:
            # TEST
            self.printbackgrounds()
           
            # SETUP BACKGROUNDS POLICE 
            
           
                
            # BOUTON img_next 

            if self.perso.name != None and self.perso.classe != None:
                if self.creation_img_text_click(img_next,"Suivant",ColderWeather,WHITE,right=1):
                    self.afficherinventaire(self.perso.inventaire) # HERE GAME LUNCHER 
                    
            if self.creation_img_text_click(img_next,"Reprendre",ColderWeather,WHITE,left=1):
                self.click = False
                self.load_game()
                
                 # HERE GAME LUNCHER 


            # CHOISIR UNE CLASSE : CREATION BOUTON

            text_width, text_height = ColderWeather.size("Choisir une classe :")
            self.draw_text('Choisir une classe',ColderWeather,GREY,screen,LONGUEUR//4 - text_width // 2.5,LARGEUR//6 + 3 * text_height)
            
            text_width, text_height = ColderWeather.size("Sorcerer")
            button_1 = pygame.Rect(LONGUEUR//4 - text_width // 2.5, LARGEUR//6 + 4*text_height, text_width, text_height)
            button_2 = pygame.Rect(LONGUEUR//4 - text_width // 2.5, LARGEUR//6 + 5*text_height, text_width, text_height)
            button_3 = pygame.Rect(LONGUEUR//4 - text_width // 2.5, LARGEUR//6 + 6*text_height, text_width, text_height)

            # CHOISIR UNE CLASSE : CHANGEMENT DE COULEUR QUAND SELECTIONNER 

            if self.bouton_click(button_1) or self.perso.classe == 'Fighter':
                self.draw_text('Fighter', ColderWeather, RED, screen, LONGUEUR//4 - text_width // 2.5,LARGEUR//6 + 4*text_height)
                self.perso.classe = 'Fighter'
            else:
                self.draw_text('Fighter', ColderWeather, WHITE, screen, LONGUEUR//4 - text_width // 2.5,LARGEUR//6 + 4*text_height)


            if self.bouton_click(button_2) or self.perso.classe == 'Sorcerer':
                self.draw_text('Sorcerer',ColderWeather,RED,screen,LONGUEUR//4 - text_width // 2.5,LARGEUR//6 + 5*text_height)
                self.perso.classe = 'Sorcerer'
            else:
                self.draw_text('Sorcerer',ColderWeather,WHITE,screen,LONGUEUR//4 - text_width // 2.5,LARGEUR//6 + 5*text_height)


            if self.bouton_click(button_3) or self.perso.classe == 'Rogue':
                self.draw_text('Rogue',ColderWeather,RED,screen,LONGUEUR//4 - text_width // 2.5,LARGEUR//6 + 6*text_height)
                self.perso.classe = 'Rogue'
            else:
                self.draw_text('Rogue',ColderWeather,WHITE,screen,LONGUEUR//4 - text_width // 2.5,LARGEUR//6 + 6*text_height)
        
            # CHANGEMENTS CAPACITES JOUEURS : AFFICHAGE 

            text_width, text_height = ColderWeather.size("Points Disponible")
            self.draw_text('Points Disponible : %d'%(self.perso.difficulty), ColderWeather, GREY, screen, LONGUEUR - LONGUEUR//4 - text_width // 1.5,LARGEUR//6 )
            text_width, text_height = ColderWeather.size("STR")
            self.draw_text('STR : %d'%(self.perso.STR), ColderWeather, WHITE, screen, LONGUEUR - LONGUEUR//4 - 2.5*text_width,LARGEUR//6 + 1*text_height )
            self.draw_text('DEX : %d'%(self.perso.DEX), ColderWeather, WHITE, screen, LONGUEUR - LONGUEUR//4 - 2.5*text_width,LARGEUR//6 + 2*text_height)
            self.draw_text('CON : %d'%(self.perso.CON), ColderWeather, WHITE, screen,LONGUEUR - LONGUEUR//4 - 2.5*text_width,LARGEUR//6 + 3*text_height)
            self.draw_text('INT : %d'%(self.perso.INT), ColderWeather, WHITE, screen, LONGUEUR - LONGUEUR//4 - 2.5*text_width,LARGEUR//6 + 4*text_height)
            self.draw_text('WIS : %d'%(self.perso.WIS), ColderWeather, WHITE, screen, LONGUEUR - LONGUEUR//4 - 2.5*text_width,LARGEUR//6 + 5*text_height)
            self.draw_text('CHA : %d'%(self.perso.CHA), ColderWeather, WHITE, screen,LONGUEUR - LONGUEUR//4 - 2.5*text_width ,LARGEUR//6 + 6*text_height)

            # CHANGEMENTS CAPACITES JOUEURS : MISE A JOUR 

            self.perso.STR = self.affichage_set_point(LONGUEUR - LONGUEUR//4 + 0.5*text_width,LARGEUR//6 + 1*text_height,self.perso.STR)
            self.perso.DEX = self.affichage_set_point(LONGUEUR - LONGUEUR//4 + 0.5*text_width,LARGEUR//6 + 2*text_height,self.perso.DEX)
            self.perso.CON = self.affichage_set_point(LONGUEUR - LONGUEUR//4 + 0.5*text_width,LARGEUR//6 + 3*text_height,self.perso.CON)
            self.perso.INT = self.affichage_set_point(LONGUEUR - LONGUEUR//4 + 0.5*text_width,LARGEUR//6 + 4*text_height,self.perso.INT)
            self.perso.WIS = self.affichage_set_point(LONGUEUR - LONGUEUR//4 + 0.5*text_width,LARGEUR//6 + 5*text_height,self.perso.WIS)
            self.perso.CHA = self.affichage_set_point(LONGUEUR - LONGUEUR//4 + 0.5*text_width,LARGEUR//6 + 6*text_height,self.perso.CHA)

            # CHANGEMENTS NOM 

            text_width, text_height = ColderWeather.size("Choisir un Nom")
            self.draw_text('Choisir un Nom', ColderWeather, GREY, screen, LONGUEUR//4 - text_width // 2.5, LARGEUR//6)
            bouton_nom = pygame.Rect(LONGUEUR//4 - text_width // 2.5, LARGEUR//6+1.5*text_height,text_width, text_height)
            pygame.draw.rect(screen,(150,150,150),bouton_nom,1)

            if self.bouton_click(bouton_nom):
                self.perso.name = self.checkclavier((LONGUEUR//4 - text_width // 2.5),(LARGEUR//6+1.5*text_height),screen,bouton_nom)

            self.draw_text(self.perso.name,ColderWeather,WHITE,screen,LONGUEUR//4 - text_width // 2.5, LARGEUR//6+1.5*text_height)
            if self.perso.name != None:
                if len(self.perso.name) < 2 :
                    self.perso.name = None
                    self.Validation_screen("Erreur : Nom incorrect")
            # REFRESH + END EVENT

            running = self.checkevent()
            pygame.display.update()
    def Credit(self):
        running = True
        while running:
            screen.fill(LIGHT_GREY)
            #y= 0
            #for i in range(len(key)):
            #    if 50*i % LONGUEUR > LONGUEUR - 100:
            #        y +=1
            #    screen.blit(key[i].wpn_img,((50*i % LONGUEUR),(y*50)))
            
            #self.draw_text('Credit', Drifftype, WHITE, screen, 20, 20)
            floor = pygame.image.load(r'D:\Pygeon\Pygeon\Addon\Test\grass.png')
            floor.set_colorkey(BLACK)
            floor = pygame.transform.scale(floor,(3*floor.get_width()-4,3*floor.get_height()))
            #for y in range(30):
            y=0
            for i in range(30):
                screen.blit(floor,(i*floor.get_width()+100+floor.get_width()//2,y*floor.get_width()+(floor.get_height()-floor.get_width()//2)))
                
                screen.blit(floor,(100+i*floor.get_width(),100+y*floor.get_width()))
                screen.blit(floor,(100+(i+1)*floor.get_width(),100+y*floor.get_width()))
                #screen.blit(floor,(100+(i+2)*floor.get_width(),100+y*floor.get_width()))
                y+=1
            
            running = self.checkevent()
            pygame.display.update()
    def Option(self):
        running = True
        while running:
            global LONGUEUR
            global LARGEUR
            global screen
            global menu_background
            global coeff
            global coeff1
            global coeff2

            screen.fill(LIGHT_GREY)
            screen.blit(menu_background,(0,0))
            
            old_Largueur = LARGEUR
            # Partie Choisir résolution 
           
            text_width, text_height = ColderWeather.size("Choisir la résolution")
            self.draw_text('Choisir la resolution', ColderWeather, GREY, screen, LONGUEUR//4 - text_width // 2.5, LARGEUR//6)
            text_width, text_height = ColderWeather.size("    x    ")
            self.draw_text("    x    ", ColderWeather, GREY, screen,LONGUEUR//4 - text_width // 2, LARGEUR//6+text_height)

            text_width, text_height = ColderWeather.size("1000")
            bouton_resolution_Longeur = pygame.Rect(LONGUEUR//4 - 2*text_height, LARGEUR//6+text_height, text_width, text_height)
            bouton_resolution_Largueur = pygame.Rect(LONGUEUR//4 + 0.6*text_height, LARGEUR//6+text_height, text_width, text_height)

            pygame.draw.rect(screen,(150,150,150),bouton_resolution_Longeur,1)
            pygame.draw.rect(screen,(150,150,150),bouton_resolution_Largueur,1)

            if self.bouton_click(bouton_resolution_Longeur):
                LONGUEUR = self.checkclaviernum((LONGUEUR//4 - 2*text_height),(LARGEUR//6+text_height),screen,bouton_resolution_Longeur)
                screen = pygame.display.set_mode((LONGUEUR, LARGEUR))
                menu_background = pygame.transform.scale(menu_background,(LONGUEUR,LARGEUR))

            if self.bouton_click(bouton_resolution_Largueur):
                LARGEUR = self.checkclaviernum((LONGUEUR//4 + 0.6*text_height),(LARGEUR//6+text_height),screen,bouton_resolution_Largueur)
                screen = pygame.display.set_mode((LONGUEUR, LARGEUR))
                menu_background = pygame.transform.scale(menu_background,(LONGUEUR,LARGEUR))
                coeff = LARGEUR * coeff // old_Largueur
                coeff1 = LARGEUR * coeff1 // old_Largueur
                coeff2 = LARGEUR * coeff2 // old_Largueur


            self.draw_text("%d"%LONGUEUR,ColderWeather,WHITE,screen,(LONGUEUR//4 - 2*text_height), (LARGEUR//6+text_height))
            self.draw_text("%d"%LARGEUR,ColderWeather,WHITE,screen,(LONGUEUR//4 + 0.6*text_height), (LARGEUR//6+text_height))

            # Partie Curseur

            # Partie son 
            running = self.checkevent()
            pygame.display.update()
    def Quit(self):
        sys.exit()      
    def draw_text(self,text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect) 
    def affichage_set_point(self,x,y,cap):
       
        # CREATION/AFFICHAGE : BOUTON + et -

        t_width, t_height = Rumbletumble.size("+")
        self.draw_text('+', Rumbletumble, WHITE, screen, x,y)
        button_ = pygame.Rect(x,y+0.90*t_width, t_width, t_width)

        self.draw_text('-', Rumbletumble, WHITE, screen, x+3*t_width,y)
        button_2 = pygame.Rect(x+2.9*t_width,y+0.90*t_width, t_width, t_width)

        # REGLE POUR LES POINTS : https://www.d20pfsrd.com/basics-ability-scores/ability-scores

        if self.bouton_click(button_):
            if cap < 7 or cap >= 18:
                return cap
            elif self.perso.difficulty - self.point_attrib[cap - 7] < 0:
                return cap
            else:
                self.perso.difficulty = self.perso.difficulty - self.point_attrib[cap - 7]
                return cap + 1    
        if self.bouton_click(button_2):         
            if cap <= 7 or cap >= 19  :
                return cap
            else:
                self.perso.difficulty = self.perso.difficulty + self.point_attrib[cap - 8]
                return cap -1
        return cap
    def afficherinventaire(self,pack):
        running = True
        while running:
            #AFFICHAGE BACKGROUNDS 
            pack = self.perso.inventaire
            
            screen.fill(LIGHT_GREY)
            menu_inventaire = pygame.transform.scale(menu_background,(LONGUEUR//2,LARGEUR//2))
            screen.blit(menu_inventaire,(LONGUEUR//2-LONGUEUR//4,LARGEUR//2-LARGEUR//4))
            screen.blit(title,(LONGUEUR//2-LONGUEUR//7.5,LARGEUR//2-LARGEUR//3.5))
        
            #CREATION BOUTON INVENTAIRE
            bouton_test = dict()
            h=0
            for y in range(50,50+(pack.nb_x*50),50):
                for i in range(0,pack.nb_y,1):
                    bouton_test[h+i] = pygame.Rect(53*i+LONGUEUR//2-LONGUEUR//5, 1.05*y+LARGEUR//2-LARGEUR//7, 50, 50)
                h += pack.nb_y

            # AFFICHER LES BOUTONS INVENTAIRE   
            
            text_width, text_height = Drifftype.size("Inventaire")

            self.draw_text('Inventaire', ColderWeather, WHITE, screen, LONGUEUR//2-text_width//4,LARGEUR//2-text_height//2-LONGUEUR//6.3)

            for i in range(0,pack.nb_x*pack.nb_y):
                #pygame.draw.rect(screen,WHITE,bouton_test[i])
                pygame.draw.rect(screen,LIGHT_GREY,bouton_test[i],1)
            for i in range(0,pack.nb_x*pack.nb_y):
                if self.bouton_click(bouton_test[i]):
                    pygame.draw.rect(screen,(255,0,255),bouton_test[i]) 
                    if(pack.backpack[i] != None):
                        self.draw_text(key[pack.backpack[i]].wpn_name,Drifftype, WHITE, screen, 20,20)
                        
            

            # AFFICHER LES ITEMS INVENTAIRE
            h = 0
            for y in range(50,50+(pack.nb_x*50),50):
                for i in range(0,pack.nb_y,1):
                    if pack.backpack[h+i] != None :
                       screen.blit(key[pack.backpack[h+i]].wpn_img,(bouton_test[h+i].x, bouton_test[h+i].y))     
                h += pack.nb_y
            
            #CREATION BOUTONS JOUEURS ET AFFICHAGE
            bouton_arm = dict()

            for i in range(0,4):
                bouton_arm[i] = pygame.Rect(LONGUEUR//2-LONGUEUR//5+pack.nb_y*50*1.4, 1.05*(50*(i+1))+LARGEUR//2-LARGEUR//7,50,50)
               # pygame.draw.rect(screen,WHITE,bouton_arm[i])
                pygame.draw.rect(screen,LIGHT_GREY,bouton_arm[i],1)
                
            for i in range(0,2):
                bouton_arm[4+i] = pygame.Rect(LONGUEUR//2-LONGUEUR//5+pack.nb_y*50*1.6+53*i,1.05*50+LARGEUR//2-LARGEUR//7,50,50)
                pygame.draw.rect(screen,LIGHT_GREY,bouton_arm[4+i],1)
            
            for i in range(0,6):
                if self.perso.armor[i] != None:
                    screen.blit(key[self.perso.armor[i]].wpn_img,(bouton_arm[i].x,bouton_arm[i].y))
                    #self.draw_text(self.perso.armor[i].armor_name,Drifftype,WHITE,screen,100,100)  


            #AFFICHER ITEMS CORPS JOUEURS

            #DRAG AND DROP
            
            mx,my = pygame.mouse.get_pos()
            #button_drag = pygame.Rect(mx,my,50,50)
            #pygame.draw.rect(screen,RED,button_drag)
            mouse_slot = pack.nb_x*pack.nb_y

            # TEST : PRENDRE UN OBJECT DANS LA MOUSE

            for i in range(pack.nb_x*pack.nb_y):
                if self.bouton_click(bouton_test[i]):
                    if pack.backpack[i] != None and have_object == False:
                        pack.backpack[pack.nb_x*pack.nb_y] = pack.backpack[i]
                        pack.backpack[i] = None
                        last_moove = i
                        have_object = True
                if i < 6 and self.bouton_click(bouton_test[i]):
                    if self.perso.armor[i] != None and have_object == False:
                        pack.backpack[pack.nb_x*pack.nb_y] = self.perso.armor[i]
                        self.perso.armor[i] = None
                        last_moove = mouse_slot+i+1
                        have_object = True
            # TEST : DEPOSER UN OBJECT DE LA MOUSE VERS L INVENTAIRE 

            if pack.backpack[mouse_slot] != None:
                if any(pygame.mouse.get_pressed()):
                    have_object =True
                    screen.blit(key[pack.backpack[mouse_slot]].wpn_img,(mx,my))
                elif not(any(pygame.mouse.get_pressed())):
                    for i in range(pack.nb_y*pack.nb_x):
                        if bouton_test[i].collidepoint((mx,my)) :
                            pack.backpack[last_moove] = pack.backpack[i]
                            pack.backpack[i] = pack.backpack[mouse_slot]
                            pack.backpack[mouse_slot] = None
                            last_moove = mouse_slot
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
                        self.perso.armor[last_moove-mouse_slot-1] = pack.backpack[mouse_slot]
                        pack.backpack[mouse_slot] =None
                        have_object = False
            else:
                #pygame.draw.rect(screen,RED,button_drag)
                have_object = False

            running = self.checkevent()
            pygame.display.update()
    def bouton_click(self,bouton,constant_click = 0):
        # TEST : BOUTON EST CLIQUE ?
        mx, my = pygame.mouse.get_pos()
        return bouton.collidepoint((mx,my)) and self.click
    def checkevent(self):

        self.click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True     
        return True
    def checkclavier(self,x,y,screen,rect):
        running = True
        mot = ''
        all_key = (K_a,K_b,K_c,K_d,K_e,K_f,K_g,K_h,K_i,K_j,K_k,K_l,K_m,K_n,K_o,K_p,K_q,K_r,K_s,K_t,K_u,K_v,K_w,K_x,K_y,K_z)
        while running:
            screen.fill(LIGHT_GREY,rect)
            self.draw_text(mot,ColderWeather,WHITE,screen,x,y)
            
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
            pygame.display.update()
    def checkclaviernum(self,x,y,screen,rect):
        running = True
        mot = ''

        while running:
            screen.fill(LIGHT_GREY,rect)
            self.draw_text(mot,ColderWeather,WHITE,screen,x,y)
            
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
                    
            pygame.display.update()
    def printbackgrounds(self):
        screen.fill(LIGHT_GREY)
        global menu_background 
        menu_background = pygame.transform.scale(menu_background,(LONGUEUR,LARGEUR))
        screen.blit(menu_background,(0,0))     
    def load_game(self):
        running = True
        Choose = False
        self.click=False
        num = 0
        
        while running:

            self.printbackgrounds()
            #screen.blit(img_next,(LONGUEUR-338  ,LARGEUR-112))
            #screen.blit(img_next,(0,LARGEUR-112))

            button_save_1 = pygame.Rect(100,100,LONGUEUR//2-150,LARGEUR//2-150)
            button_save_2 = pygame.Rect(LONGUEUR//2,100,LONGUEUR//2-150,LARGEUR//2-150)
            button_save_3 = pygame.Rect(100,LARGEUR//2,LONGUEUR//2-150,LARGEUR//2-150)
            button_save_4 = pygame.Rect(LONGUEUR//2,LARGEUR//2,LONGUEUR//2-150,LARGEUR//2-150)

            if num == 1 : pygame.draw.rect(screen,RED,button_save_1)
            else : pygame.draw.rect(screen,LIGHT_GREY,button_save_1,1)
            if num == 2 : pygame.draw.rect(screen,RED,button_save_2)
            else : pygame.draw.rect(screen,LIGHT_GREY,button_save_2,1)
            if num == 3 : pygame.draw.rect(screen,RED,button_save_3)
            else : pygame.draw.rect(screen,LIGHT_GREY,button_save_3,1)
            if num == 4 : pygame.draw.rect(screen,RED,button_save_4)
            else : pygame.draw.rect(screen,LIGHT_GREY,button_save_4,1)

            text_width, text_height = ColderWeather.size("Sauvegarde 1")
            path = r'D:\\Pygeon\\Pygeon\\Save\\'
            if os.path.getsize(r'D:\Pygeon\Pygeon\Save\sauvegarde') > 0 :
                with open(r'D:\Pygeon\Pygeon\Save\sauvegarde','rb') as fichier:
                    mon_depickler = pickle.Unpickler(fichier)
                    inter = mon_depickler.load()
                    self.draw_text("Sauvegarde 1",ColderWeather,LIGHT_GREY,screen,button_save_1.width//2-text_width//4,100+text_height//4)
                    self.draw_text("Nom : %s"%(inter.name),ColderWeather,LIGHT_GREY,screen,button_save_1.width//2-text_width//4,200+text_height)
                    if self.bouton_click(button_save_1):
                        Choose = True
                        num = 1
                        choose_path = path + 'sauvegarde'
            else : self.draw_text("VIDE",ColderWeather,LIGHT_GREY,screen,button_save_1.width//2-text_width//4,100+text_height//4)

            if os.path.getsize(r'D:\Pygeon\Pygeon\Save\sauvegarde2') > 0 :
                with open(r'D:\Pygeon\Pygeon\Save\sauvegarde2','rb') as fichier:
                    mon_depickler = pickle.Unpickler(fichier)
                    inter = mon_depickler.load()
                    self.draw_text("Sauvegarde 2",ColderWeather,LIGHT_GREY,screen,(100-text_width//2+(LONGUEUR//2-100)//2)+LONGUEUR//2-100,100+text_height//4)
                    self.draw_text("Nom : %s"%(inter.name),ColderWeather,LIGHT_GREY,screen,(100-text_width//2+(LONGUEUR//2-100)//2)+LONGUEUR//2-100,200+text_height)
                    if self.bouton_click(button_save_2):
                        Choose = True
                        num = 2
                        choose_path = path + 'sauvegarde2'
            else : self.draw_text("VIDE",ColderWeather,LIGHT_GREY,screen,button_save_1.width//2-text_width//4,100+text_height//4)

            if os.path.getsize(r'D:\Pygeon\Pygeon\Save\sauvegarde3') > 0 :
                with open(r'D:\Pygeon\Pygeon\Save\sauvegarde3','rb') as fichier:
                    mon_depickler = pickle.Unpickler(fichier)
                    inter = mon_depickler.load()
                    self.draw_text("Sauvegarde 3",ColderWeather,LIGHT_GREY,screen,100-text_width//2+(LONGUEUR//2-100)//2,text_height//4+LARGEUR//2)
                    self.draw_text("Nom : %s"%(inter.name),ColderWeather,LIGHT_GREY,screen,100-text_width//2+(LONGUEUR//2-100)//2,text_height//4+LARGEUR//2+200)
                    if self.bouton_click(button_save_3):
                        Choose = True
                        num = 3
                        choose_path = path + 'sauvegarde3'
            else : self.draw_text("VIDE",ColderWeather,LIGHT_GREY,screen,button_save_1.width//2-text_width//4,100+text_height//4)
        
            if os.path.getsize(r'D:\Pygeon\Pygeon\Save\sauvegarde4') > 0 :
                with open(r'D:\Pygeon\Pygeon\Save\sauvegarde4','rb') as fichier:
                    mon_depickler = pickle.Unpickler(fichier)
                    inter = mon_depickler.load()
                    self.draw_text("Sauvegarde 4",ColderWeather,LIGHT_GREY,screen,(100-text_width//2+(LONGUEUR//2-100)//2)+LONGUEUR//2-100,text_height//4+LARGEUR//2)
                    self.draw_text("Nom : %s"%(inter.name),ColderWeather,LIGHT_GREY,screen,(100-text_width//2+(LONGUEUR//2-100)//2)+LONGUEUR//2-100,text_height//4+LARGEUR//2+200)
                    if self.bouton_click(button_save_4):
                        Choose = True
                        num = 4
                        choose_path = path + 'sauvegarde4'
            else : self.draw_text("VIDE",ColderWeather,LIGHT_GREY,screen,button_save_1.width//2-text_width//4,100+text_height//4)
            

            if (Choose):
                if self.creation_img_text_click(img_next,"Sauvegarder",ColderWeather,WHITE,0,0,right=1):
                    if self.perso.name == None:
                        self.Validation_screen("Erreur : Nom incorrect")
                    else:
                        self.click = False
                        text = 'Etes vous sur de vouloir sauvegarder ?'
                        if(self.Validation_screen(text)):
                            with open(choose_path,'wb') as fichier:
                                mon_pickler = pickle.Pickler(fichier)
                                mon_pickler.dump(self.perso)

                if self.creation_img_text_click(img_next,"Charger",ColderWeather,WHITE,0,0,left=1):
                    self.click = False
                    if (self.Validation_screen('Etes vous sur de vouloir charger ?')):
                        with open(choose_path,'rb') as fichier:
                            mon_depickler = pickle.Unpickler(fichier)
                            self.perso = mon_depickler.load()
                        return 

            running = self.checkevent()
            pygame.display.update()
    def Validation_screen(self,text):
        running = True
        while running:
            # Backgrounds :
            global img_backgrounds_warning 
            self.printbackgrounds()
            img_backgrounds_warning = pygame.transform.scale(img_backgrounds_warning,(LONGUEUR//2,LARGEUR//4))
            screen.blit(img_backgrounds_warning,(LONGUEUR//2-img_backgrounds_warning.get_width()//2,LARGEUR//2-img_backgrounds_warning.get_height()))
            screen.blit(exclamation,(LONGUEUR//2+img_backgrounds_warning.get_width()//2.5,LARGEUR//2-1.1*img_backgrounds_warning.get_height()))
            text_width, text_height = ColderWeather_small.size(text)
            self.draw_text(text,ColderWeather_small,WHITE,screen,LONGUEUR//2-text_width//2,LARGEUR//2-text_height//2-img_backgrounds_warning.get_height()//2)
            if self.creation_img_text_click(validation_button,"Valider",ColderWeather,WHITE,LONGUEUR//2,LARGEUR//2):
                return True
            running = self.checkevent() 
            pygame.display.update()
    def creation_img_text_click(self,img,text,font,color,x=0,y=0,button=1,left=0,right=0): 
        text_width, text_height = font.size(text)
        if img.get_width() < text_width:
            img = pygame.transform.scale(img,(text_width+50,img.get_height()))
        if(left):
            x = 0
            y = LARGEUR-img.get_height()
        elif(right):
            x = LONGUEUR-img.get_width()
            y = LARGEUR-img.get_height()
        else:
            x = x-img.get_width()//2
            y = y-img.get_height()//2
        screen.blit(img,(x,y))
        button_crea = pygame.Rect(x,y,img.get_width(),img.get_height())
        self.draw_text(text,font,color,screen,x+img.get_width()//2-text_width//2,y+img.get_height()//2-img.get_height()//2)
        if self.bouton_click(button_crea):
            return True

menu = Menu(player)

menu.game_loop()