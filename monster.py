from settings.setting_monster import MONSTER_SIZE
from entity import Entity,Collide_box
from personnage import Stats
import pygame
from settings.load_img import *
from settings.screen import *
from settings.color import *
from settings.police import ColderWeather
from settings.load_img import ava_perso
from items import Wikitem, choisir_alea, choisir_alea_armor
from basic_actions import *
from fonctions import wblack
import random
key = list(Wikitem.keys())
liste_type_monste = [demon_1_animation,demon_animation,squelton_animation,wizard_animation,dark_wizard_animation]

stats_nv1 = [9,9,9,12,12,12,10]

stats_nv2 = [12,12,12,12,12,12,15]

stats_nv3 = [12,12,12,12,12,12,20]

stats_nv4 = [13,13,13,13,13,13,25]

stats_nv5 = [15,15,15,15,15,15,30]


list_stats = []
list_stats.append(stats_nv1)
list_stats.append(stats_nv2)
list_stats.append(stats_nv3)
list_stats.append(stats_nv4)
list_stats.append(stats_nv5)


class Monster(Entity,Stats):
    def __init__(self, pos_x, pos_y, img, name, which_type, decalage,animation_dict=None, talking='', size=(0,0), size_monster='Small', walking_speed=30,size_collide_box = 1,donjon=False):
        super().__init__(pos_x, pos_y, img, name, which_type, animation_dict=animation_dict, talking=talking, size=size, decalage=decalage,size_collide_box=size_collide_box,donjon=donjon)
        if int(which_type) == 4:
            which_type = randrange(4,5)
        Stats.__init__(self,list_stats[int(which_type)-1][0],list_stats[int(which_type)-1][1],list_stats[int(which_type)-1][2],list_stats[int(which_type)-1][3],list_stats[int(which_type)-1][4],list_stats[int(which_type)-1][5],list_stats[int(which_type)-1][6])
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

        self.collide_box_interact = Collide_box(1,donjon=donjon)
        self.collide_patrouille = Collide_box(2)
        self.is_aggresive = True
        self.change_direction = 0
        self.mouvement = [0,0]
        self.is_player = False
        self.level=int(which_type)
        self.xp = (50*self.level)**self.level
        self.stats=list_stats[int(which_type)-1]
        self.skills=[0,0,0,0,0,0]
        self.action = Actions()
        self.attack = int(which_type)
        self.crit = False
        self.proficiency=2
        self.armor = dict()
        
        for i in range(0,6):     # 0 : HEAD 1 : TORSE 2 : COUE  3 BOTTE 4 : MAIN GAUCHE : 5 MAIN DROITE
            self.armor[i] = None
            
        self.armor[1],t=choisir_alea_armor()
        self.armor[4],t=choisir_alea()
        if int(which_type)<=2:
            while (key[self.armor[1]].rarete!="commun"):
                self.armor[1],t=choisir_alea_armor()
            while (key[self.armor[4]].rarete!="commun"):
                self.armor[4],t=choisir_alea()
        elif 2<int(which_type)<=3:
            while (key[self.armor[1]].rarete!="rare"):
                self.armor[1],t=choisir_alea_armor()
            while (key[self.armor[4]].rarete!="rare"):
                self.armor[4],t=choisir_alea()
        elif int(which_type)==4:
            while (key[self.armor[1]].rarete!="epique"):
                self.armor[1],t=choisir_alea_armor()
            while (key[self.armor[4]].rarete!="legendaire"):
                self.armor[4],t=choisir_alea()
        self.armor_class=self.calcul_armor()
    def check_alive(self):
        if self.hp <= 0:
            self.is_alive = False 
    def init_collide_patrouille(self):
        self.collide_patrouille.pos_x = int ( self.pos_x - self.collide_patrouille.img_collide.get_width()//2 + self.img.get_width()//2)
        self.collide_patrouille.pos_y = int ( self.pos_y + self.img.get_height() - self.collide_patrouille.img_collide.get_height()//2)
    def unmove_patrouille(self):
        self.pos_x -= self.mouvement[0]
        self.pos_y -= self.mouvement[1]

    def moove_patrouille(self,player,list_monster,donjon=False,velocity=2):
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
        if not donjon : 
            
            mask_to_get = player.masks
            test_mask =mask_to_get.overlap(self.collide_box.mask,((self.collide_box.pos_x )-player.pos_x,(self.collide_box.pos_y)-(player.pos_y+130)))
        else:
            mask_to_get = player.donjon_mask
            test_mask = mask_to_get.overlap(self.collide_box.mask,((self.collide_box.pos_x )-player.pos_x,(self.collide_box.pos_y)-(player.pos_y+90)))
        
        if not test_mask:
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
                        x.pos_x += 2*velocity
                    else:
                        x.pos_x -=2*velocity
                    if (x.pos_y - player.pos_y ) < 0:
                        x.pos_y += velocity
                    else:
                        x.pos_y -=velocity
                    x.update_pos_collide()
                    x.update_collide_monster()
            else:
                for x in self.group_monster:
                    if (x.pos_x - player.pos_x ) >0:
                        x.pos_x -= 2*velocity
                    else:
                        x.pos_x +=velocity
                    if (x.pos_y - player.pos_y ) < 0:
                        x.pos_y += velocity
                    else:
                        x.pos_y -=velocity
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
    def score(self,comp):
        """basic version of the skills effect just to provide proficiency
        this fonction must be call for all the calculs wich need ability modifier"""
        select={"str" : 0,"dex" : 1, "con" : 2, "int" : 3, "wis" : 4, "cha" : 5}
        assert(comp in select), "wrong argument for score()" 
        if self.skills[select[comp]]:
            return self.ability_score(select[comp])+self.proficiency
        else :
            return self.ability_score(select[comp])
    
    def handicap(self,comp):
        "calcul les différents handicapes, liés au poids de l'armure par exemple"
        if comp==1 and self.armor[1]!=None:
            if self.stats[comp]>8+key[self.armor[1]].dex_bonus:
                return 8+key[self.armor[1]].dex_bonus
        return self.stats[comp]

    def calcul_armor(self, type_of_calcul=0):
        """ refresh the value of the class armor, must add calcul with """
        assert(type_of_calcul==1 or type_of_calcul==0), "must add a valide type of calcul : 1 without armor"
        if type_of_calcul==0:
            if self.armor[1]!=None:
                return self.score("dex")+10+key[self.armor[1]].armor_bonus
        return self.score("dex")+10
    def calcul_attack_score(self):
        "renvoie le score de l'attaque roll pour savoir si le joueur touvhe le monstre"
        i=self.action.dice(20)
        if i==1:
            return 0
        elif i==20:
            self.crit=True
            return float("inf")
        return i+self.attack
    
    def damage(self):
        "calcule les dommages en fonction de l'arme équipée"
        bonus_deg=0
        crit=1
        dex=self.score("dex")
        if dex==-1:
            dex=0
        strong=self.score("str")
        if strong==-1:
            strong=0
        if self.crit:
            crit=2
            self.crit=False
        if self.armor[4]!=None:
            bonus_deg=self.action.dice(key[self.armor[4]].dmg)
            if key[self.armor[4]].wpn_type=="RANGED":
                return (bonus_deg+dex)*crit
        elif self.armor[5]!=None:
            bonus_deg=self.action.dice(key[self.armor[5]].dmg)
            if key[self.armor[4]].wpn_type=="RANGED":
                return (bonus_deg+dex)*crit
        if self.armor[4]!=None:
            if all([key[self.armor[4]].wpn_type!="Two Handed"]):
                bonus_deg+=self.action.dice(key[self.armor[4]].dmg)
            elif key[self.armor[4]].wpn_type=="Two Handed":
                bonus_deg+=(strong//2)*crit  
        return (bonus_deg+strong)*crit
    def ability_score(self,caracteristique):
        """calcul basique du score en fonction d'une caractéristique passée en paramètre
        STR=0, DEX=1, CON=2, INT=3, WIS=4, CHA=5"""

        return (self.handicap(caracteristique)-10)//2
    def display_lvl(self,surface,x,y):
        name = wblack(ColderWeather,str(self.level))
        name = pygame.transform.scale(name,(name.get_width() // 2,name.get_height()//2))
        screen.blit(name,(x,y + name.get_height()))


