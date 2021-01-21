import pygame
from Donjon.donjon import Donjon
from settings.screen import screen
from script import player
from entity import Entity
from settings.load_img import rune_1
# DONJON LVL 1 

# SET VARIABLE ENTITY POUR PLACEMENT CARTE
entity_donjon_lvl_1_1 = Entity(0,0,rune_1,"Donjon","Donjon")
entity_donjon_lvl_1_2 = Entity(0,0,rune_1,"Donjon","Donjon")
# SET DONJON
donjon_lvl_1_1 = Donjon(1,screen,player,nbreEtage=1)
donjon_lvl_1_2 = Donjon(1,screen,player,nbreEtage=1)

# DONJON LVL 2

# SET VARIABLE ENTITY POUR PLACEMENT CARTE
entity_donjon_lvl_2_1 = Entity(0,0,rune_1,"Donjon","Donjon")
entity_donjon_lvl_2_2 = Entity(0,0,rune_1,"Donjon","Donjon")
# SET DONJON
donjon_lvl_2_1 = Donjon(2,screen,player,nbreEtage=2)
donjon_lvl_2_2 = Donjon(2,screen,player,nbreEtage=2)


# DONJON LVL 3 

# SET VARIABLE ENTITY POUR PLACEMENT CARTE
entity_donjon_lvl_3_1 = Entity(0,0,rune_1,"Donjon","Donjon")
entity_donjon_lvl_3_2 = Entity(0,0,rune_1,"Donjon","Donjon")
entity_donjon_lvl_3_3 = Entity(0,0,rune_1,"Donjon","Donjon")
# SET DONJON
donjon_lvl_3_1 = Donjon(3,screen,player,nbreEtage=3)
donjon_lvl_3_2 = Donjon(3,screen,player,nbreEtage=3)
donjon_lvl_3_3 = Donjon(3,screen,player,nbreEtage=3)


# DONJON LVL 4 

# SET VARIABLE ENTITY POUR PLACEMENT CARTE
entity_donjon_lvl_4_1 = Entity(0,0,rune_1,"Donjon","Donjon")
entity_donjon_lvl_4_2 = Entity(0,0,rune_1,"Donjon","Donjon")
entity_donjon_lvl_4_3 = Entity(0,0,rune_1,"Donjon","Donjon")
entity_donjon_lvl_4_4 = Entity(0,0,rune_1,"Donjon","Donjon")

# SET DONJON
donjon_lvl_4_1 = Donjon(4,screen,player,nbreEtage=4)
donjon_lvl_4_2 = Donjon(4,screen,player,nbreEtage=4)
donjon_lvl_4_3 = Donjon(4,screen,player,nbreEtage=4)
donjon_lvl_4_4 = Donjon(4,screen,player,nbreEtage=4)


list_entity_donjon = []

list_entity_donjon.append(entity_donjon_lvl_1_1)
list_entity_donjon.append(entity_donjon_lvl_1_2)
list_entity_donjon.append(entity_donjon_lvl_2_1)
list_entity_donjon.append(entity_donjon_lvl_2_2)
list_entity_donjon.append(entity_donjon_lvl_3_1)
list_entity_donjon.append(entity_donjon_lvl_3_2)
list_entity_donjon.append(entity_donjon_lvl_3_3)
list_entity_donjon.append(entity_donjon_lvl_4_1)
list_entity_donjon.append(entity_donjon_lvl_4_2)
list_entity_donjon.append(entity_donjon_lvl_4_3)
list_entity_donjon.append(entity_donjon_lvl_4_4)

list_donjon = []

list_donjon.append(donjon_lvl_1_1)
list_donjon.append(donjon_lvl_1_2)
list_donjon.append(donjon_lvl_2_1)
list_donjon.append(donjon_lvl_2_2)
list_donjon.append(donjon_lvl_3_1)
list_donjon.append(donjon_lvl_3_2)
list_donjon.append(donjon_lvl_3_3)
list_donjon.append(donjon_lvl_4_1)
list_donjon.append(donjon_lvl_4_2)
list_donjon.append(donjon_lvl_4_3)
list_donjon.append(donjon_lvl_4_4)
