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

list_img_monstre = [list_entity_animation[0],list_entity_animation[1],list_entity_animation[2],list_entity_animation[3],list_entity_animation[4]]
list_animation_monstre = [demon_1_animation,demon_animation,squelton_animation,wizard_animation,dark_wizard_animation]
list_decalage_monstre = [[0,0],[0,0],[0,0],[0,0],[0,0]]
list_size_monstre = [(500,400),(500,400),(300,300),(300,300),(600,500)]


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
    def __init__(self,difficulte,screen,perso,game=None,nbreEtage=3):

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
        self.liste_monstre = []
        for i in range(self.nbEtage):
            self.pieces.append(Piece(screen))
            self.liste_monstre.append([])
        self.pieces[0].linked = ['Haut','Haut','Gauche','Droite', 'Gauche']        
        self.pieces[1].linked = ['Droite', 'Gauche','Gauche','Gauche','Haut']
        self.pieces[2].linked = ['Droite', 'Gauche','Gauche','Gauche','Haut']
        #i=0 -> etage 0 ; i=2 -> etage 1 ...

        #les etages 0 et 3 n'ont qu'un escalier
        self.pieces[0].max_graphique[8] = self.pieces[self.nbEtage-1].max_graphique[8] = 1
        self.pieces[self.nbEtage-1].max_graphique[8] = self.pieces[0].max_graphique[16] = 0
        for i in range(1,nbreEtage-1):
            self.pieces[i].max_graphique[8]=self.pieces[i].max_graphique[16]=1
        self.listekey = {pygame.K_UP : False, pygame.K_DOWN : False, pygame.K_RIGHT:False,pygame.K_LEFT:False,pygame.K_SPACE:False}


    def creationDonjon(self):
        j=0
        for salle in self.pieces:
            
            direction = 0
            nbreHaut = 0
            salle.linked = []
            for i in range(2+3*self.difficulty):
                direction = random.randint(0,3)
                if direction==0:salle.linked.append('Gauche')
                if direction ==1:salle.linked.append('Droite')
                if direction==2 and nbreHaut <2:
                    nbreHaut+=1
                    salle.linked.append('Haut')
            print(salle.linked)
            salle.linked=['Gauche','Haut','Droite','Haut']
            salle.createRoom()
            salle.linkedPiece()
            i=0
            

            
            while salle.check_jouabilite()!= True:
                print("Probleme generation piece %i etage %i"%(i,j))

                
                salle.createRoom()
                salle.linkedPiece(check_pieces=True)
                #salle = Piece(self.screen)
                #salle.linked = ['Haut','Haut','Gauche','Gauche','Droite','Gauche'] 
                i+=1
            
            
            salle.afficherPiece()
            self.fogs.append(Fog(self.perso,salle.afficher()))
            self.fogs[j].init_fog_for_dungeon()
            j+=1
        #implementation des monstres
        self.perso.pos_x,self.perso.pos_y = (self.pieces[self.actuel].spawn)

        #self.pieces[0].piece = numpy.rot90(self.pieces[0].piece,1)
        print(any(True if self.pieces[0].piece[y][x] == 16 or self.pieces[0].piece[y][x] == 8 else False for x in range(len(self.pieces[0].piece)) for y in range(len(self.pieces[0].piece))))
        self.spawn_monster()
        self.cam = Camera(self.perso,self.pieces[self.actuel],self.liste_monstre[self.actuel])
        
    def update_affichage(self):
        self.perso.afficher()

        self.cam.actualiser(self.perso)
        self.cam.display_piece = self.pieces[self.actuel].afficher()
        self.cam.afficher()
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
        
        self.cam.afficher()

    #fonction de deplacement, très nulle mais ce ne sera pas la version finale
    #juste une version d'essai
    def deplacement(self):
        
        if self.listekey.get(pygame.K_UP):
            
            self.perso.pos_y-=2
            self.interaction = self.pieces[self.actuel].check_interact(self.perso)
            if self.pieces[self.actuel].check_collision(self.perso):
                self.perso.pos_y+=2
            else:

                self.update_affichage()
                
        if self.listekey.get(pygame.K_DOWN): 
           
            self.perso.pos_y+=2
            self.interaction = self.pieces[self.actuel].check_interact(self.perso)
            if self.pieces[self.actuel].check_collision(self.perso):
                self.perso.pos_y-=2
            else:
                self.update_affichage()
        if self.listekey.get(pygame.K_RIGHT):
            
            self.perso.pos_x +=2
            self.interaction = self.pieces[self.actuel].check_interact(self.perso)
            if self.pieces[self.actuel].check_collision(self.perso):
                self.perso.pos_x -=2
            else:
                self.update_affichage()
        if self.listekey.get(pygame.K_LEFT):
            self.perso.pos_x -=2
            self.interaction = self.pieces[self.actuel].check_interact(self.perso)
            if self.pieces[self.actuel].check_collision(self.perso):
                self.perso.pos_x +=2
            else:
                self.update_affichage()
        if self.listekey.get(pygame.K_i):
            if self.interaction == 7:
                print("COFFRE")
                self.interaction=0
            if self.interaction == 8:
                print("ESCALIER HAUT", self.actuel)
                self.monter_etage()
                self.interaction=0
            if self.interaction==16:
                print("ESCALIER BAS", self.actuel)
                self.descendre_etage()
                self.interaction=0
        
    #classe permettant de jouer (running classique)
    #il faut prealablement avoir créé le donjon (et l'avoir affiché, c'est mieux quand même)
    def runningDonjon(self):
        
        while self.listekey[pygame.K_SPACE]==False:
            self.__checkEvent()
            self.deplacement()
            #print '{}: tick={}, fps={}'.format(i+1, clock.tick(fps), clock.get_fps())
            clock.tick(64)
            monstre = None
            
            for x in self.liste_monstre[self.actuel]:
                if x.collide_box_interact.mask.overlap(self.perso.masks,((self.perso.pos_x+10)-x.collide_box_interact.pos_x,(self.perso.pos_y+self.perso.img.get_height()-15)-x.collide_box_interact.pos_y)):
                    
                    self.perso.monstre_near = True
                    monstre = x
            if self.perso.monstre_near and monstre != None:
                for i in monstre.group_monster:
                    i.img = list_img_monstre[i.type-1]
                f = Combat(self.game,monstre.group_monster)
                f.affichage()
                """
                if f.player.crew_mate[0].hp > 0 or f.player.crew_mate[1].hp > 0  or f.player.hp > 0:
                    for x in monstre.group_monster:
                        self.liste_monstre.remove(x)"""
                monstre = None
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
            print(things)
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
            
            self.liste_monstre[indexPiece] =[]
            for i in range(3*self.difficulty+5):
                which_monster = random.randint(1,len(list_img_monstre))
                while position != True:
                    y= random.randint(0,len(salle.piece)-1)

                    x= random.randint(0,len(salle.piece[y])-1)
                    currentX= salle.startX + (salle.lengthPiece//2) * (x-y-1)
                    currentY = salle.startY + (salle.heightPiece//4)*(x+1+y)

                    if salle.piece[y][x] == 1:
                        position = True
                        pos_x = currentX+20
                        pos_y = currentY +5
                        print("COORD : ",currentX,currentY)



                position = False
                self.liste_monstre[indexPiece].append(Monster(pos_x,pos_y,pygame.transform.scale(list_img_monstre[which_monster-1],(50,80)),"",which_monster-1,\
                size=list_size_monstre[which_monster-1],animation_dict=list_animation_monstre[which_monster-1],\
                    decalage=list_decalage_monstre[which_monster-1],))

                print(f"A MONSTER HAS SPAWNED ON COORD ({pos_x},{pos_y})\n")