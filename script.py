
from pygame.locals import *
from personnage import Perso,Perso_game
from inventory import *
from entity import Entity
from items import *

pack = Inventaire(7,5)
pack_bis = Inventaire(5,5)
#player = Perso_game(10,10,10,10,10,10,100,150,pack_bis,walk_bottom['walk_bottom_' + str(1) +'.png'],9000,1000)
player = Perso_game(10,10,10,10,10,10,100,100,pack,walk_bottom['walk_bottom_' + str(1) +'.png'],8680,800,player_animation=player_animation)
player.xp = 500
playerbis = Perso(20,20,20,20,20,20,20,20,pack)


pack_bis.ajouteritems(Sword9)
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

### Fixing PATH
path_pygeon = path.dirname(__file__)
path_addon = path.join(path_pygeon, 'Addon')
path_police = path.join(path_addon, 'Police')
path_menu = path.join(path_addon, 'Menu')
path_demon_walk = path.join(path_addon, 'demon_walk')
path_seller = path.join(path_addon, 'seller')
###


tavern_img = pygame.image.load(path.join(path_addon, 'tavern_1.png')).convert_alpha()
tavern_img = pygame.transform.scale(tavern_img,(int(1.8*tavern_img.get_width()),int(1.8*tavern_img.get_height())))
tavern_2_img = pygame.image.load(path.join(path_addon, 'tavern_2.png')).convert_alpha()
tavern_2_img = pygame.transform.scale(tavern_2_img,(int(1.7*tavern_2_img.get_width()),int(1.7*tavern_2_img.get_height())))
demon = pygame.image.load(path.join(path_demon_walk, 'demon_walk_1.png')).convert_alpha()
demon = pygame.transform.scale(demon,(10*demon.get_width(),10*demon.get_height()))
vendeur_1 = pygame.image.load(path.join(path_seller, 'seller_5/seller_1_idle_1.png')).convert_alpha()

tavern2_img = pygame.image.load(path.join(path_addon, 'medieval-tavern_00000.png')).convert_alpha()
tavern2_img = pygame.transform.scale(tavern2_img,(2*tavern2_img.get_width(),2*tavern2_img.get_height()))

vendeur_1 = pygame.transform.scale(vendeur_1,(3*vendeur_1.get_width(),3*vendeur_1.get_height()))
entity_1 = Entity(9250-tavern_img.get_width()//2,175-tavern_img.get_height()//2,tavern_img,'Tavern','Building')
entity_2 = Entity(10000,1000,demon,'demon_1','Monster',demon_1_animation,size=(500,400),decalage=[60,0])
entity_2bis = Entity(10000,1000,demon,'demon','Monster',demon_animation,size=(500,400),decalage=[60,0])
entity_3 = Entity(8830,1505-tavern_img.get_height()//2,tavern2_img,'Tavern','Building')
entity_4 = Shop(pack_bis,8660,790,seller_1_hide["seller_1_idle_1.png"],"seller_1","Seller",seller_1_animation,"Bonjour !")
entity_5 = Shop(pack_bis,9260,490,seller_1_hide["seller_1_idle_2.png"],"seller_1","Seller",seller_1_animation,"Bonjour Aventurier ! Vous voulez voir mes produits ?")
entity_6 = Entity(7350-tavern_img.get_width()//2,1125-tavern_img.get_height()//2,tavern_img,"Tavern","Building")
entity_7 = Entity(11060-tavern_img.get_width()//2,1080-tavern_img.get_height()//2,tavern_img,"Tavern","Building")
entity_8 = Entity(10540+380,1790-tavern_img.get_height()//2+270,tavern2_img,"Tavern","Building")
wizard = Entity(9000,800,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
wizard_2 = Entity(9000,500,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_1 = Entity(9250,685,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_2 = Entity(9250,785,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_3 = Entity(9250,885,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_4 = Entity(9250,985,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_5 = Entity(9350,685,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_6 = Entity(9450,785,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_7 = Entity(9550,885,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_8 = Entity(9650,985,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_9 = Entity(9765,1000,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_10 = Entity(9765,1100,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_11 = Entity(9765,1200,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_12 = Entity(9765,1300,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_13 = Entity(9765,1400,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_14 = Entity(9765,1500,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_15 = Entity(9765,1600,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
squelton_16 = Entity(9765,1700,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))

dark_wizard = Entity(10000,400,dark_wizard_idle["dark_wizard_idle_1.png"],"dark_wizard","Monster",dark_wizard_animation,size=(500,500),decalage=[70,60])


list_static_entity = []
list_mooving_entity = []

"""
# For test 
test_demon = Entity(7180, 1940, demon, 'test_demon', 'Monster',
                  demon_1_animation, size=(500, 400), decalage=[60, 0])
demon_shadow = pygame.image.load(
    path.join(path_demon_walk, 'demon_shadow.png')).convert_alpha()
demon_shadow = pygame.transform.scale(
    demon_shadow, (10*demon_shadow.get_width(), 10*demon_shadow.get_height()))
test_demon.shadow = demon_shadow
# list_mooving_entity.append(test_demon)

###
"""


list_static_entity.append(entity_1)

list_static_entity.append(entity_6)
list_static_entity.append(entity_7)

list_static_entity.append(entity_8)
list_static_entity.append(entity_3)

list_mooving_entity.append(squelton_1)
list_mooving_entity.append(squelton_2)
list_mooving_entity.append(squelton_3)
list_mooving_entity.append(squelton_4)
list_mooving_entity.append(squelton_5)
list_mooving_entity.append(squelton_6)
list_mooving_entity.append(squelton_7)
list_mooving_entity.append(squelton_8)
list_mooving_entity.append(squelton_9)
list_mooving_entity.append(squelton_10)
list_mooving_entity.append(squelton_11)
list_mooving_entity.append(squelton_12)
list_mooving_entity.append(squelton_13)
list_mooving_entity.append(squelton_14)
list_mooving_entity.append(squelton_15)
list_mooving_entity.append(squelton_16)
'''list_mooving_entity.append(dark_wizard)
list_mooving_entity.append(wizard)

list_mooving_entity.append(entity_2)
list_mooving_entity.append(entity_2bis)
list_mooving_entity.append(entity_2)
list_mooving_entity.append(wizard)
list_mooving_entity.append(wizard_2)'''
