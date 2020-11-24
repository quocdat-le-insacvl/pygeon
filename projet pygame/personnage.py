
class Object():
    def __init__(self,name,value=None):
        self.name = name
        self.value = value

class Perso():
    def __init__(self,STR,DEX,CON,INT,WIS,CHA,hp,hp_max,inventaire,name=None,classe=None,level=1,xp=0):
        self.name=name
        self.classe = classe
        self.level = level
        self.xp = xp 
        self.hp = hp
        self.hp_max = hp_max
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
        lvl_XP = (400,600,800,1200,1600,2400,3200,4800,6400,9600,12800,19200,25600,38400,51200,76800,102400,153600,204800,307200,409600,614400,819200,1228800,1638400,2457600,3276800,4915200,6553600,9830400)
        while self.xp >= lvl_XP[self.level-1]:
            self.level += 1

    