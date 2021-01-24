import pygame
import os
import random
import time
import numpy
import sys
from inventory import Inventaire
from entity import Chest
from settings.load_img import graphique_donjon,nb_graphique_donjon,collide_donjon,mur_donjon,parquet_donjon
sys.setrecursionlimit(10000)
class Piece():

    def __init__(self,display): 

        self.tailleMax = [70,70] #argument donnant la definition de la piece -> si on augmente ca dezoome et si on diminue ça zoom
        self.lengthPiece,self.heightPiece = self.tailleMax

        #image du mur
        self.mur = mur_donjon
        #image du parquet
        self.parquet = parquet_donjon
        #taux d'irregularites des murs
        self.changementRate = 20
        #nombre d'irregularites dans les murs
        self.nbreChangement = 3

        #coordonne d'affichage du (0,0) de la piece
        self.start = tuple((2500,2500))
        self.startX, self.startY = self.start
        self.donotBlit=[]
        #ecran a afficher
        self.piece =[]
        self.display = pygame.Surface((7000,7000))

        #nom des grapiques a afficher
        #convention de nommage : nom_element000 + 1 chiffre entre 0 et 4
        #chaque numero correspond a un point de vue de la piece

        #nombre d'elements graphiques ( le 2 correspond au mur + parquet)

        #variable inutile mais permet de relier les id aux elements
        self.id_graphname = {2:"litA",3:"chaise",4:"commode",5:"cheminee",\
            6:"table",7:"coffre",8:"escalier",9:"litB",10:"livre",\
            11:"biblio",12:"biblioA",13:"biblioB",14:"tableA",\
            15:"teleporteur",16:"escalier"
            }
        
        #dictionnaire reliant les id aux images
        """
        self.graphique = {i+2 : [self.createImages(self.graphique_states[i][j],autocolorkey=True,scaled=(70,70)) for j in range(len(self.graphique_states[i]))]  for i in range(len(self.graphique_states))  }
        self.graphique[self.nbre_graphique] = [self.createImages("teleporter.png",scaled=(64,64))]
        self.nbre_graphique+=1
        self.graphique[self.nbre_graphique] = [self.createImages("45.png",forceScale=True)]
        self.graphique[16] = self.graphique[8]
        self.nbre_graphique+=1
        """

        self.graphique = graphique_donjon

        self.nbre_graphique = nb_graphique_donjon
        #self.graphiique[self.nbre_graphique]
        #dictionnaire definissant le nombre maximum d'elements par piece selon les id
        self.max_graphique = {2:50,3:15,4:25,5:50,6:50,7:50,8:50,9:50,10:50,11:50,12:50,13:50,14:50,15:0}
        self.max_graphique={x : 10 for x in range(2,self.nbre_graphique)}

        self.max_graphique[15] = 1
        self.max_graphique[16] = self.max_graphique[8] = 1
        self.max_graphique[17] = 0
        self.collide = collide_donjon
        self.collide_mask = pygame.mask.from_surface(self.parquet)
        #liste a utiliser pour les collisions
        self.liste_collision = []
        #liste a utiliser pour les collisions avec un element interactif (coffre, escalier, peut-etre porte par la suite)
        self.interact_collision = []
        self.index_interact_collsion = []
        #taux dapparition des graphiques par piece
        self.rate_graphique={2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1,10:1,11:1,12:1,13:1,14:1,16:1}
        self.rate_graphique={x : 0.1 for x in range(2,self.nbre_graphique)}
        self.rate_graphique[15] = self.rate_graphique[16] = 1
        self.rate_graphique[7] = self.rate_graphique[8] = self.rate_graphique[16] = 1
        self.spawn = tuple()

        self.isSpawn = False 
        #equivalent = self.spawn != tuple()
        #graphique (id) ne pouvant se trouver que sur des bords
        self.bord_graphique = [2,5,7,8]
        self.graphique_collision = []

        self.image_collision_graphique = []
        #graphique important : parquet et interaction possible
        self.important_graph = [1,7,8,16,17]
        #self.vide = self.createImages("antho.png",forceScale=True,autocolorkey=True)

        self.taille = None
        self.linked = None
        self.alreadySpawn = False
        self.list_coffre = []

    #methode de test pour afficher une liste double
    def afficherListe(self):
        for y in range(len(self.piece)):
                print(self.piece[y])


    
    #equivalent a afficherPiece (pour la compatibilite)
    def afficher(self):
        self.afficherPiece()

    
    #methode creant une piece
    #argument taille_Min : taille minimum de la piece (en nombre d'elements) de la forme tailleMin(longueur,largeur)
    #argument taille_Max : idem que taille_Min pour pour le maximum
    #la methode tire au sort un nombre entre taille_Min et taille_Max
    def createRoom(self, taille_Min = (15,15), taille_Max = (18,18),graphique_count=None,start=False):
        if start:
            graphique_count = dict()
            graphique_count[16]=0
            graphique_count[8] = graphique_count[17] = 1
        self.piece = self.__createPiece(taille_Min=taille_Min,taille_Max=taille_Max,graphique_count=graphique_count)
    def __createPiece(self,taille_Min = (15,15), taille_Max = (18,18),graphique_count=None):

        if self.taille == None:
                self.taille = (random.randint(taille_Min[0],taille_Max[0]), random.randint(taille_Min[1],taille_Max[1]))
        while self.taille[0] +2 == self.taille[1]:
             self.taille = (random.randint(taille_Min[0],taille_Max[0]), random.randint(taille_Min[1],taille_Max[1]))

        #bug sur la taille (16,18)
        x,y = 0,0
        piece = []
        directionMemory = 0
        piece = [[1 for j in range(0,self.taille[0])] for i in range(0,self.taille[1])]
        for y in range(0, self.taille[1], self.taille[1]-1):

            for x in range(0,self.taille[0]):
                i = random.randint(0,100)
                if i <=self.changementRate and directionMemory < self.nbreChangement:
                    piece[y][x] = 0
                    directionMemory += 1
            directionMemory = 0

        for x in range(0, self.taille[0], self.taille[0]-1):

            for y in range(0,self.taille[1]):
                i = random.randint(0,100)
                if i <=self.changementRate and directionMemory < self.nbreChangement:
                    piece[y][x] = 0
                    directionMemory += 1
            directionMemory = 0
        if piece[0][1] == piece[1][0]:#coin en haut a droite
            piece[0][1] = 1
        if piece[0][self.taille[0]-2] == piece[1][self.taille[0]-1]: # coin en haut à gauche
            piece[0][self.taille[0]-1] = 0
        if piece[self.taille[1]-2][0] == piece[self.taille[1] - 1][1]: # coin en bas a gauche
            piece[self.taille[1]-1][0] = 0
        if piece[self.taille[1]-1][self.taille[0]-2] == piece[self.taille[1] - 2][self.taille[0]-1]: #coin en bas a gauche
            piece[self.taille[1]-1][self.taille[0]-2] = 0
        if graphique_count==None:
            graphique_count = dict()
        #permettant de compter le nombre d'occurences de chaque element
        for y in range(0,len(piece)):
            for x in range(0,len(piece[0])):
                if piece[y][x] ==1:
                    choosen = random.randint(2,self.nbre_graphique-1) #defini l'element a choisir
                    rate = random.randint(0,100) #tire un nombre aleatoire pour savoir si l'element va spawn ou non
                    if rate <= self.rate_graphique[choosen] * 100:
                        testBord = True
                        if choosen in self.bord_graphique: #si l'element est obligatoirement a l'extremite d'une piece
                            if x == 0 or x == len(piece[0]) -1 or y== len(piece) -1 or y ==0:
                                testBord = True
                            elif piece[y-1][x] == 0 or piece[y+1][x] == 0 or piece[y][x-1] ==0 or piece[y][x]==0:
                                testBord = True
                            else:
                                testBord = False
                                x-=1
                        if choosen in graphique_count and testBord:
                            if graphique_count[choosen] < self.max_graphique[choosen]: 
                                graphique_count[choosen] +=1
                                if choosen ==15 and not self.alreadySpawn:
                                    self.isSpawn=True
                                    piece[y][x] = choosen
                                elif choosen == 15:
                                    x-=1
                                else:
                                    piece[y][x] = choosen
                        elif testBord and self.max_graphique[choosen] >0:
                            graphique_count[choosen] = 1
                            if choosen==15 and not self.alreadySpawn:
                                self.isSpawn=True
                                piece[y][x] = choosen
                            elif choosen == 15:
                                x-=1
                            else:
                                piece[y][x] = choosen
        if 15 not in self.piece:
            piece[0][0] = 15 #provisoirement le spawn du joueur
        #a remplacer plus tard par un teleporteur

        return piece

    #methode affichant une piece : parquet murs et elements
    #aucune valeur de retour
    #methode pour les tests
    #ne pas utiliser
    def wait(self):
        end = True
        while end:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        end = False
        return True

    #methode permettant de creer les elements dans la piece
    #ne retourne rien et creer tous les elements dans self.piece
    def __createElts(self):
        graphique_count = dict()
        #permettant de compter le nombre d'occurences de chaque element
        for y in range(0,len(self.piece)):
            for x in range(0,len(self.piece[0])):
                if self.piece[y][x] ==1:
                    choosen = random.randint(2,self.nbre_graphique-1) #defini l'element a choisir
                    rate = random.randint(0,100) #tire un nombre aleatoire pour savoir si l'element va spawn ou non
                    if rate <= self.rate_graphique[choosen] * 100:
                        testBord = True
                        if choosen in self.bord_graphique: #si l'element est obligatoirement a l'extremite d'une piece
                            if x == 0 or x == len(self.piece[0]) -1 or y== len(self.piece) -1 or y ==0:
                                testBord = True
                            elif self.piece[y-1][x] == 0 or self.piece[y+1][x] == 0 or self.piece[y][x-1] ==0 or self.piece[y][x]==0:
                                testBord = True
                            else:
                                testBord = False
                                x-=1
                        if choosen in graphique_count and testBord:
                            if graphique_count[choosen] < self.max_graphique[choosen]: 
                                graphique_count[choosen] +=1
                                if choosen ==15:self.spawn=True
                                self.piece[y][x] = choosen
                        elif testBord and self.max_graphique[choosen] !=0:
                            graphique_count[choosen] = 1
                            if choosen==15:self.spawn=True
                            self.piece[y][x] = choosen
        if not self.spawn:
            self.piece[0][0] = 15 #provisoirement le spawn du joueur
        #a remplacer plus tard par un teleporteur


    #methode affichant une piece : parquet murs et elements
    #aucune valeur de retour
    def afficher(self):
        return self.display
        
    def afficherPiece(self):
        #affichage parquet
        currentX = self.startX
        currentY = self.startY
        for y in range(0,len(self.piece)):
            for x in range(0,len(self.piece[0])):
                if self.piece[y][x] != 0:
                    #self.display.blit(pygame.transform.scale(self.parquet,(self.lengthPiece,self.heightPiece)), (currentX,currentY))
                    self.display.blit(self.parquet,(currentX,currentY))
                currentX+=self.lengthPiece//2
                currentY+= self.heightPiece//4
            currentY= self.startY + (self.heightPiece//4)*(y+1)
            currentX = self.startX - (self.lengthPiece//2)*(y+1)

        #affichage de la piece : mur et elements
        #methode : on afficher les elements selon la diagonale gauche bas
        #un element plus haut a droite sera affiche avant pour conserver l'effet de perspective
        #chaque element est enregistre dans self.liste_collision pour les collisions


        currentX = self.startX
        currentY = self.startY


        for y in range (len(self.piece)):
            for x in range (len(self.piece[y])):
                if self.piece[y][x] ==0: #si il n'y a rien et du parquet autour on affiche un mur
                    if (x!=0 and self.piece[y][x-1]!=0) or (y!=0 and self.piece[y-1][x]!=0) or (y!=len(self.piece)-1 and self.piece[y+1][x]!=0 and self.piece[y+1][x]!=15) or (x!=len(self.piece[y])-1 and self.piece[y][x+1]!=0):
                        
                        self.display.blit(self.mur,(currentX,currentY))
                        self.liste_collision.append((currentX,currentY-8))
                        self.graphique_collision.append(pygame.Rect((currentX,currentY),(self.mur.get_width(),self.mur.get_height())))
                        self.image_collision_graphique.append([self.mur,(currentX,currentY)])
                elif self.piece[y][x] !=0: #si ce n'est pas vide on affiche l'element correspondant (en regardant au prealable si il n'y a pas un mur a placer autour)
                    if x==0:
                        self.display.blit(self.mur,(currentX-self.lengthPiece//2,currentY-self.heightPiece//4))
                        self.liste_collision.append((currentX-self.lengthPiece//2,currentY-self.heightPiece//4-8))
                        self.graphique_collision.append(pygame.Rect((currentX-self.lengthPiece//2,currentY-self.heightPiece//4),(self.mur.get_width(),self.mur.get_height())))
                        self.image_collision_graphique.append([self.mur,(currentX-self.lengthPiece//2,currentY-self.heightPiece//4)])
                        
                    if y == 0:
                        self.display.blit(self.mur,(currentX+self.lengthPiece//2,currentY-self.heightPiece//4))
                        self.liste_collision.append((currentX+self.lengthPiece//2,currentY-self.heightPiece//4-8))
                        self.graphique_collision.append(pygame.Rect((currentX+self.lengthPiece//2,currentY-self.heightPiece//4),(self.mur.get_width(),self.mur.get_height())))
                        self.image_collision_graphique.append([self.mur,(currentX+self.lengthPiece//2,currentY-self.heightPiece//4)])


                    #affichage des elements    
                    if(self.piece[y][x] >= 2):
                        if x==0 or self.piece[y][x-1] ==0:
                            image=self.__imageAngle(self.graphique[self.piece[y][x]], gauche=True)
                            #self.display.blit(image,(currentX,currentY+image.get_height()-self.tailleMax[1]/2))
                                
                        elif x==len(self.piece[0]) -1 or self.piece[y][x+1]==0:
                            image=self.__imageAngle(self.graphique[self.piece[y][x]], droite=True)
                            #self.display.blit(image,(currentX,currentY+image.get_height()-self.tailleMax[1]/2))
  
                        elif y==0 or self.piece[y-1][x] == 0:
                            image=self.__imageAngle(self.graphique[self.piece[y][x]], haut=True)
                            #self.display.blit(self.__imageAngle(self.graphique[self.piece[y][x]], haut=True),(currentX,currentY))

                        elif y==len(self.piece) -1 or self.piece[y+1][x] ==0:
                            image=self.__imageAngle(self.graphique[self.piece[y][x]], bas=True)
                            #self.display.blit(self.__imageAngle(self.graphique[self.piece[y][x]], bas=True),(currentX,currentY))

                        else:
                            image=self.__imageAngle(self.graphique[self.piece[y][x]], gauche=True)
                            #self.display.blit(self.__imageAngle(self.graphique[self.piece[y][x]], gauche=True),(currentX,currentY))
                        if(self.piece[y][x] == 15):
                            self.spawn=(currentX+20,currentY+5)
                        #self.display.blit(image,(currentX,currentY+self.tailleMax[1]-image.get_height()))
                        if self.piece[y][x] != 7:
                            try :
                                self.display.blit(image,(currentX,currentY))
                            except:
                                pass
                        if(self.piece[y][x] != 15 and self.piece[y][x] != 17):
                            self.liste_collision.append((currentX,currentY))
                            if self.piece[y][x] != 7:
                                self.graphique_collision.append(pygame.Rect((currentX,currentY),(image.get_width(),image.get_height())))
                                self.image_collision_graphique.append([image,(currentX,currentY)])
                        if self.piece[y][x] in self.important_graph:
                            self.interact_collision.append((currentX,currentY))
                            self.index_interact_collsion.append(self.piece[y][x])
                            if self.piece[y][x] == 7:
                                inv_chest = Inventaire(7,7)
                                inv_chest.add_random_drop(random.randint(1,5))
                                self.list_coffre.append(Chest(currentX+15,currentY+20,pygame.transform.scale(self.graphique[7][0],(32,32)),"Coffre","Coffre",inv_chest))
 
                    if x==len(self.piece[y])-1:
                        self.display.blit(self.mur,(currentX+self.lengthPiece//2,currentY+self.heightPiece//4))
                        self.liste_collision.append((currentX+self.lengthPiece//2,currentY+self.heightPiece//4-8))
                        self.graphique_collision.append(pygame.Rect((currentX+self.lengthPiece//2,currentY+self.heightPiece//4),(self.mur.get_width(),self.mur.get_height())))
                        self.image_collision_graphique.append([self.mur,(currentX+self.lengthPiece//2,currentY+self.heightPiece//4)])
                    if y == len(self.piece)-1:
                        self.display.blit(self.mur,(currentX-self.lengthPiece//2,currentY+self.heightPiece//4))
                        self.liste_collision.append((currentX-self.lengthPiece//2,currentY+self.heightPiece//4-8))
                        self.graphique_collision.append(pygame.Rect((currentX-self.lengthPiece//2,currentY+self.heightPiece//4),(self.mur.get_width(),self.mur.get_height())))
                        self.image_collision_graphique.append([self.mur,(currentX-self.lengthPiece//2,currentY+self.heightPiece//4)])
                currentX+=self.lengthPiece//2
                currentY+= self.heightPiece//4
            currentY= self.startY + (self.heightPiece//4)*(y+1)
            currentX = self.startX - (self.lengthPiece//2)*(y+1)
        """for x in self.liste_collision:
            self.display.blit(self.collide,(x[0],x[1]+32))"""
        self.voisin_collision = []
        for i in self.graphique_collision:
            liste =[]
            y=0
            for j in self.graphique_collision:
                if j.colliderect(i):
                    if i.y<j.y:
                        liste.append(y)
                y+=1
            self.voisin_collision.append(sorted(liste))



    #methode permettant de load une image pygame
    #arguments : name -> nom du fichier a load /!\ obligatoirement dans le fichier imgs/
    #scale -> si l'image est plus grande que la definition de chaque element (stocke dans self.tailleMax)redimensionne l'image
    #colorkey -> definit la couleur de transparence de l'image en RGB, par defaut noir
    #forceScale -> equivalent a scale sauf que l'image est obligatoirement redimensionnee (quelle que soit sa taille)


    #chaque image a 4 angles differents et cette methode permettant de selectionner un certain agnle
    #renvoie une image avec un angle donne
    #liste_etats : liste de 4 etats (images) et chaque etat est un angle/point de vue
    #gauche : retourne le point de vue de gauche
    #haut/droite/bas idem que gauche mais pour les points de vue respectifs
    def __imageAngle(self,liste_etats, gauche=False, haut=False, droite=False,bas=False):
        try:
            len(liste_etats)
        except:

            return self.graphique[17]

        if len(liste_etats) !=4:
            if len(liste_etats) ==2:
                if gauche or haut:
                    return liste_etats[0]
                return liste_etats[1]
            else:
                return liste_etats[0]
        if gauche:
            return liste_etats[0]
        if droite:
            return liste_etats[2]
        if haut :
            return liste_etats[1]
        return liste_etats[3]


    #gere les collisions entre le joueurs et les elements du decor (meubles/murs)
    def check_collision(self,perso,monstre=False):
 

        if monstre: 
            mask_d = perso.collide_box.mask
        else:
            mask_d = perso.donjon_mask
        for x in self.liste_collision:
            if self.collide_mask.overlap(mask_d,((round(perso.pos_x))-x[0]+10,(49+round(perso.pos_y)-x[1])-15)):

                return True
        return False
        
    #gere les interactions entre le perso et les graphs importants (escalier, coffre...)
    def check_interact(self,perso):
        i=0
        interact=0
        for x in self.interact_collision:
            mask_interaction = self.collide_mask.overlap(perso.donjon_mask,((round(perso.pos_x))-x[0]+10,(49+round(perso.pos_y)-x[1])-15))
            if mask_interaction:
                interact = self.index_interact_collsion[i]
            i+=1
        return interact
    
    def create_linked(self,nombre_max=5):
        self.linked = []
        for i in range(nombre_max):
            direction = 0
            nbreHaut = 0
            self.linked = []
            for i in range(nombre_max):
                direction = random.randint(0,3)
                if direction==0:self.linked.append('Gauche')
                if direction ==1:self.linked.append('Droite')
                if direction==2 and nbreHaut <2:
                    nbreHaut+=1
                    self.linked.append('Haut')

    
    
    #rajoute une piece liee
    #la liste des pieces liees donne les positions : 'Droite' 'Gauche' 'Bas' 'Haut'
    def linkedPiece(self,position=None,tailleCouloir = 5,check_pieces=False):
        #8 pour monter 16 pour descendre
        savedPosition = position
        i=0
        random_escalier = 0
        random_escalier = random.randint(0,len(self.linked) -1)
        if self.linked != None:
            
            for direction in self.linked:
                graphique_count= dict()
                position = savedPosition
                #8 ESCALIER HAUT
                #Premiere piece ->

                #16 ESCALIER BAS
                #premiere piece -> graphique_count[16] = 0

                
                graphique_count[8] = graphique_count[16] = graphique_count[15] = 1
                if random_escalier == i:

                    graphique_count[16] = 0
                if i==0:

                    graphique_count[8] = 0
                if i == len(self.linked)-1:
                    graphique_count[17] = 0
                if direction == 'Droite':
                    
                    if position == None:
                        position= random.randint(0,len(self.taille))
                        
                    #while(self.piece[position][-1] != 1):
                        #position= random.randint(0,len(self.taille))
                    """self.piece[position][-1] = 1
                    self.piece[position][-2] = 1"""
                    nouvellePiece = self.piece
                    self.createRoom(graphique_count=graphique_count)
                    while not self.check_jouabilite() and check_pieces:
                        self.createRoom(graphique_count=graphique_count)
                    temp = nouvellePiece
                    nouvellePiece = self.piece
                    self.piece = temp
                    nouvellePiece = self.__createPiece(graphique_count=graphique_count)
                    self.rognerPiece()
                    

                    for _ in range(0,tailleCouloir):
                        self.piece[position].append(1)
                    self.equilibrerTaillePiece()
                    self.rognerPiece()
                    self.ajouterMatrice(nouvellePiece)
                    self.equilibrerTaillePiece()
                    

                if direction == 'Gauche':
                    

                    #while(self.piece[position][-1] != 1):
                        #position = random.randint(0,len(self.taille))
                    nouvellePiece = self.piece
                    
                    self.createRoom(graphique_count=graphique_count)
                    while(not self.check_jouabilite() and check_pieces):
                        self.createRoom(graphique_count=graphique_count)
                    if position == None:
                        position = random.randint(0,min(len(self.piece),len(nouvellePiece)) -1)
                    for _ in range(0,tailleCouloir):
                        self.piece[position].append(1)
                    self.piece[position][-1] = 1
                    self.piece[position][-2] = 1
                    self.equilibrerTaillePiece()
                    self.rognerPiece()
                    self.ajouterMatrice(nouvellePiece)
                    self.equilibrerTaillePiece()
                    


                if direction == 'Haut':
                    self.piece = numpy.rot90(self.piece,-1).tolist()
                    self.rognerPiece()


                    

                    #while(self.piece[position][-1] != 1):
                        #position = random.randint(0,len(self.taille))
                    nouvellePiece = self.piece
                   

                    self.createRoom(graphique_count=graphique_count)
                    while not self.check_jouabilite() and check_pieces:
                        self.createRoom(graphique_count=graphique_count)
                    if position == None:
                        position = random.randint(0,min(len(self.piece),len(nouvellePiece)) -1)
                    nouvellePiece[position][0] =1
                    nouvellePiece[position][1] = 1
                    nouvellePiece[position][2]=1
                    for _ in range(0,tailleCouloir):
                        self.piece[position].append(1)
                    self.piece[position][-1] = 1
                    self.piece[position][-2] = 1
                    self.piece[position][-3]=1
                    self.equilibrerTaillePiece()
                    self.ajouterMatrice(nouvellePiece)
                   
                    numpyPiece = numpy.rot90(self.piece,1)
                    self.piece = numpyPiece.tolist()
                i+=1
            self.alreadySpawn = True
        self.equilibrerTaillePiece()
                


                





    #permet de donner un effet de profondeur sur la map:
    #affiche le personnage derriere des meubles si il est effectivement derriere des meubles
    def update_graph(self,perso):
        kdebut=1
        udpate_index=[]
        self.donotBlit=[]
        self.retour=[]
        y=0
        for i in self.graphique_collision:
            if perso.rect_persoDonjon.colliderect(i):
                if perso.rect_persoDonjon.y-10 < i.y:
                    self.__checkVoisin(y,self.donotBlit,first=True)
            y+=1
        return self.retour
    
    
    
    #methode privee, ne pas utiliser
    #utilisee par update_graph(), elle permet de ne blit que le nombre minimum de meubles
    #bug connu : mauvais enchainement de blit
    def __checkVoisin(self,index,donotBlit,first=False):
        if index not in self.donotBlit:
            self.donotBlit.append(index)
            image = self.image_collision_graphique[index][0]
            if first : image.set_alpha(200)
            self.retour.append([image,self.image_collision_graphique[index][1]])
        if self.voisin_collision[index] != []:
            for i in self.voisin_collision[index]:
                self.__checkVoisin(i,self.donotBlit)


    #methode permettant de savoir si une piece est jouable ou non
    #une piece est consideree jouable si le joueur peut acceder a tous les elements du parquet, les escaliers et les coffres
    def check_jouabilite(self,doEH=False,doEB=False,doTe=False):
        testEH,testEB,testTe=False,False,False
        for i in self.piece:
            if 8 in i:
                
                testEH = True

            if 16 in i:   
                testEB=True
            if 17 in i:
                testTe =True
        if doEH==True and testEH ==False:
            return False
        if doEB==True and testEB ==False:
            return False
        if doTe==True and testTe ==False:

            return False
        self.pathMatrice = [[1 if self.piece[y][x] in self.important_graph else 0 if self.piece[y][x] == 0 else 100 for x in range(len(self.piece[y]))] for y in range(len(self.piece))]
        #assert len(self.pathMatrice) == len(self.pathMatrice[0])
        #permet de regarder si tous les endroits importants du donjon
        #sont atteignables
        start = [[x,y] for x in range(len(self.piece[0])) for y in range(len(self.piece)) if self.piece[y][x] == 15]

        self.__checkPath(start[0][0],start[0][1])
        for y in self.pathMatrice:
            if 1 in y:
                return False
        return True



    #methode privee utilisee par check_jouabilite()
    def __checkPath(self,x,y):


        #si on est dans un endroit, on a potentiellement acces
        #aux quatre directions : droite gauche haut bas
        if self.pathMatrice[y][x] > 0:
            self.pathMatrice[y][x] = -1


            #si on ne vient pas de la gauche
            #et qu'on n'est pas au bord de la carte
            if (x!=0 and self.pathMatrice[y][x-1] != -1):
                if (self.piece[y][x-1] == 1) and self.piece[y][x-1] != 0 :
                    self.__checkPath(x-1,y)
                if(self.pathMatrice[y][x-1] in self.important_graph):
                    self.pathMatrice[y][x-1] =-1

            #idem mais droite
            if(x!=len(self.piece[y])-1 and self.pathMatrice[y][x+1] != -1):
                if (self.piece[y][x+1] == 1) and self.piece[y][x+1] != 0:
                    self.__checkPath(x+1,y)
                if(self.pathMatrice[y][x+1] in self.important_graph):
                    self.pathMatrice[y][x+1] =-1

            #idem mais haut
            if(y!=0 and self.pathMatrice[y-1][x]!=-1):
                if (self.piece[y-1][x] ==1)and self.piece[y-1][x] != 0:
                    self.__checkPath(x,y-1)
                if(self.pathMatrice[y-1][x] in self.important_graph):
                    self.pathMatrice[y-1][x] =-1

            #idem mais bas
            if(y!=len(self.piece)-1 and self.pathMatrice[y+1][x]!=-1):
                if (self.piece[y+1][x] ==1) and self.piece[y+1][x] != 0:
                    self.__checkPath(x,y+1)
                if(self.pathMatrice[y+1][x] in self.important_graph):
                    self.pathMatrice[y+1][x] =-1
        

    #x et y sont le spawn du joueur


    #methode sauvegardant une piece dans un fichier
    #la sauvegarde se situe obligatoirement dans le fichier saves
    #arguement nom_fichier : nom_du fichier avec l'extension .txt obligatoire
    def save(self,nom_fichier,ecrireFin=False):
        relative_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"saves/")
        print(relative_path)
        ecrase = True
        mode = "w"
        if nom_fichier in os.listdir(relative_path) and not ecrireFin:
            print("Fichier %s existe deja, voulez-vous l'ecrase ? : (O/N)" % nom_fichier)
            rep = input("\n")
            while(rep not in ["O","N"]):
                rep = input("\n")
            ecrase = (rep == "O")
        if nom_fichier[-4:] != ".txt":
            print("Le fichier n'est pas un .txt")
        elif ecrase:
            if ecrireFin:mode="a"
            fichier = open(os.path.join(relative_path,nom_fichier),mode)
            for y in range(len(self.piece)):
                for x in range(len(self.piece[0])):
                    fichier.write("%i "%(self.piece[y][x]))
                fichier.write("\n")
            fichier.write("end\n")
            fichier.close()
            
    #methode permettant de creer une piece a partir d'un fichier
    def load(self,nom_fichier):
        relative_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"saves/")
        fichier = open(os.path.join(relative_path,nom_fichier),"r")
        self.piece = []
        ligne = []
        x=0
        y=0
        max=0
        chaine =""
        for things in fichier:
            if things == "end":
                break
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
                        self.piece.append(ligne)
                        if(x>max):
                            max=x
                        x=0
                        ligne = []
                        chaine =""
                    else:
                        chaine +=things[i]
        self.equilibrerTaillePiece()
        fichier.close()

    def equilibrerTaillePiece(self):
        nbreMaxLigne = max((len(self.piece[i]) for i in range(len(self.piece))))
        nbreColonne = len(self.piece)
        maxTake = max(nbreMaxLigne,nbreColonne)
        for y in range(len(self.piece)):
            for x in range(len(self.piece[y]),maxTake):
                self.piece[y].append(0)
        for a in range(len(self.piece),maxTake):
            self.piece.append([0 for y in range(maxTake)])
        assert len(self.piece[0]) == len(self.piece) == len(self.piece[-1])

    def rognerPiece(self):

        self.equilibrerTaillePiece()
        lastZeroRow = 0
        for y in range(len(self.piece)):
            for i in range(len(self.piece)-1,0,-1):
                if self.piece[y][i] == 1:
                    if i+1 > lastZeroRow:
                        lastZeroRow = i+1

                    break
        lastZeroCol =0
        x=0
        for i in range(len(self.piece[x])):
            for y in range(len(self.piece)-1,0,-1):
                if self.piece[y][i] ==1:
                    if y + 1 > lastZeroCol:
                        lastZeroCol = y+1

                    break
                x+=1


        firstZeroRow = len(self.piece[0])
        firstZeroCol = len(self.piece)
        changedZeroRow = False
        changedZeroCol = False
        for y in range(len(self.piece)):
            for i in range(len(self.piece[i])):
                if self.piece[y][i] ==1:
                    if i-1 >= 0 and i-1<firstZeroRow:
                        firstZeroRow = i-1
                        changedZeroRow = True
                    break
        x=0
        
        for i in range(len(self.piece[0])):
            for y in range(len(self.piece)):
                if self.piece[y][i] ==1:
                    if y -1 >= 0 and  y-1< firstZeroCol:
                        firstZeroCol = y-1
                        changedZeroCol = True

                    break
                x+=1    
        if not changedZeroCol:firstZeroCol=0
        if not changedZeroRow:firstZeroRow=0


        self.piece = [[self.piece[y][x] for x in range(firstZeroRow,lastZeroRow)] for y in range(lastZeroCol)]


    def refresh(self):
        x=0
        y=0
        for i in range(0,round(self.display.get_height()/self.heightPiece)):
            for j in range(0,round(self.display.get_width()/self.lengthPiece)):
                self.display.blit(self.vide,(x,y))
                
                x+=self.lengthPiece//2
                y+= self.heightPiece//4
            y= (self.heightPiece//4)*(i+1)
            x =(self.lengthPiece//2)*(i+1)
        

    #objectif de cette méthode est de "coller une matrice à une autre"
    #pour ça
    def ajouterMatrice(self,matrice):
        result = [[0 for _ in range(len(self.piece[0]) + len(matrice[0]))] for _ in range(max(len(self.piece), len(matrice)))]
        
        for y in range(max(len(self.piece), len(matrice))):
            for x in range(len(self.piece[0]) + len(matrice[0]) -1):
                

                if len(self.piece) < len(matrice):
                    if x < len(self.piece[0]):
                        if y <len(self.piece):
                            result[y][x] = self.piece[y][x]
                    else:
                        result[y][x] = matrice[y][x-len(self.piece[0])]


                else:

                    if x< len(self.piece[0]):
                        result[y][x] = self.piece[y][x]
                    else:
                        if y< len(matrice):
                            result[y][x] = matrice[y][x-len(self.piece[0])]

        self.piece = result
     
        

"""
#<---Exemple de creation de piece-->
pygame.init()
pygame.display.set_caption("Test")
display = pygame.display.set_mode((1200,800))
display.fill((255,255,0))
pygame.display.flip()

piece = Piece(display) #initialisation de la piece
piece.createRoom() #creation de la piece (initialisation de la matrice piece.piece)
piece.afficherPiece() #affichage COMPLET de la piece
piece.wait() #appuyer sur ESPACE pour quitter
pygame.quit()

"""