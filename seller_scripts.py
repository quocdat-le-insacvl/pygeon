from inventory import Shop,Inventaire
from items import *
from fonction_load_image import *
from fonction import *
import pygame
from entity import Collide_box
from os import path
key = list(Wikitem.keys())
path_pygeon = path.dirname(__file__)
path_addon = path.join(path_pygeon, 'Addon')


seller_1_img = pygame.image.load(path.join(path_addon,r'seller\seller_1\vendeur_1.png'))
seller_1_img = pygame.transform.scale(seller_1_img,(3*seller_1_img.get_width(),3*seller_1_img.get_height()))
seller_2_img = pygame.image.load(path.join(path_addon,r'seller\seller_2\vendeur_3_1.png'))
seller_2_img = pygame.transform.scale(seller_2_img,(3*seller_2_img.get_width(),3*seller_2_img.get_height()))
seller_3_img = pygame.image.load(path.join(path_addon,r'seller\seller_3\vendeur_4_1.png'))
seller_3_img = pygame.transform.scale(seller_3_img,(3*seller_3_img.get_width(),3*seller_3_img.get_height()))
seller_4_img = pygame.image.load(path.join(path_addon,r'seller\seller_4\vendeur_2_1.png'))
seller_4_img = pygame.transform.scale(seller_4_img,(3*seller_4_img.get_width(),3*seller_4_img.get_height()))
seller_5_img = pygame.image.load(path.join(path_addon,r'seller\seller_5\seller_1_idle_1.png'))
seller_5_img = pygame.transform.scale(seller_5_img,(3*seller_5_img.get_width(),3*seller_5_img.get_height()))



# SELLER_1

seller_1_inv = Inventaire(7,5)
seller_1_inv.ajouteritems(Bow1)
seller_1_inv.ajouteritems(Bow7)
seller_1_inv.ajouteritems(Bow11)
seller_1_inv.ajouteritems(Bow13)
seller_1_inv.ajouteritems(Mace8)
seller_1_inv.ajouteritems(Mace7)
seller_1_inv.ajouteritems(Mace11)


seller_1 = Shop(seller_1_inv,7280,1430,seller_1_img,'Patrick','Seller',talking="Bienvenue dans mon magasin !",size_collide_box=2)

# SELLER_2

seller_2_inv = Inventaire(7,5)
seller_2_inv.ajouteritems(Sword1)
seller_2_inv.ajouteritems(Sword4)
seller_2_inv.ajouteritems(Sword8)
seller_2_inv.ajouteritems(Sword9)
seller_2_inv.ajouteritems(Sword13)
seller_2_inv.ajouteritems(Sword16)
seller_2_inv.ajouteritems(Spear1)
seller_2_inv.ajouteritems(Spear5)
seller_2_inv.ajouteritems(Spear9)
seller_2_inv.ajouteritems(Spear13)
seller_2_inv.ajouteritems(Spear14)


seller_2 = Shop(seller_2_inv,9250,485,seller_2_img,'Sebastien','Seller',talking="Bienvenue dans mon magasin !",size_collide_box=2)

# SELLER_3

seller_3_inv = Inventaire(7,5)
seller_3_inv.ajouteritems(A_Armor04)
seller_3_inv.ajouteritems(A_Armor05)
seller_3_inv.ajouteritems(A_Armour01)
seller_3_inv.ajouteritems(A_Armour02)
seller_3_inv.ajouteritems(A_Armour03)
seller_3_inv.ajouteritems(A_Clothing01)
seller_3_inv.ajouteritems(A_Clothing02)
seller_3_inv.ajouteritems(A_Shoes01)
seller_3_inv.ajouteritems(A_Shoes02)
seller_3_inv.ajouteritems(A_Shoes03)
seller_3_inv.ajouteritems(A_Shoes04)
seller_3_inv.ajouteritems(A_Shoes05)
seller_3_inv.ajouteritems(A_Shoes06)
seller_3_inv.ajouteritems(A_Shoes07)
seller_3_inv.ajouteritems(C_Elm01)
seller_3_inv.ajouteritems(C_Hat01)
seller_3_inv.ajouteritems(C_Elm03)
seller_3_inv.ajouteritems(C_Elm04)




seller_3 = Shop(seller_3_inv,10870,1395,seller_3_img,'Paul','Seller',talking="Bienvenue dans mon magasin !",size_collide_box=2)

# SELLER_4

seller_4_inv = Inventaire(7,5)
seller_4_inv.ajouteritems(Ac_Medal1)
seller_4_inv.ajouteritems(Ac_Medal2)
seller_4_inv.ajouteritems(Ac_Medal3)
seller_4_inv.ajouteritems(Ac_Medal4)
seller_4_inv.ajouteritems(Ac_Necklace01)
seller_4_inv.ajouteritems(Ac_Necklace02)
seller_4_inv.ajouteritems(Ac_Necklace03)
seller_4_inv.ajouteritems(Ac_Necklace04)
seller_4_inv.ajouteritems(Ac_Ring04)



seller_4 = Shop(seller_4_inv,11270,2345,seller_4_img,'Lucas','Seller',talking="Bienvenue dans mon magasin !",size_collide_box=2)

# SELLER_5

seller_5_inv = Inventaire(7,5)
seller_5_inv.ajouteritems(I_C_YellowPepper)
seller_5_inv.ajouteritems(Mushroom)
seller_5_inv.ajouteritems(Cherry)
seller_5_inv.ajouteritems(Meat)
seller_5_inv.ajouteritems(Watermellon)
seller_5_inv.ajouteritems(FishTail)
seller_5_inv.ajouteritems(P_Red1)
seller_5_inv.ajouteritems(P_Red2)
seller_5_inv.ajouteritems(P_Red3)


seller_5 = Shop(seller_5_inv,8980,1800,seller_5_img,'Flavian','Seller',talking="Bienvenue dans mon magasin !",size_collide_box=2)

list_seller =[]
list_seller.append(seller_1)
list_seller.append(seller_2)
list_seller.append(seller_3)
list_seller.append(seller_4)
list_seller.append(seller_5)
'''
all_items = Inventaire(23,16)
for x in key:
    all_items.ajouteritems(x)
running = True
click = False
while running:
    all_items.print_inventory_bis(0,0,print_info_on_mouse=True)
    running,click = basic_checkevent(click)
    pygame.display.update()'''