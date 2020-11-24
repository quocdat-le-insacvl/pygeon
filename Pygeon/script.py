# Déclaration de tout les objects pour le fonctionnement programme.
import personnage,pickle
from pygame.locals import *
from personnage import Perso
from inventory import Inventaire
from items import *
from entity import Entity


pack = Inventaire(4,6)
pack_bis = Inventaire(5,5)
player = Perso(10,10,10,10,10,10,100,150,pack_bis)
player.xp = 500
playerbis = Perso(20,20,20,20,20,20,20,20,pack)
entity_1 = Entity(8400,1000,seller,'Seller','Seller',100)
#Godzilla = Perso(20,10,30,15,15,10,1000,150,'Godzilla')

#print("%i",joueur_recup.xp)
pack_bis.ajouteritems(playerbis,Sword9)
pack.ajouteritems(player,A_Shoes01)
pack.ajouteritems(player,E_Metal02)
pack.ajouteritems(player,C_Elm01)

pack.ajouteritems(player,Sword1)
pack.ajouteritems(player,Sword2)
pack.ajouteritems(player,Sword3)

pack.ajouteritems(player,Sword4)
pack.ajouteritems(player,Sword5)
pack.ajouteritems(player,Sword6)
pack.ajouteritems(player,Sword7)
pack.ajouteritems(player,Sword8)
#player.armor[0] = A_Armor04
#pack.ajouteritems(Mace)

#player.armor["Head"] = Wooden_helmet
#pack.enleveritems(Gauntlet)

#player.xp = 9000
#player.levelupchange()
#print("Level : %i \n",player.level)



