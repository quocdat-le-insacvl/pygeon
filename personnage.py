from competences import Competence
from basic_actions import Actions
from feats import Feat
import pygame
class Object():
    def __init__(self,name,value=None):
        self.name = name
        self.value = value


  
class Perso():
    def __init__(self,STR=10,DEX=10,CON=10,INT=10,WIS=10,CHA=10,hp=10,hp_max=10,inventaire=10,name=None,classe=None,level=0,xp=0):
        super().__init__()
        self.name=name
        self.action=Actions(0)
        self.feats=[]
        self.x=100
        self.y=400
        self.classe = classe
        self.level = level
        self.competence=Competence(self.classe)
        self.xp = xp
        self.hit_dice=0
        self.nb_hit_dice=0
        self.hp = hp
        self.hp_max = hp_max
        self.mana=100
        self.difficulty = 10
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        self.inventaire = inventaire
        self.armor = dict()
        for i in range(0,6):     # 0 : HEAD 1 : TORSE 2 : COUE  3 BOTTE 4 : MAIN GAUCHE : 5 MAIN DROITE
            self.armor[i] = None
    
    def levelupchange(self):
        #SOURCE https://www.d20pfsrd.com/Gamemastering/#Table-Experience-Point-Awards
        
        #lvl_life = (1000,3000,6000,10500,16000,23500,33000,46000,62000,82000,108000,140000,185000,240000,315000,410000,530000,685000,880000)
        #lvl max=5, change position of float("inf") to change the max lvl
        lvl_XP = (400,600,800,1200,1600,float("inf"),2400,3200,4800,6400,9600,12800,19200,25600,38400,51200,76800,102400,153600,204800)
        if self.level==0:
            print("selectionner vos premiers attributs")
            self.level=1
            self.competence.competence1()
            self.nb_hit_dice=1
            self.hp_max=8+self.ability_score(3) 
            self.hp=self.hp_max
        elif self.xp>=lvl_XP[self.level-1]:
            self.level+=1
            print("level up")
            print(self.level)
            #competences à definir
            if self.level==2: self.competence.competence2()
            elif self.level==3: self.competence.competence3()
            elif self.level==4: self.competence.competence4()
            elif self.level==5: self.competence.competence5()
            #fin des competence initialisation des statistiques de base
            self.nb_hit_dice=self.level
            self.hp_max=8+self.ability_score(3)
            self.hp_max+=(self.level-1)*(self.hit_dice/2+self.ability_score(3))
            self.hp=self.hp_max


    def ability_score(self,caracteristique):
        #permet d'augmenter ou de diminuer ses chances de réussir une action
        #STR=1, DEX=2, CON=3, INT=4, WIS=5, CHA=6
        caract=[self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA]
        return (caract[caracteristique]-10)/2


    # def stats_up(self,stat,facteur,temps):
    #     #STR=1, DEX=2, CON=3, INT=4, WIS=5, CHA=6
    #     #facteur c'est le multiplicateur, temps c'est le nombre de tours que la modification prend effet : 0 rend l'effet permanent
    #     stats=[self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA]
    #     self.bonus=Bonus(self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA,temps)
        
    #     stats[stat]=facteur*stats[stat]

    
    def rest(self):
        #vie que récupère le joueur après s'être reposé
        #coder un lit pour que le joueur puisse se reposer, faut faire le temps encore
        self.hp+=self.level*self.action.dice(self.hit_dice)
        if self.hp>self.hp_max:
            self.hp=self.hp_max

    def update_hp_bar(self,surface):
        bar_color=(113,255,51)
        hp_pourcent=(self.hp/self.hp_max)*100
        bar_position=(self.x,self.y,(hp_pourcent/2 if hp_pourcent>0 else 0),10)
        barmax_color=(255,60,51)
        hp_max_pourcent=self.hp_max/self.hp_max*100
        barmax_position=(self.x,self.y,hp_max_pourcent/2,10)
        pygame.draw.rect(surface, barmax_color, barmax_position)
        pygame.draw.rect(surface, bar_color, bar_position)


