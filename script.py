
from pygame.locals import *
from personnage import Perso,Perso_game,Perso_saveable
from inventory import *
from entity import Entity,Collide_box
from items import *
from monster import Monster
from sorcerer import Sorcerer

pack = Inventaire(7,5)
pack_bis = Inventaire(5,5)

player_2 = Perso_game(10,10,10,10,10,10,100,150,pack_bis,walk_bottom['walk_bottom_' + str(1) +'.png'].copy(),8680,2000,decalage=[30,80],size=(300,300))

player = Perso_game(10,10,10,10,10,10,100,100,pack,walk_bottom['walk_bottom_' + str(1) +'.png'],8680,800,decalage=[30,80],size=(300,300))
player_3 = Perso_game(50,10,10,10,10,10,100,100,pack,walk_bottom['walk_bottom_' + str(1) +'.png'].copy(),8680,800,decalage=[30,80],size=(300,300))

sorcerer = Sorcerer(decalage=[10,80],size=(300,300), name= "Perso1",n_case = 59)
sorcerer_2 = Sorcerer(decalage=[10,80],size=(300,300), name = "Perso2",n_case = 65)
sorcerer_3 = Sorcerer(decalage=[10,80],size=(300,300), name= "Perso3", n_case = 51)

player.xp = 500

playerbis = Perso(20,20,20,20,20,20,20,20,pack,name="Anthony",decalage=[30,80],size=(300,300))
player_for_save = Perso_saveable()


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

tavern2_img = pygame.image.load(path.join(path_addon, 'medieval-tavern_00000.png')).convert_alpha()
tavern2_img = pygame.transform.scale(tavern2_img,(2*tavern2_img.get_width(),2*tavern2_img.get_height()))

test_demon = Entity(7180, 1940, demon, 'test_demon', 'Monster',
                  demon_1_animation, size=(500, 400), decalage=[60, 0])
demon_shadow = pygame.image.load(
    path.join(path_addon, 'demon_shadow.png')).convert_alpha()
demon_shadow = pygame.transform.scale(
    demon_shadow, (10*demon_shadow.get_width(), 10*demon_shadow.get_height()))
test_demon.shadow = demon_shadow


tavern_1 = Entity(8830,1505-tavern_img.get_height()//2,tavern2_img,'Tavern','Building')
tavern_2 = Entity(9250-tavern_img.get_width()//2,175-tavern_img.get_height()//2,tavern_img,'Tavern','Building')
tavern_3 = Entity(7350-tavern_img.get_width()//2,1125-tavern_img.get_height()//2,tavern_img,"Tavern","Building")
tavern_4 = Entity(11060-tavern_img.get_width()//2,1080-tavern_img.get_height()//2,tavern_img,"Tavern","Building")
tavern_5 = Entity(10540+380,1790-tavern_img.get_height()//2+270,tavern2_img,"Tavern","Building")

list_static_entity = []



"""
list_static_entity.append(tavern_1)
list_static_entity.append(tavern_2)
list_static_entity.append(tavern_3)
list_static_entity.append(tavern_4)
list_static_entity.append(tavern_5)"""

list_mooving_entity = []


# running = True
# click = False
# while running:
#     #player.spell_bar()
#     print_turn_batlle([squelton_2,entity_2])
#     running,click = basic_checkevent(click)
#     pygame.display.update()
