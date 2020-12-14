
from items import Wikitem
import pygame
from pygame.locals import *
from settings.screen import *
from settings.police import Drifftype,ColderWeather,Rumbletumble,coeff,coeff1,coeff2,ColderWeather_small
from settings.load_img import *
from settings.color import *
from fonction import *
from entity import Entity
key = list(Wikitem.keys())

class Inventaire():
    def __init__(self,nb_x,nb_y):
        self.nb_x = nb_x
        self.nb_y = nb_y
        self.nb_items = 0
        self.backpack = dict()
        self.poid_actuel = 0
        self.poid_max = 100
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
    def print_inventory(self,perso,pos_x,pos_y,display,click,Is_perso = True,Is_shop = False):
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

class Shop(Entity):
    def __init__(self,inventory,pos_x,pos_y,img,name,which_type,animation_dict=None,talking=None,size=(0,0)):
        Entity.__init__(self,pos_x,pos_y,img,name,which_type,animation_dict,talking,size)
        self.show = True
        self.inventory = inventory
    def print_shop(self,perso,click,just_print = False):
        running = True
        display = pygame.Surface((1980,1024))
        while running:
            display.fill(LIGHT_GREY)
            items = None
            items = self.inventory.print_inventory(self.inventory,display.get_width(),display.get_height()//2,display,click,Is_perso=False,Is_shop=True)
            if items != None:
                print(key[items].value)
                if (perso.argent - key[items].value) < 0 :
                    Validation_screen("Vous avez pas assez d'argent",display,click)
                    #self.print_inventory(perso2.inventaire,display.get_width(),1.5*display.get_height())

                    self.inventory.ajouteritems(key[items])
                else:
                    perso.argent -= key[items].value
                    perso.inventaire.ajouteritems(key[items])
            perso.inventaire.print_inventory(perso,display.get_width(),1.5*display.get_height(),display,click)


            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            pygame.display.update()
            running,click = basic_checkevent(click)






