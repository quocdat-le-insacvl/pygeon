import pygame
from entity import Entity
from settings.load_img import pixel_red
from pygame.locals import *
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
    def move_player(self,map):
        self.refresh_animation_and_mouvement()
        self.swap = False
        self.entity_near = False
        possible = True
        for x in map.collision_entity:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.entity_near = True
        for x in map.collision_change_camera:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.swap = True
        for x in map.collision:
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