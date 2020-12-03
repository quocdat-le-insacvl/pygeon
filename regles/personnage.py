from competences import Competence
from basic_actions import Combat
class Object():
    def __init__(self,name,value=None):
        self.name = name
        self.value = value


  
class Perso():
    def __init__(self,STR=10,DEX=10,CON=10,INT=10,WIS=10,CHA=10,hp=10,hp_max=10,inventaire=10,name=None,classe=None,level=0,xp=0):
        self.name=name
        self.combat=Combat(0)
        self.x=0
        self.y=400
        self.classe = classe
        self.level = level
        self.competence=Competence(self.classe)
        self.xp = xp 
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
        self.bonus=Bonus(self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA)
        self.inventaire = inventaire
        self.armor = dict()
        for i in range(0,6):     # 0 : HEAD 1 : TORSE 2 : COUE  3 BOTTE 4 : MAIN GAUCHE : 5 MAIN DROITE
            self.armor[i] = None
    
    def levelupchange(self):
        #SOURCE https://www.d20pfsrd.com/Gamemastering/#Table-Experience-Point-Awards
        
        #lvl_life = (1000,3000,6000,10500,16000,23500,33000,46000,62000,82000,108000,140000,185000,240000,315000,410000,530000,685000,880000)
        lvl_XP = (400,600,800,1200,1600,2400,3200,4800,6400,9600,12800,19200,25600,38400,51200,76800,102400,153600,204800,float("inf"))
        if self.level==0:
            print("selectionner vos premiers attributs")
            self.level=1
            self.competence.competence1()
        elif self.xp>=lvl_XP[self.level-1]:
            self.level+=1
            print("level up")
            print(self.level)
            if self.level==2: self.competence.competence2()
            elif self.level==3: self.competence.competence3()
            elif self.level==4: self.competence.competence4()
            elif self.level==5: self.competence.competence5()


    def ability_score(self,caracteristique):
        #STR=1, DEX=2, CON=3, INT=4, WIS=5, CHA=6
        caract=[self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA]
        return (caract[caracteristique]-10)/2

    def controle(time,stats,valeur):
        print("okay")
    def stats_up(self,stat,facteur,temps):
        #STR=1, DEX=2, CON=3, INT=4, WIS=5, CHA=6
        #facteur c'est le multiplicateur, temps c'est le nombre de tours que la modification prend effet : 0 rend l'effet permanent
        stats=[self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA]
        self.bonus=Bonus(self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA,temps)
        
        stats[stat]=facteur*stats[stat]

    
