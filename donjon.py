from piece import Piece
import pygame
from perso import Personnage
from pygame.time import Clock
import os
clock = pygame.time.Clock()
#classe permettant de créer un donjon
#un donjon contient un ensemble de piece ainsi que des monstres, des loots, etc...
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)
class Donjon():

    #difficulte pas encore implementee, soon
    #screen : la surface surlaquelle print les salles du donjons
    #peros : self.personnage que l'on doit déplacer -> sert pour les collisions
    #nbreEtage : De base on est a 3, mais on peut faire +
    def __init__(self,difficulte,screen,perso,nbreEtage=3):

        self.difficulty = difficulte
        self.nbEtage = nbreEtage
        self.pieces = []
        self.screen = screen
        self.actuel = 0 # piece actuelle
        self.listekey = dict()
        self.perso = perso
        self.interaction = 0
        for i in range(self.nbEtage):
            self.pieces.append(Piece(screen))

        #i=0 -> etage 0 ; i=2 -> etage 1 ...

        #les etages 0 et 3 n'ont qu'un escalier
        self.pieces[0].max_graphique[8] = self.pieces[self.nbEtage-1].max_graphique[8] = 1
        self.pieces[self.nbEtage-1].max_graphique[8] = self.pieces[0].max_graphique[16] = 0
        
        self.listekey = {pygame.K_UP : False, pygame.K_DOWN : False, pygame.K_RIGHT:False,pygame.K_LEFT:False,pygame.K_SPACE:False}
    def creationDonjon(self):
        for salle in self.pieces:
            salle.createRoom()
            while salle.check_jouabilite() != True:
                salle.createRoom()
                print("Probleme generation piece")
            salle.afficherPiece()
    

    #affichage d'un donjon : refresh est pour clean le screen (l'ecran devient noir)
    #permet d'afficher la piece actuelle, mais aussi de definir le spawn du joueur
    def affichageDonjon(self,refresh=False):

        if refresh:
            #self.pieces[self.actuel].refresh()
            self.screen.fill((255,255,255))
            pygame.display.flip()
        
        self.pieces[self.actuel].afficher()
        self.perso.X,self.perso.Y = (self.pieces[self.actuel].spawn)
        self.perso.afficher()
        pygame.display.flip()

    #fonction de deplacement, très nulle mais ce ne sera pas la version finale
    #juste une version d'essai
    def deplacement(self):
        if self.listekey.get(pygame.K_UP):
            
            self.perso.deplacerHaut()
            self.interaction = self.pieces[self.actuel].check_interact(self.perso)
            if self.pieces[self.actuel].check_collision(self.perso):
                self.perso.deplacerBas()
            else:
                self.pieces[self.actuel].afficher()
                self.perso.afficher()
                self.pieces[self.actuel].update_graph(self.perso,self.screen)
                
                pygame.display.update()
        if self.listekey.get(pygame.K_DOWN):
           
            self.perso.deplacerBas()
            self.interaction = self.pieces[self.actuel].check_interact(self.perso)
            if self.pieces[self.actuel].check_collision(self.perso):
                self.perso.deplacerHaut()
            else:
                self.pieces[self.actuel].afficher()
                self.perso.afficher()
                self.pieces[self.actuel].update_graph(self.perso,self.screen)
                
                pygame.display.update()
        if self.listekey.get(pygame.K_RIGHT):
            
            self.perso.deplacerDroite()
            self.interaction = self.pieces[self.actuel].check_interact(self.perso)
            if self.pieces[self.actuel].check_collision(self.perso):
                self.perso.deplacerGauche()
            else:
                self.pieces[self.actuel].afficher()
                self.perso.afficher()
                self.pieces[self.actuel].update_graph(self.perso,self.screen)
                
                pygame.display.update()
        if self.listekey.get(pygame.K_LEFT):
            self.perso.deplacerGauche()
            self.interaction = self.pieces[self.actuel].check_interact(self.perso)
            if self.pieces[self.actuel].check_collision(self.perso):
                self.perso.deplacerDroite()
            else:
                self.pieces[self.actuel].afficher()
                
                self.perso.afficher()
                self.pieces[self.actuel].update_graph(self.perso,self.screen)
                
                pygame.display.update()
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
            textsurface = myfont.render('Etage : %i'%self.actuel, False, (255, 255, 255))
            self.screen.blit(textsurface,(15,15))
            pygame.display.update()

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
