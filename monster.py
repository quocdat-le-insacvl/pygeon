from settings.setting_monster import MONSTER_SIZE
from entity import Entity
import pygame
from settings.load_img import *
from settings.screen import *
from settings.color import *
from settings.load_img import ava_perso

class Monster(Entity):
    def __init__(self, pos_x, pos_y, img, name, which_type, animation_dict, talking, size, decalage, size_monster, walking_speed):
        super().__init__(pos_x, pos_y, img, name, which_type, animation_dict=animation_dict, talking=talking, size=size, decalage=decalage)
        # Rule : https://www.dndbeyond.com/sources/basic-rules/monsters#Challenge
        self.challenge = 0
        # Size of a monster => A monster can be Tiny, Small, Medium, Large, Huge, or Gargantuan.
        # Il sert pour l<Affichage et le combat aussi
        self.size_monster = size_monster
        self.size_affichage = MONSTER_SIZE[self.size_monster]
        # A monster's walking speed tells you how far it can move on its turn.
        self.walking_speed = walking_speed 
        
        # A monster that wears armor or carries a shield has an Armor Class (AC) that takes its armor, shield, and Dexterity into account. 
        # Otherwise, a monster's AC is based on its Dexterity modifier and natural armor, if any. 
        # If a monster has natural armor, wears armor, or carries a shield, this is noted in parentheses after its AC value.
