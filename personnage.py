import pygame
from entity import Entity
from settings.load_img import pixel_red, ava_perso
from pygame.locals import *
from items import Sword1,Sword10,Wikitem
from inventory import Inventaire
from settings.screen import screen
from fonction import *
key = list(Wikitem.keys())
pixel_mask = pygame.mask.from_surface(pixel_red)
class Perso():
    def __init__(self,STR,DEX,CON,INT,WIS,CHA,hp,hp_max,inventaire,argent = 0,name=None,classe=None,level=1,xp=0):
        self.name=name
        self.classe = classe
        self.level = level
        self.xp = xp 
        self.hp = hp
        self.hp_max = hp_max
        self.difficulty = 10
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        self.inventaire = inventaire
        self.argent = argent
        self.poid_actuel = 0
        self.poid_max = 300
        self.armor = dict()
        self.avata = ava_perso
        self.tour = False
        self.resultat = 0
        
        for i in range(0,6):     # 0 : HEAD 1 : TORSE 2 : COUE  3 BOTTE 4 : MAIN GAUCHE : 5 MAIN DROITE
            self.armor[i] = None   
        self.pos_x = 9000
        self.pos_y = 2000
    def levelupchange(self):
        #SOURCE https://www.d20pfsrd.com/Gamemastering/#Table-Experience-Point-Awards
        
        #lvl_life = (1000,3000,6000,10500,16000,23500,33000,46000,62000,82000,108000,140000,185000,240000,315000,410000,530000,685000,880000)
        lvl_XP = (400,600,800,1200,1600,2400,3200,4800,6400,9600,12800,19200,25600,38400,51200,76800,102400,153600,204800,307200,409600,614400,819200,1228800,1638400,2457600,3276800,4915200,6553600,9830400)
        while self.xp >= lvl_XP[self.level-1]:
            self.level += 1

class Perso_game(Perso,Entity):
    def __init__(self,STR,DEX,CON,INT,WIS,CHA,hp,hp_max,inventaire,img,pos_x,pos_y,player_animation = None ,argent = 0,name=None,classe=None,level=1,xp=0):
        Entity.__init__(self,pos_x,pos_y,img,name,"Player",player_animation)
        Perso.__init__(self,STR,DEX,CON,INT,WIS,CHA,hp,hp_max,inventaire,argent,level,xp)
        self.case_connue = []
        self.mask_surface = pygame.Surface((img.get_width()-40,10))
        self.mask_surface.fill((255,0,0))
        self.masks = pygame.mask.from_surface(self.mask_surface)
        self.swap = False
        self.entity_near = False
        self.swap_entity = False
        self.mouvement = [False,False,False,False]
        self.deplacement = [0,0]
    def refresh_animation_and_mouvement(self):
        if self.mouvement[0]:
            self.deplacement = [10,-5]
            self.type_animation = "walk_top"
        elif self.mouvement[1]:
            self.deplacement = [-10,+5]
            self.type_animation = "walk_bottom"
        elif self.mouvement[2]:
            self.deplacement = [+10,+5]
            self.type_animation = "walk_right"
        elif self.mouvement[3]:
            self.deplacement = [-10,-5]
            self.type_animation = "walk_left"
        else:
            self.deplacement = [0,0]
            self.type_animation = "idle"     
    def move_player(self,dict_collision):
        self.refresh_animation_and_mouvement()
        self.swap = False
        self.entity_near = False
        self.swap_entity = False
        possible = True
        for x in dict_collision['change_camera_entity']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.swap_entity = True
        for x in dict_collision['collision_entity']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.entity_near = True
        for x in dict_collision['collision_change_camera']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.swap = True
        for x in dict_collision['collision']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                possible = False
        if possible:
            self.pos_x += self.deplacement[0]
            self.pos_y += self.deplacement[1]
        """def move_player():
        Permet de déplcer le player_rect de mouvement check si le joeurs ne collide pas avec un chamgement de caméra ou une entité"""
    def check_user(self,event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.mouvement[0] = True
            elif event.key == K_DOWN:
                self.mouvement[1] = True
            elif event.key == K_RIGHT:
                self.mouvement[2] = True
            elif event.key == K_LEFT:
                self.mouvement[3] = True
                
        if event.type == KEYUP:
            if event.key == K_UP:
                self.mouvement[0] = False
            if event.key == K_DOWN:
                self.mouvement[1] = False
            if event.key == K_RIGHT:
                self.mouvement[2] = False
            if event.key == K_LEFT:
                self.mouvement[3] = False

    
        '''def interact_with_entity(self,entity):
        Effectue les actions en fonctions du type de l'entité la fonction est à compléter elle ne traite pas tout les types entités''' 
    def transform_display_for_combat(self):
        self.display = pygame.Surface((300,300))
        self.display.set_colorkey((0,0,0))
    def transform_display_for_map(self):
        self.display = pygame.Surface((self.img.get_width(),self.img.get_height()))
        self.display.set_colorkey((0,0,0))
    def print_equipement(self,pos_x,pos_y):
        
        display = pygame.Surface((250,200))
        display.set_colorkey(BLACK)
        x = 125
        y_ = 100
        display.blit(pygame.transform.scale(img_inventaire,(250,200)),(0,0))
        self.img.set_alpha(50)
        display.blit(self.img,(250//2-self.img.get_width()//2,100-self.img.get_height()//2))
        bouton_arm = dict()
        mouse_slot = self.inventaire.nb_x * self.inventaire.nb_y
        mx,my = pygame.mouse.get_pos()
        mx_display = mx - pos_x
        my_display = my - pos_y

        for i in range(0,4):
            bouton_arm[i] = pygame.Rect(x-25, 50*i,50,50)
            pygame.draw.rect(display,(0,0,1),bouton_arm[i],1)   
        for i in range(0,2):
            bouton_arm[4+i] = pygame.Rect(25+i*150,75,50,50)
            pygame.draw.rect(display,(0,0,1),bouton_arm[4+i],1)  
        screen.blit(display,(pos_x,pos_y))
        #screen.blit(display,(0,0))
        for i in range(0,6):
            if self.armor[i] != None:
                screen.blit(key[self.armor[i]].wpn_img,(bouton_arm[i].x+pos_x,bouton_arm[i].y+pos_y))
        i=0
        if self.inventaire.have_object == False:
            for i in range(6):
                if bouton_arm[i].collidepoint((mx_display,my_display)):
                    self.inventaire.backpack[mouse_slot] = self.armor[i]
                    self.armor[i] = None
                    self.inventaire.last_moove = mouse_slot+i+1
                    self.inventaire.have_object = True
        i=0
        if self.inventaire.backpack[mouse_slot] != None:
            if any(pygame.mouse.get_pressed()):
                self.have_object =True
                #screen.blit(key[self.inventaire.backpack[mouse_slot]].wpn_img,(mx,my))
            elif not(any(pygame.mouse.get_pressed())):
                for i in range(0,6):
                    if bouton_arm[i].collidepoint((mx_display,my_display)) and key[self.inventaire.backpack[mouse_slot]].wpn_type == i:
                        self.inventaire.backpack[self.inventaire.last_moove] = self.armor[i]
                        self.armor[i] = self.inventaire.backpack[mouse_slot]
                        self.inventaire.backpack[mouse_slot] = None
                        self.inventaire.last_moove = mouse_slot
                        self.inventaire.have_object = False
        else:
            self.inventaire.have_object = False
            self.inventaire.last_moove = -1
        self.inventaire.print_inventory_bis(500,500,main=False)
        if self.inventaire.backpack[mouse_slot] != None:
            screen.blit(key[self.inventaire.backpack[mouse_slot]].wpn_img,(mx,my))
