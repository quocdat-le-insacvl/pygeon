from settings.setting_monster import MONSTER_SIZE
from entity import Entity,Collide_box
import pygame
from settings.load_img import *
from settings.screen import *
from settings.color import *
from settings.load_img import ava_perso
import random

liste_type_monste = [demon_1_animation,demon_animation,squelton_animation,wizard_animation,dark_wizard_animation]




class Monster(Entity):
    def __init__(self, pos_x, pos_y, img, name, which_type, animation_dict=None, talking='', size=(0,0), decalage=[0,0], size_monster='Small', walking_speed=30,size_collide_box = 1):
        super().__init__(pos_x, pos_y, img, name, which_type, animation_dict=animation_dict, talking=talking, size=size, decalage=decalage,size_collide_box=size_collide_box)
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
        self.group_monster = []
        self.collide_box_interact = Collide_box(1)
        self.collide_patrouille = Collide_box(2)
        self.is_aggresive = True
        self.change_direction = 0
        self.mouvement = [0,0]
        self.STR = 10
        
    def init_collide_patrouille(self):
        self.collide_patrouille.pos_x = int ( self.pos_x - self.collide_patrouille.img_collide.get_width()//2 + self.img.get_width()//2)
        self.collide_patrouille.pos_y = int ( self.pos_y + self.img.get_height() - self.collide_patrouille.img_collide.get_height()//2)
    def moove_patrouille(self,player,list_monster):
        if self.change_direction ==0:
            self.update_collide_monster()
            self.init_collide_patrouille()
        if self.change_direction == 100:
            m = random.randint(0,3)
            if m==0:
                self.mouvement = [2,1]
            elif m ==1:
                self.mouvement = [-2,1]
            elif m==2:
                self.mouvement = [-2,-1]
            else:
                self.mouvement = [2,-1]

            self.change_direction = 1
        self.change_direction +=1
        if not player.masks.overlap(self.collide_box.mask,((self.collide_box.pos_x + self.mouvement[0])-player.pos_x,(self.collide_box.pos_y+ self.mouvement[1])-(player.pos_y+130))):
            if self.collide_patrouille.mask.overlap(self.collide_box_interact.mask,((self.collide_box_interact.pos_x + self.mouvement[0])-self.collide_patrouille.pos_x,(self.collide_box_interact.pos_y+ self.mouvement[1])-self.collide_patrouille.pos_y)):
                self.pos_x += self.mouvement[0]
                self.pos_y += self.mouvement[1]
            else:
                if self.collide_patrouille.mask.overlap(self.collide_box_interact.mask,((self.collide_box_interact.pos_x)-self.collide_patrouille.pos_x,(self.collide_box_interact.pos_y)-self.collide_patrouille.pos_y)):
                    self.change_direction = 100
                else:
                    self.pos_x += (self.collide_patrouille.pos_x+self.collide_patrouille.img_collide.get_width()//2 - self.pos_x)//400
                    self.pos_y += (self.collide_patrouille.pos_y+self.collide_patrouille.img_collide.get_height()//2 - self.pos_y)//400
        elif not player.visible:
            if self.collide_patrouille.mask.overlap(self.collide_box_interact.mask,((self.collide_box_interact.pos_x + self.mouvement[0])-self.collide_patrouille.pos_x,(self.collide_box_interact.pos_y+ self.mouvement[1])-self.collide_patrouille.pos_y)):
                self.pos_x += self.mouvement[0]
                self.pos_y += self.mouvement[1]
            else:
                if self.collide_patrouille.mask.overlap(self.collide_box_interact.mask,((self.collide_box_interact.pos_x)-self.collide_patrouille.pos_x,(self.collide_box_interact.pos_y)-self.collide_patrouille.pos_y)):
                    self.change_direction = 100
                else:
                    self.pos_x += (self.collide_patrouille.pos_x+self.collide_patrouille.img_collide.get_width()//2 - self.pos_x)//400
                    self.pos_y += (self.collide_patrouille.pos_y+self.collide_patrouille.img_collide.get_height()//2 - self.pos_y)//400
        else:
            if not self.is_aggresive :
                for x in self.group_monster:
                    if (x.pos_x - player.pos_x ) >0:
                        x.pos_x += 4
                    else:
                        x.pos_x -=4
                    if (x.pos_y - player.pos_y ) < 0:
                        x.pos_y += 2
                    else:
                        x.pos_y -=2
                    x.update_pos_collide()
                    x.update_collide_monster()
            else:
                for x in self.group_monster:
                    if (x.pos_x - player.pos_x ) >0:
                        x.pos_x -= 4
                    else:
                        x.pos_x +=4
                    if (x.pos_y - player.pos_y ) < 0:
                        x.pos_y += 2
                    else:
                        x.pos_y -=2
                    x.update_pos_collide()
                    x.update_collide_monster()
        self.update_pos_collide()
        self.update_collide_monster()
        self.update_group_monster(list_monster)
    def moove_monster(self,mouvement,player,list_monster):
        if not player.masks.overlap(self.collide_box.mask,((self.collide_box.pos_x + mouvement[0])-player.pos_x,(self.collide_box.pos_y+ mouvement[1])-(player.pos_y+130))):
            self.pos_x += mouvement[0]
            self.pos_y += mouvement[1]    

        else:
            if not self.is_aggresive :
                for x in self.group_monster:
                    if (x.pos_x - player.pos_x ) >0:
                        x.pos_x += 4     
                    else:
                        x.pos_x -=4
                    if (x.pos_y - player.pos_y ) < 0:
                        x.pos_y += 2

                    else:
                        x.pos_y -=2
                    x.update_pos_collide()
                    x.update_collide_monster()
            else:
                for x in self.group_monster:
                    if (x.pos_x - player.pos_x ) >0:
                        x.pos_x -= 4
                    else:
                        x.pos_x +=4
                    if (x.pos_y - player.pos_y ) < 0:
                        x.pos_y += 2
                    else:
                        x.pos_y -=2
                    x.update_pos_collide()
                    x.update_collide_monster()
                
        self.update_pos_collide()
        self.update_collide_monster()
        self.update_group_monster(list_monster)
    def init(self):
        self.update_collide_monster()
        self.update_pos_collide()
    def set_group_monster(self,list_monster):
        self.update_group_monster(list_monster)
        
    def update_collide_monster(self):
        self.collide_box_interact.pos_x = int ( self.pos_x - self.collide_box_interact.img_collide.get_width()//2 + self.img.get_width()//2 )
        self.collide_box_interact.pos_y = int ( self.pos_y + self.img.get_height() - self.collide_box_interact.img_collide.get_height()//2)
    def update_group_monster(self,list_monster):
        self.group_monster = []
        for x in list_monster:
            if x.collide_box.mask.overlap(self.collide_box.mask,(self.collide_box.pos_x-x.collide_box.pos_x,self.collide_box.pos_y-x.collide_box.pos_y)):
                if not self.group_monster.__contains__(x):
                    self.group_monster.append(x)
