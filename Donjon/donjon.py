from entity import Collide_box, Chest
from monster import Monster
from Donjon.piece import Piece
import pygame
from personnage import Perso
from pygame.time import Clock
from Donjon.camera import Camera
from custum_map_ import list_entity_animation,list_npc
from script import player_for_save,player_3,list_static_entity,player_2,playerbis,sorcerer,sorcerer_2,sorcerer_3
from settings.load_img import *
import os
import numpy
import random
from fog import Fog
from minimap import Minimap
from combat import Combat
from inventory import Inventaire
from items import Wikitem
from math import sqrt
list_img_monstre = [list_entity_animation[0],list_entity_animation[1],list_entity_animation[2],list_entity_animation[3],list_entity_animation[4]]
list_animation_monstre = [demon_1_animation,demon_animation,squelton_animation,wizard_animation,dark_wizard_animation]
list_decalage_monstre= [[-80,30],[-90,40],[-30,-10],[-20,0],[-110,+50]]
list_size_monstre = [(500,400),(500,400),(300,300),(300,300),(700,700)]
key = list(Wikitem.keys())

clock = pygame.time.Clock()
#classe permettant de créer un donjon
#un donjon contient un ensemble de piece ainsi que des monstres, des loots, etc...
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
class Donjon():

    #difficulte pas encore implementee, soon
    #screen : la surface surlaquelle print les salles du donjons
    #peros : self.personnage que l'on doit déplacer -> sert pour les collisions
    #nbreEtage : De base on est a 3, mais on peut faire +
    def __init__(self,difficulte,screen,perso,game=None,nbreEtage=2):

        self.game = game
        self.difficulty = difficulte
        self.nbEtage = nbreEtage
        self.pieces = []
        self.screen = screen
        self.actuel = 0 # piece actuelle
        self.listekey = dict()
        self.perso = perso
        self.interaction = 0
        self.fogs=[]
        self.liste_monstre = [[]]
        self.liste_coffre = []
        for i in range(self.nbEtage):
            self.pieces.append(Piece(screen))
            self.liste_monstre.append([])

        #i=0 -> etage 0 ; i=2 -> etage 1 ...

        #les etages 0 et 3 n'ont qu'un escalier
        
        self.pieces[0].max_graphique[8] = self.pieces[self.nbEtage-1].max_graphique[16] = 1
        self.pieces[self.nbEtage-1].max_graphique[8] = self.pieces[0].max_graphique[16] = 0
        self.pieces[0].max_graphique[15] = 1
        self.pieces[-1].max_graphique[17] = 1
        for i in range(1,nbreEtage-1):
            self.pieces[i].max_graphique[8]=self.pieces[i].max_graphique[16]=1
            self.pieces[i].max_graphique[15] = 0
        
        
        self.listekey = {pygame.K_UP : False, pygame.K_DOWN : False, pygame.K_RIGHT:False,pygame.K_LEFT:False,pygame.K_SPACE:False,pygame.K_ESCAPE:False}


    def creationDonjon(self):
        j=0
        for salle in self.pieces:
            
            direction = 0
            nbreHaut = 0
            salle.linked = []
            for i in range(3):
                direction = random.randint(0,2)
                if direction==0:salle.linked.append('Gauche')
                if direction ==1:salle.linked.append('Droite')
                if direction==2 and nbreHaut <1:
                    nbreHaut+=1
                    salle.linked.append('Haut')

            #salle.linked=['Haut','Gauche','Droite'
            salle.create_linked(3)
            salle.createRoom()
            salle.linkedPiece()
            i=0
            doEB,doEH,doTe=False,False,False
            if j>0:
                doEB = True
            if j < len(self.pieces)-1:
                doEH=True
            if j== len(self.pieces)-1:
                doTe=True
            
            while salle.check_jouabilite(doEH=doEH,doEB=doEB,doTe=doTe)!= True:
                    
                salle.createRoom(start=True)
                salle.linkedPiece(check_pieces=True) 
                #salle = Piece(self.screen)
                #salle.linked = ['Haut','Haut','Gauche','Gauche','Droite','Gauche'] 

                i+=1
                if i>100:
                    i=0
                    #print("Plus de 100 essais")
                    salle.create_linked(3)
                    salle.createRoom()
                    salle.linkedPiece() 


            
            salle.afficherPiece()
            self.fogs.append(Fog(self.perso,salle.afficher()))
            self.fogs[j].init_fog_for_dungeon()
            self.liste_coffre.append(salle.list_coffre)
        
            j+=1
            #print(salle.nbre_graphique)        #implementation des monstres
        self.perso.pos_x,self.perso.pos_y = (self.pieces[self.actuel].spawn)

        #self.pieces[0].piece = numpy.rot90(self.pieces[0].piece,1)
        #print(any(True if self.pieces[0].piece[y][x] == 16 or self.pieces[0].piece[y][x] == 8 else False for x in range(len(self.pieces[0].piece)) for y in range(len(self.pieces[0].piece))))
        self.spawn_monster()
        self.cam = Camera(self.perso,self.pieces[self.actuel],self.liste_monstre[self.actuel])
        
    def update_affichage(self):
        self.perso.afficher()

        self.cam.actualiser(self.perso)
        self.cam.display_piece = self.pieces[self.actuel].afficher()
        #self.cam.afficher()
    #affichage d'un donjon : refresh est pour clean le screen (l'ecran devient noir)
    #permet d'afficher la piece actuelle, mais aussi de definir le spawn du joueur
    def affichageDonjon(self,refresh=False):

        if refresh:
            #self.pieces[self.actuel].refresh()
            self.screen.fill((255,255,255))
            pygame.display.flip()
        
        self.perso.pos_x,self.perso.pos_y = (self.pieces[self.actuel].spawn)
        self.cam.fog = self.fogs[self.actuel]
        self.cam.actualiser(self.perso)
        
        self.perso.afficher()
        self.cam.piece = self.pieces[self.actuel]
        self.cam.display_piece = self.pieces[self.actuel].afficher()
        self.cam.list_monster = self.liste_monstre[self.actuel]
        self.cam.liste_coffre = self.liste_coffre[self.actuel]
        self.cam.afficher()

    #fonction de deplacement, très nulle mais ce ne sera pas la version finale
    #juste une version d'essai
    def deplacement(self):
        
        if self.listekey.get(self.game.key["move up"]):
            self.cam.perso.mouvement = [False,False,False,False,False]
            self.cam.perso.mouvement[0] = True
            self.cam.perso.refresh_animation_and_mouvement()
            self.perso.pos_y-=4
            self.interaction = self.pieces[self.actuel].check_interact(self.perso)
            if self.pieces[self.actuel].check_collision(self.perso):
                self.perso.pos_y+=4
            else:

                self.update_affichage()
                
        if self.listekey.get(self.game.key["move down"]): 
            self.cam.perso.mouvement = [False,False,False,False,False]
            self.cam.perso.mouvement[1] = True
            self.cam.perso.refresh_animation_and_mouvement()
            self.perso.pos_y+=4
            self.interaction = self.pieces[self.actuel].check_interact(self.perso)
            if self.pieces[self.actuel].check_collision(self.perso):
                self.perso.pos_y-=4
            else:
                self.update_affichage()
        if self.listekey.get(self.game.key["move right"]):
            self.cam.perso.mouvement = [False,False,False,False,False]
            self.cam.perso.mouvement[2] = True
            self.cam.perso.refresh_animation_and_mouvement()
            self.perso.pos_x +=4
            self.interaction = self.pieces[self.actuel].check_interact(self.perso)
            if self.pieces[self.actuel].check_collision(self.perso):
                self.perso.pos_x -=4
            else:
                self.update_affichage()
        if self.listekey.get(self.game.key["move left"]):
            
            self.cam.perso.mouvement = [False,False,False,False,False]
            self.cam.perso.mouvement[3] = True
            self.cam.perso.refresh_animation_and_mouvement()
            self.perso.pos_x -=4
            self.interaction = self.pieces[self.actuel].check_interact(self.perso)
            if self.pieces[self.actuel].check_collision(self.perso):
                self.perso.pos_x +=4
            else:
                self.update_affichage()
        if self.listekey.get(self.game.key["interact"]):
            chest = self.collide_coffre()
            if chest != None:
                self.listekey[pygame.K_ESCAPE] = False
                while self.waitfor():
                    self.listekey[pygame.K_ESCAPE] = True 
                    self.cam.afficher(donotupdate = True)
                    chest.inventaire.loot_inventory(100,400,700,400,self.perso.inventaire)
                    pygame.display.update()
                    


                self.listekey[pygame.K_ESCAPE] = False 
                try:
                    self.liste_coffre[self.actuel].remove(chest)
                except:
                    pass
            if self.interaction == 8:
                
                self.monter_etage()
                
                #print("ESCALIER HAUT", self.actuel)
                self.interaction=0
            if self.interaction==16:
                
                self.descendre_etage()
                
                #print("ESCALIER BAS", self.actuel)
                self.interaction=0
            if self.interaction == 17:
                #print("FINISHED")
                self.interaction =0
                return 1
            self.listekey[self.game.key["interact"]]=False

        if self.listekey.get(pygame.K_u):
            self.monter_etage()
            self.listekey[pygame.K_u] = False
        if self.listekey.get(pygame.K_o):
            self.descendre_etage()
    
        if self.listekey.get(self.game.key["inventaire"]):
            while self.waitfor():
                self.cam.afficher(donotupdate = True)
                self.perso.print_equipement(100,100,500,500)
                pygame.display.update()
            self.listekey[pygame.K_i] = False
            
        if self.listekey.get(self.game.key["charactere sheet"]):
            self.perso.caracter_sheet()
            self.listekey[self.game.key["charactere sheet"]] = False
        if self.listekey.get(self.game.key["map"]):
            self.cam.zoom_minimap = True
        else:
            self.cam.zoom_minimap = False
    #classe permettant de jouer (running classique)
    #il faut prealablement avoir créé le donjon (et l'avoir affiché, c'est mieux quand même)

    def waitfor(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    self.listekey[pygame.K_ESCAPE] = False 
                    return False
        return True
    def runningDonjon(self):
        look_level = False
        look_level2 = False
        look_level3 = False
        mp = 0
        while self.listekey[pygame.K_SPACE]==False:
            self.__checkEvent()
            if(self.deplacement()==1):
                return 1
            #print '{}: tick={}, fps={}'.format(i+1, clock.tick(fps), clock.get_fps())
            clock.tick(32)
            monstre = None
            
            for x in self.liste_monstre[self.actuel]:
                if x.collide_box_interact.mask.overlap(self.perso.donjon_mask,((self.perso.pos_x+10)-x.collide_box_interact.pos_x,(self.perso.pos_y+90)-x.collide_box_interact.pos_y)):
                    #self.cam.screen.blit(x.collide_box_interact.img_collide,(x.collide_box_interact.pos_x,x.collide_box_interact.pos_y))
                    #pygame.display.update()
                    #self.pieces[self.actuel].wait()
                    self.perso.monstre_near = True
                    monstre = x
            if self.perso.monstre_near and monstre != None:
                for i in monstre.group_monster:
                    i.img = list_img_monstre[i.type-1]
                f = Combat(self.game,monstre.group_monster)

                f.affichage()
                if f.player.crew_mate[0].hp > 0 or f.player.crew_mate[1].hp > 0  or f.player.hp > 0:
                    inv_chest = Inventaire(7,7)
                    nbre_max_loot_possibles = 3 * len(monstre.group_monster)
                    items_dropable = []
                    for x in monstre.group_monster:
                        
                        items_dropable.append(key[x.armor[1]])
                        items_dropable.append(key[x.armor[4]])
                        self.liste_monstre[self.actuel].remove(x)
                        self.perso.xp += x.xp
                        self.perso.crew_mate[0].xp += x.xp
                        self.perso.crew_mate[1].xp += x.xp
                        if self.perso.levelupchange():
                            look_level = True
                        if self.perso.crew_mate[0].levelupchange():
                            look_level2 = True
                        if self.perso.crew_mate[1].levelupchange():
                            look_level3 = True
                    nbre_loot = random.randint(0,nbre_max_loot_possibles)

                    for i in range(nbre_loot):
                        chance_drop = random.randint(1,20)
                        if chance_drop == 1:  
                            num_item_drop = random.randint(0,len(items_dropable)-1)
                            inv_chest.ajouteritems(items_dropable[num_item_drop])
                            try :
                                items_dropable.remove(items_dropable[num_item_drop])
                            except:
                                pass
                    self.cam.liste_coffre.append(Chest(self.perso.pos_x,self.perso.pos_y,pygame.transform.scale(monstre_loot,(32,32)),"Coffre","Coffre",inv_chest))
                    self.cam.liste_coffre[-1].update_pos_collide()


                else:
                    return -1
                monstre = None
            if look_level:
                mp +=1
            if mp >= 50 and mp <= 200:
                self.cam.screen.blit(pygame.transform.scale(pygame.image.load(path.join(path_addon,'Image/lvl_up.png')),(WINDOWS_SIZE[0]//20,WINDOWS_SIZE[1]//20)),(self.player.pos_x+100+center_x,self.player.pos_y+center_y))
            elif mp>200:
                look_level = False
                mp =0
            if look_level2:
                mp +=1
            if mp >= 50 and mp <= 200:
                self.cam.screen.blit(pygame.transform.scale(pygame.image.load(path.join(path_addon,'Image/lvl_up.png')),(WINDOWS_SIZE[0]//20,WINDOWS_SIZE[1]//20)),(self.player.crew_mate[0].pos_x+100+center_x,self.player.crew_mate[0].pos_y+center_y))
            elif mp>200:
                look_level2 = False
                mp =0
            if look_level3:
                mp +=1
            if mp >= 50 and mp <= 200:
                self.cam.screen.blit(pygame.transform.scale(pygame.image.load(path.join(path_addon,'Image/lvl_up.png')),(WINDOWS_SIZE[0]//20,WINDOWS_SIZE[1]//20)),(self.player.crew_mate[1].pos_x+100+center_x,self.player.crew_mate[1].pos_y+center_y))
            elif mp>200:
                look_level3 = False
                mp =0
            self.cam.afficher()
            
        self.listekey[pygame.K_SPACE] = False

    #permet de changer de salle
    def monter_etage(self):
        if self.actuel < self.nbEtage-1:
            self.actuel +=1
            self.affichageDonjon(refresh=True)

    #idem que monter_etage
    def descendre_etage(self):
        if self.actuel>0:
            self.actuel-=1
            self.affichageDonjon(refresh=True)

    
        
    #methode permettant de recuperer les touches pressees par l'utilisateur
    #6 touches utiles:
    # 4 touches directionnelles -> deplacer le personnage
    # touche i -> interagir avec les escaliers
    # touche ESPACE pour quiter le jeu
    def __checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                running = False
                pygame.quit()
                print("Fermeture du jeu")
                return True
            if event.type == pygame.KEYDOWN:
                self.listekey[event.key] = True
                if event.key == pygame.K_RIGHT and self.listekey[pygame.K_LEFT]:self.listekey[pygame.K_LEFT]=False
                if event.key == pygame.K_LEFT and self.listekey[pygame.K_RIGHT]:self.listekey[pygame.K_RIGHT]=False
                if event.key == pygame.K_UP and self.listekey[pygame.K_DOWN]:self.listekey[pygame.K_DOWN]=False
                if event.key == pygame.K_DOWN and self.listekey[pygame.K_UP]:self.listekey[pygame.K_UP]=False
                if event.key == pygame.K_ESCAPE : self.listekey[event.key] = False
                return True
            if event.type == pygame.KEYUP:
                self.listekey[event.key] = False
                return True

    def save(self,nom_fichier):
        for salle in self.pieces:
            salle.save(nom_fichier,ecrireFin=(salle!=self.pieces[0]))

    def load(self,nom_fichier):
        relative_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"saves/")
        fichier = open(os.path.join(relative_path,nom_fichier),"r")
        ligne = []
        x=0
        y=0
        max=0
        chaine =""
        index=0
        for things in fichier:
            #print(things)
            if things[0]=='e':
                for y in range(len(self.pieces[index].piece)):
                    for x in range(len(self.pieces[index].piece[y]),max):
                        self.pieces[index].piece[y].append(0)
                index+=1
            else:
                for i in range(len(things)):
                    if things[i] == " ":
                        x+=1
                        ligne.append(int(chaine))
                        chaine =""
                    elif things[i] == "\n":
                        y+=1
                        if chaine != "":
                            x+=1
                            ligne.append(int(chaine))
                        self.pieces[index].piece.append(ligne)
                        if(x>max):
                            max=x
                        x=0
                        ligne = []
                        chaine =""
                    else:
                        chaine +=things[i]
        fichier.close()
        for salle in self.pieces:
            salle.afficherPiece()

    def spawn_monster(self):
        currentX = 0
        currentY = 0
        position = False # Le monstre a-t'il trouve un spawn
        indexPiece = 0
        which_monster = 0
        pos_x = 0
        pos_y=0
        for salle in self.pieces:
            
            self.liste_monstre[indexPiece] = []
            for i in range(3*self.difficulty+5):
                difficulte_monstre = self.difficulty
                if(self.difficulty>4):
                    difficulte_monstre = 4
                if self.difficulty >2:
                    which_monster = random.randint(difficulte_monstre,len(list_img_monstre)-1)
                else:
                    which_monster = random.randint(0,2)
                while position != True:
                    y= random.randint(0,len(salle.piece)-1)

                    x= random.randint(0,len(salle.piece[y])-1)
                    currentX= salle.startX + (salle.lengthPiece//2) * (x-y-1)
                    currentY = salle.startY + (salle.heightPiece//4)*(x+1+y)

                    if salle.piece[y][x] == 1:
                        position = True
                        pos_x = currentX+20
                        pos_y = currentY +5



                position = False
                self.liste_monstre[indexPiece].append(Monster(pos_x,pos_y,pygame.transform.scale(list_img_monstre[which_monster-1],(50,80)),"",which_monster-1,\
                size=list_size_monstre[which_monster-1],animation_dict=list_animation_monstre[which_monster-1],\
                    decalage=list_decalage_monstre[which_monster-1],donjon=True))
            indexPiece+=1
    
    def collide_coffre(self):
        for chest in self.liste_coffre[self.actuel]:
            center = (chest.pos_x + chest.img.get_width()//2, chest.pos_y+chest.img.get_height() // 2)
            dist = sqrt((center[0] - self.perso.pos_x)**2 + (center[1] - self.perso.pos_y)**2)
            if dist < 80:
                return chest