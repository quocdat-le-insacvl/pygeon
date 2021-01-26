
from items import Wikitem
import pygame
from pygame.locals import *
from settings.screen import *
from settings.police import Drifftype,ColderWeather,Rumbletumble,coeff,coeff1,coeff2,ColderWeather_small
from settings.load_img import *
from settings.color import *
from fonction import *
from entity import Entity,Collide_box
from items import *

key = list(Wikitem.keys())

class Inventaire():
    def __init__(self,nb_x,nb_y):
        self.nb_x = nb_x
        self.nb_y = nb_y
        self.nb_items = 0
        self.backpack = dict()
        self.poid_actuel = 0
        self.poid_max = 20000000
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
    def is_empty(self):
        for i in range(0,self.nb_x*self.nb_y+1):
            if self.backpack[i] != None:
                return False
        return True
    def print_inventory_bis(self,pos_x,pos_y,main=True,mouse=False,print_poids=True,print_info_on_mouse = False,click=False):
        display = pygame.Surface((60*(self.nb_x+2),60*(self.nb_y+2)))
        x=display.get_width()//2
        y_=display.get_height()//2
        display.blit(pygame.transform.scale(img_inventaire,(x*2,y_*2)),(0,0))
        display.set_colorkey(BLACK)



        display_about_items = pygame.Surface((350,200))
        display_about_items.blit(pygame.transform.scale(img_inventaire,(350,200)),(0,0))
        display_about_items.set_colorkey(BLACK)
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
        i=1
        screen.blit(display,(pos_x,pos_y))
        #AFFICHER L INVENTAIRE SUR L ECRAN
        for i in range(self.nb_x*self.nb_y):
            if self.backpack[i] != None :
                screen.blit(key[self.backpack[i]].wpn_img,(self.bouton_test[i].x+pos_x, self.bouton_test[i].y+pos_y))

        if self.last_items_select != None:
            display_info_items = pygame.Surface((350,200))
            display_info_items.blit(pygame.transform.scale(img_inventaire,(350,200)),(0,0))
            display_info_items.set_colorkey(BLACK)
            draw_text("Valeur : %i"%key[self.last_items_select].value,ColderWeather_small,WHITE,display_info_items,95,10)
            draw_text("Poids : %i"%key[self.last_items_select].wheight,ColderWeather_small,WHITE,display_info_items,95,40)
            draw_text("Type : %s"%key[self.last_items_select].wpn_name,ColderWeather_small,WHITE,display_info_items,95,70)
            

            if key[self.last_items_select].wpn_type == 4:
                draw_text("Attack : %i"%key[self.last_items_select].dmg,ColderWeather_small,WHITE,display_info_items,95,100)
            elif key[self.last_items_select].wpn_type == 6:
                pass
            elif key[self.last_items_select].wpn_type == 9:
                draw_text("Heal : %i"%key[self.last_items_select].heal,ColderWeather_small,WHITE,display_info_items,95,100)
            else:
                draw_text("Armor : %i"%key[self.last_items_select].armor_bonus,ColderWeather_small,WHITE,display_info_items,95,100)
                draw_text("Dex Bonus : %i"%key[self.last_items_select].dex_bonus,ColderWeather_small,WHITE,display_info_items,95,130)
                draw_text("Speed : %i"%key[self.last_items_select].speed,ColderWeather_small,WHITE,display_info_items,95,160)
            if key[self.last_items_select].info != "":
                lenght_text,y_use = ColderWeather_small.size(key[self.last_items_select].info)
                if lenght_text > 250:
                    text = key[self.last_items_select].info.split(' ')
                    total_size = 30
                    ligne = 10
                    for i in range (len(text)):
                        draw_text(text[i],ColderWeather_small,BURGUNDY,display_about_items,total_size,ligne)
                        total_size += ColderWeather_small.size(text[i])[0] + ColderWeather_small.size(" ")[0]
                        if total_size > 270:
                            ligne +=30
                            total_size = 30
                if not print_info_on_mouse:
                    screen.blit(display_about_items,(pos_x+250,pos_y-200))
                else:
                    screen.blit(display_about_items,(mx+350,my))
            else:
                screen.blit(display_about_items,(pos_x+250,pos_y-200))
            if not print_info_on_mouse:
                screen.blit(display_info_items,(pos_x-100,pos_y-200))
                screen.blit(pygame.transform.scale(key[self.last_items_select].wpn_img,(75,75)),(pos_x-100+10,pos_y-200+10))
            else:
                screen.blit(display_info_items,(mx,my))
                screen.blit(pygame.transform.scale(key[self.last_items_select].wpn_img,(75,75)),(mx+10,my+10))
                
        # AFFICHER POIDS INVENTAIRE
        
        if print_poids:
            display_poids = pygame.Surface((200,50))
            display_poids.blit(pygame.transform.scale(img_inventaire,(200,50)),(0,0))
            display_poids.set_colorkey(BLACK)
            draw_text("Poids : %i / %i"%(self.poid_actuel,self.poid_max),ColderWeather_small,WHITE,display_poids,10,5)
            screen.blit(display_poids,(pos_x,pos_y+y_*2))
        i=0

       


        # SI MAIN AFFICHER L INVENTAIRE SELECTIONNER SUR LA SOURIS

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

        # SI RIEN DANS LA MAIN D AUTRE INVENTAIRE, DRAG AND DROP CLASSIQUE

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
    def loot_inventory(self,pos_self_x,pos_self_y,pos_other_x,pos_other_y,inv,print_info_on_mouse=False):
        mx,my = pygame.mouse.get_pos()
        mx_inv = mx - pos_other_x
        my_inv = my - pos_other_y
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
        inv.print_inventory_bis(pos_other_x,pos_other_y,mouse=self.have_object,print_info_on_mouse=print_info_on_mouse)
        self.print_inventory_bis(pos_self_x,pos_self_y,print_info_on_mouse=print_info_on_mouse)
    def add_random_drop(self,number):
        for i in range(number):
            j = random.randint(0,len(Droppable)-10)
            self.ajouteritems(Droppable[j])


class Shop(Entity):
    def __init__(self,inventory,pos_x,pos_y,img,name,which_type,animation_dict=None,talking=None,size=(0,0),size_collide_box=1):
        Entity.__init__(self,pos_x,pos_y,img,name,which_type,animation_dict,talking,size,size_collide_box=1)
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
        mx_display_2 = mx -100
        my_display_2 = my -200
        
        if self.inventory.backpack[mouse_slot] != None:
            if not(any(pygame.mouse.get_pressed())):
                for i in range(mouse_slot):
                    if perso.inventaire.bouton_test[i].collidepoint(mx_display,my_display):
                        if perso.argent - key[self.inventory.backpack[mouse_slot]].value > 0 :
                            if Validation_screen("etes vous sur de vouloir acheter cette items ?",display_talk,click,choice=True):
                                perso.argent -= key[self.inventory.backpack[mouse_slot]].value
                                perso.inventaire.poid_actuel += key[self.inventory.backpack[mouse_slot]].wheight
                                perso.inventaire.backpack[i] = self.inventory.backpack[mouse_slot]
                                # self.inventory.backpack[mouse_slot] = None
                                self.inventory.have_object = False
                        else:
                            Validation_screen("Vous n'avez pas assez d'argent !",display_talk,click)
        i=0
        if perso.inventaire.backpack[mouse_slot] != None:
            if not(any(pygame.mouse.get_pressed())):
                for i in range(mouse_slot):
                    if self.inventory.bouton_test[i].collidepoint(mx_display_2,my_display_2):
                        if Validation_screen("etes vous sur de vouloir vendre cette items ?",display_talk,click,choice=True):
                            perso.argent += key[perso.inventaire.backpack[mouse_slot]].value
                            perso.inventaire.poid_actuel -= key[perso.inventaire.backpack[mouse_slot]].wheight
                            if self.inventory.backpack[i] == None:
                                self.inventory.backpack[i] = perso.inventaire.backpack[mouse_slot]
                            else:
                                self.inventory.ajouteritems(key[perso.inventaire.backpack[mouse_slot]])
                            perso.inventaire.backpack[mouse_slot] = None
                            perso.inventaire.have_object = False


       
        self.inventory.print_inventory_bis(100,200,main=False,mouse=perso.inventaire.have_object,print_poids=False)
        #perso.inventaire.print_inventory_bis(1000,200,main=False,mouse=self.inventory.have_object)
        perso.print_equipement(1000,700,1200,200,mouse=self.inventory.have_object)
        if perso.inventaire.backpack[mouse_slot] != None:
            screen.blit(key[perso.inventaire.backpack[mouse_slot]].wpn_img,(mx,my))        
        if self.inventory.backpack[mouse_slot] != None:
            screen.blit(key[self.inventory.backpack[mouse_slot]].wpn_img,(mx,my))
        screen.blit(display_talk,(0,0))
inv = Inventaire(7,5)
inv.ajouteritems(Sword1)
inv.ajouteritems(Sword10)
inv.ajouteritems(A_Armor04)
inv.ajouteritems(A_Shoes01)
inv.ajouteritems(Ac_Medal1)
inv.ajouteritems(C_Elm01)
inv.ajouteritems(C_Elm04)
inv.ajouteritems(E_Metal02)
inv.ajouteritems(Strawberry)
inv.ajouteritems(Mace1)
inv.ajouteritems(Bow1)
inv.ajouteritems(Spear11)
inv.ajouteritems(Key1)
#inv.add_random_drop(random.randint(1,5))

running = True
click = False


