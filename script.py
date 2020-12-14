
from pygame.locals import *
from personnage import Perso
from inventory import *
from entity import Entity
from items import *

pack = Inventaire(4,6)
pack_bis = Inventaire(5,5)
player = Perso(10,10,10,10,10,10,100,150,pack_bis)
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
demon = pygame.image.load(path.join(path_demon_walk, 'walk_1.png')).convert_alpha()
demon = pygame.transform.scale(demon,(10*demon.get_width(),10*demon.get_height()))
vendeur_1 = pygame.image.load(path.join(path_seller, 'seller_1_idle_1.png')).convert_alpha()

tavern2_img = pygame.image.load(path.join(path_addon, 'medieval-tavern_00000.png')).convert_alpha()
tavern2_img = pygame.transform.scale(tavern2_img,(2*tavern2_img.get_width(),2*tavern2_img.get_height()))

vendeur_1 = pygame.transform.scale(vendeur_1,(3*vendeur_1.get_width(),3*vendeur_1.get_height()))
entity_1 = Entity(9250-tavern_img.get_width()//2,175-tavern_img.get_height()//2,tavern_img,'Tavern','Building')
entity_2 = Entity(10000,1000,demon,'Demon','Monster')
entity_3 = Entity(8830,1505-tavern_img.get_height()//2,tavern2_img,'Tavern','Building')
entity_4 = Shop(pack,8660,790,seller_1_hide["seller_1_idle_1.png"],"seller_1","Seller",seller_1_animation,"Bonjour !")
entity_5 = Shop(pack,9260,490,seller_1_hide["seller_1_idle_2.png"],"seller_1","Seller",seller_1_animation,"Bonjour Aventurier ! Vous voulez voir mes produits ?")
entity_6 = Entity(7350-tavern_img.get_width()//2,1125-tavern_img.get_height()//2,tavern_img,"Tavern","Building")
entity_7 = Entity(11060-tavern_img.get_width()//2,1080-tavern_img.get_height()//2,tavern_img,"Tavern","Building")
entity_8 = Entity(10540,1790-tavern_img.get_height()//2,tavern2_img,"Tavern","Building")
wizard = Entity(100,100,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))
wizard_2 = Entity(100,100,wizard_hide["wizard_idle_1.png"],"wizard","Monster",wizard_animation,size=(300,300))

list_static_entity = []
list_mooving_entity = []

list_static_entity.append(entity_1)

list_static_entity.append(entity_6)
list_static_entity.append(entity_7)

list_static_entity.append(entity_8)
list_static_entity.append(entity_3)

list_mooving_entity.append(entity_4)
list_mooving_entity.append(entity_5)
list_mooving_entity.append(entity_2)
list_mooving_entity.append(wizard)
list_mooving_entity.append(wizard_2)
