
from items import Wikitem
import pygame
from pygame.locals import *
from settings.screen import *
from settings.police import Drifftype,ColderWeather,Rumbletumble,coeff,coeff1,coeff2,ColderWeather_small
from settings.load_img import *
from settings.color import *
from fonction import *
from entity import Entity
from items import Sword1,Sword10
key = list(Wikitem.keys())

class Inventaire():
    def __init__(self,nb_x,nb_y):
        self.nb_x = nb_x
        self.nb_y = nb_y
        self.nb_items = 0
        self.backpack = dict()
        self.poid_actuel = 0
        self.poid_max = 100
        self.have_object = False
        self.last_moove = 0
        self.mouse_slot = self.nb_x*self.nb_y
        self.bouton_test = dict()
        self.last_items_select = None
        for i in range(0,nb_x*nb_y+1):
            self.backpack[i] = None
    def ajouteritems(self,piece):
        
        if(self.nb_items >= (self.nb_x*self.nb_y) or (self.poid_actuel + piece.wheight ) > self.poid_max):
            return
        else:
            i=0
            while self.backpack[i] != None:
                i += 1
            last_moove = i
            self.backpack[last_moove] = Wikitem[piece]
            self.poid_actuel += piece.wheight
            self.nb_items += 1
    def enleveritems(self,piece):
        for i in range(len(self.backpack)):
            if self.backpack[i] == piece:
                self.backpack[i] = None
                self.nb_items -=1
                self.poid_actuel -= piece.wheight
    def print_inventory(self,perso,pos_x,pos_y,display,click,Is_perso = True,Is_shop = False,poid_max=0):
        #AFFICHAGE BACKGROUNDS 
        if Is_perso:
            pack = perso.inventaire
        else:
            pack = perso

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

            draw_text('Inventaire', ColderWeather, WHITE, display, pos_x//2-text_width//4,pos_y//2-text_height//2-menu_inventaire.get_height()//2.1)
            text_width, text_height = ColderWeather_small.size("Piece :  ")

            draw_text('Pieces : %i'%perso.argent,ColderWeather_small,WHITE,display,pos_x//2-text_width//2,pos_y//2+LARGEUR//6)
            draw_text('Poids : %i / %i'%(perso.inventaire.poid_actuel,perso.inventaire.poid_max),ColderWeather_small,WHITE,display,pos_x//2-LARGEUR//3,pos_y//2+LARGEUR//6)

                
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
                if perso.armor[i] != None:
                    display.blit(key[perso.armor[i]].wpn_img,(bouton_arm[i].x,bouton_arm[i].y))
                    #draw_text(self.perso.armor[i].armor_name,Drifftype,WHITE,display,100,100)  


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
            display.blit(pygame.transform.scale(board_medium,(LONGUEUR//4,LARGEUR//2)),(0,0))

            display.blit(pygame.transform.scale(key[pack.backpack[mouse_slot]].wpn_img,(100,100)),(50,50))  
            draw_text(key[pack.backpack[mouse_slot]].wpn_name,ColderWeather_small,WHITE,display,200,70)
            draw_text("Description : %s"%key[pack.backpack[mouse_slot]].info,ColderWeather_small,WHITE,display,200,90)
            draw_text("Prix : %i"%key[pack.backpack[mouse_slot]].value,ColderWeather_small,WHITE,display,100,150)
            draw_text("Poids : %i"%key[pack.backpack[mouse_slot]].wheight,ColderWeather_small,WHITE,display,100,250)
            draw_text("Dommage : %i"%key[pack.backpack[mouse_slot]].dmg,ColderWeather_small,WHITE,display,100,350)

        else:
            have_object = False
            #display.blit(pygame.transform.scale(board_medium,(LONGUEUR//4,LARGEUR//2)),(0,0))

        i = 0
        while pack.backpack[i] != None:
            i += 1
        last_moove = i

        for i in range(pack.nb_x*pack.nb_y):
            if bouton_click(bouton_test[i],display,click):
                if pack.backpack[i] != None and have_object == False:
                    pack.backpack[mouse_slot] = pack.backpack[i]
                    pack.backpack[i] = None
                    last_moove = i
                    have_object = True
            if Is_perso:
                if i < 6 and bouton_click(bouton_arm[i],display,click):
                    if perso.armor[i] != None and have_object == False:
                        pack.backpack[pack.nb_x*pack.nb_y] = perso.armor[i]
                        perso.armor[i] = None
                        last_moove = mouse_slot+i+1
                        have_object = True
        if Is_shop :Is_buying = creation_img_text_click(img_next,"Acheter",ColderWeather,WHITE,display,click,pos_x//2+img_next.get_width()//2,pos_y//2,Click=False) and pack.backpack[mouse_slot] != None
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
                                pack.backpack[last_moove] = perso.armor[i]
                                perso.armor[i] = pack.backpack[mouse_slot]
                                pack.backpack[mouse_slot] = None
                                last_moove = mouse_slot
                if last_moove <= mouse_slot:
                    pack.backpack[last_moove] = pack.backpack[mouse_slot]
                    pack.backpack[mouse_slot] = None
                    have_object = False
                else:
                    if Is_perso:
                        perso.armor[last_moove-mouse_slot-1] = pack.backpack[mouse_slot]
                        pack.backpack[mouse_slot] =None
                        have_object = False
        else:
            last_moove = -1
            #pygame.draw.rect(screen,RED,button_drag)
            have_object = False  
    def print_inventory_bis(self,pos_x,pos_y,main=True,mouse=False,print_poids=True):
        display = pygame.Surface((500,400))
        x=display.get_width()//2
        y_=display.get_height()//2
        display.blit(pygame.transform.scale(img_inventaire,(500,400)),(0,0))
        display.set_colorkey(BLACK)
        
        if self.backpack[self.mouse_slot] != None:
            self.last_items_select = self.backpack[self.mouse_slot]
        
       


        mx,my = pygame.mouse.get_pos()
        mx_display =  mx  - pos_x
        my_display =  my  - pos_y
        h=0
        mouse_slot = self.nb_x*self.nb_y
        
        y=0
        for y in range(self.nb_x):
            for i in range(self.nb_y):
                self.bouton_test[h+i] = pygame.Rect(60*y+x-60*self.nb_x//2, 60*i+y_-60*self.nb_y//2, 50, 50)
                pygame.draw.rect(display,(0,0,1),self.bouton_test[h+i],1)
            h += self.nb_y
        i=0
        screen.blit(display,(pos_x,pos_y))
        if self.last_items_select != None:
            display_info_items = pygame.Surface((250,200))
            display_info_items.blit(pygame.transform.scale(img_inventaire,(250,200)),(0,0))
            display_info_items.set_colorkey(BLACK)
            display_info_items.blit(pygame.transform.scale(key[self.last_items_select].wpn_img,(75,75)),(10,10))
            draw_text("Valeur : %i"%key[self.last_items_select].value,ColderWeather_small,WHITE,display_info_items,95,0)
            draw_text("Poids : %i"%key[self.last_items_select].wheight,ColderWeather_small,WHITE,display_info_items,95,50)
            if key[self.last_items_select].wpn_type == 4:
                draw_text("Attack : %i"%key[self.last_items_select].dmg,ColderWeather_small,WHITE,display_info_items,95,100)
            
            screen.blit(display_info_items,(pos_x,pos_y-200))
        if print_poids:
            display_poids = pygame.Surface((200,50))
            display_poids.blit(pygame.transform.scale(img_inventaire,(200,50)),(0,0))
            display_poids.set_colorkey(BLACK)
            draw_text("Poids : %i / %i"%(self.poid_actuel,self.poid_max),ColderWeather_small,WHITE,display_poids,10,5)
            screen.blit(display_poids,(pos_x+500,pos_y+400))
        for i in range(self.nb_x*self.nb_y):
            if self.backpack[i] != None :
                screen.blit(key[self.backpack[i]].wpn_img,(self.bouton_test[i].x+pos_x, self.bouton_test[i].y+pos_y))
        if main:
            if self.backpack[mouse_slot] != None :
                self.have_object = True
                screen.blit(key[self.backpack[mouse_slot]].wpn_img,(mx,my))
            else:
                self.have_object = False
        i = 0
        while self.backpack[i] != None:
            i += 1
        self.last_moove = i
        if not mouse:
            for i in range(self.nb_x*self.nb_y):
                if self.bouton_test[i].collidepoint(mx_display,my_display):
                    if self.backpack[i] != None and self.have_object == False:
                        self.backpack[mouse_slot] = self.backpack[i]
                        self.backpack[i] = None
                        self.last_moove = i
                        self.have_object = True
        if self.backpack[mouse_slot] != None:
            if not(any(pygame.mouse.get_pressed())):
                for i in range(self.nb_y*self.nb_x):
                    if self.bouton_test[i].collidepoint((mx_display,my_display)) :
                        self.backpack[self.last_moove] = self.backpack[i]
                        self.backpack[i] = self.backpack[mouse_slot]
                        self.backpack[mouse_slot] = None
                        self.have_object = False
                        self.last_moove = mouse_slot
                if self.last_moove <= mouse_slot:
                    self.backpack[self.last_moove] = self.backpack[mouse_slot]
                    self.backpack[mouse_slot] = None
                    self.have_object = False
        else:
            self.last_moove = -1
    def loot_inventory(self,pos_x,pos_y,inv):
        mx,my = pygame.mouse.get_pos()
        mx_inv = mx - 500
        my_inv = my - 500
        click=False
        if self.backpack[self.mouse_slot] != None:
            self.have_object = True
            for i in range(inv.mouse_slot):
                if not(any(pygame.mouse.get_pressed())) and inv.bouton_test[i].collidepoint(mx_inv,my_inv):
                    if inv.backpack[i] == None:
                        inv.backpack[i] = self.backpack[self.mouse_slot]
                        self.backpack[self.mouse_slot] = None
                        self.have_object = False
        else:
            self.have_object = False
        inv.print_inventory_bis(500,500,mouse=self.have_object)
        self.print_inventory_bis(pos_x,pos_y)

class Shop(Entity):
    def __init__(self,inventory,pos_x,pos_y,img,name,which_type,animation_dict=None,talking=None,size=(0,0)):
        Entity.__init__(self,pos_x,pos_y,img,name,which_type,animation_dict,talking,size)
        self.show = True
        self.inventory = inventory
    def print_shop(self,perso,click,just_print = False):
        display_talk = pygame.Surface((1800,1080))
        display_talk.set_colorkey((0,0,0))
        i=0
        mouse_slot = self.inventory.mouse_slot
        mx,my = pygame.mouse.get_pos()
        mx_display= mx -1000
        my_display = my - 200
        mx_display_2 = mx -0
        my_display_2 = my -200
        
        if self.inventory.backpack[mouse_slot] != None:
            if not(any(pygame.mouse.get_pressed())):
                for i in range(mouse_slot):
                    if perso.inventaire.bouton_test[i].collidepoint(mx_display,my_display):
                        if perso.argent - key[self.inventory.backpack[mouse_slot]].value > 0 :
                            if Validation_screen("etes vous sur de vouloir acheter cette items ?",display_talk,click):
                                perso.argent -= key[self.inventory.backpack[mouse_slot]].value
                                perso.inventaire.poid_actuel += key[self.inventory.backpack[mouse_slot]].wheight
                                perso.inventaire.backpack[i] = self.inventory.backpack[mouse_slot]
                                self.inventory.backpack[mouse_slot] = None
                                self.inventory.have_object = False
                        else:
                            Validation_screen("Vous n'avez pas assez d'argent !",display_talk,click)
        i=0
        if perso.inventaire.backpack[mouse_slot] != None:
            if not(any(pygame.mouse.get_pressed())):
                for i in range(mouse_slot):
                    if self.inventory.bouton_test[i].collidepoint(mx_display_2,my_display_2):
                        if Validation_screen("etes vous sur de vouloir vendre cette items ?",display_talk,click):
                            perso.argent += key[perso.inventaire.backpack[mouse_slot]].value
                            perso.inventaire.poid_actuel -= key[perso.inventaire.backpack[mouse_slot]].wheight
                            if self.inventory.backpack[i] == None:
                                self.inventory.backpack[i] = perso.inventaire.backpack[mouse_slot]
                            else:
                                self.inventory.ajouteritems(key[perso.inventaire.backpack[mouse_slot]])
                            perso.inventaire.backpack[mouse_slot] = None
                            perso.inventaire.have_object = False


       
        self.inventory.print_inventory_bis(0,200,main=False,mouse=perso.inventaire.have_object,print_poids=False)
        #perso.inventaire.print_inventory_bis(1000,200,main=False,mouse=self.inventory.have_object)
        perso.print_equipement(1000,700,1000,200,mouse=self.inventory.have_object)
        if perso.inventaire.backpack[mouse_slot] != None:
            screen.blit(key[perso.inventaire.backpack[mouse_slot]].wpn_img,(mx,my))        
        if self.inventory.backpack[mouse_slot] != None:
            screen.blit(key[self.inventory.backpack[mouse_slot]].wpn_img,(mx,my))
        screen.blit(display_talk,(0,0))
inv = Inventaire(7,5)
inv.ajouteritems(Sword1)
inv.ajouteritems(Sword10)
running = True
click = False
'''while running:
    inv.print_inventory_bis()
    pygame.display.update()
    running,click = basic_checkevent(click)
'''

