# Déclaration de tout les objects pour le fonctionnement programme.
import personnage,pickle
from pygame.locals import *
from personnage import Perso
from inventory import Inventaire
from items import *



pack = Inventaire(4,6)

player = Perso(10,10,10,10,10,10,100,150,pack)
player.xp = 500
playerbis = Perso(20,20,20,20,20,20,20,20,pack)
#Godzilla = Perso(20,10,30,15,15,10,1000,150,'Godzilla')

#print("%i",joueur_recup.xp)

pack.ajouteritems(A_Shoes01)
pack.ajouteritems(E_Metal02)
pack.ajouteritems(C_Elm01)
pack.ajouteritems(Sword1)
pack.ajouteritems(Sword2)
pack.ajouteritems(Sword3)
pack.ajouteritems(Sword4)
pack.ajouteritems(Sword5)
pack.ajouteritems(Sword6)
pack.ajouteritems(Sword7)
pack.ajouteritems(Sword8)
#player.armor[0] = A_Armor04
#pack.ajouteritems(Mace)

#player.armor["Head"] = Wooden_helmet
#pack.enleveritems(Gauntlet)

#player.xp = 9000
#player.levelupchange()
#print("Level : %i \n",player.level)



