
import personnage,pickle
from pygame.locals import *
from personnage import Perso
from inventory import Inventaire
from items import *


pack = Inventaire(4,6)
pack_bis = Inventaire(5,5)
player = Perso(10,10,10,10,10,10,100,150,pack_bis)
player.xp = 500
playerbis = Perso(20,20,20,20,20,20,20,20,pack)


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




