from inventory import Shop,Inventaire
from items import *
from fonction_load_image import *
import pygame
from os import path

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

seller_1 = Shop(seller_1_inv,7280,1430,seller_1_img,'Patrick','Seller',talking="Bienvenue dans mon magasin !")

# SELLER_2

seller_2_inv = Inventaire(7,5)
seller_2_inv.ajouteritems(Sword1)
seller_2 = Shop(seller_2_inv,9250,485,seller_2_img,'Sebastien','Seller',talking="Bienvenue dans mon magasin !")

# SELLER_3

seller_3_inv = Inventaire(7,5)

seller_3 = Shop(seller_3_inv,10870,1395,seller_3_img,'Paul','Seller',talking="Bienvenue dans mon magasin !")

# SELLER_4

seller_4_inv = Inventaire(7,5)

seller_4 = Shop(seller_4_inv,11270,2345,seller_4_img,'Lucas','Seller',talking="Bienvenue dans mon magasin !")

# SELLER_5

seller_5_inv = Inventaire(7,5)

seller_5 = Shop(seller_5_inv,8980,1800,seller_5_img,'Flavian','Seller',talking="Bienvenue dans mon magasin !")

list_seller =[]
list_seller.append(seller_1)
list_seller.append(seller_2)
list_seller.append(seller_3)
list_seller.append(seller_4)
list_seller.append(seller_5)
