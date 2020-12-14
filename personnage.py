from competences import Competence
from basic_actions import Actions
from feats import Feat
from settings.screen import screen,WINDOWS_SIZE
from settings import police,color
import pygame
class Object():
    def __init__(self,name,value=None):
        self.name = name
        self.value = value


class Perso():
    def __init__(self,STR=8,DEX=8,CON=8,INT=8,WIS=8,CHA=8,hp=10,hp_max=10,inventaire=10,name=None,classe=None,level=0,xp=0,hit_dice=0):
        ### Stats ###
        self.name=name
        self.classe = classe
        self.level = level
        self.hp = hp
        self.hp_max = hp_max
        self.proficiency=2
        self.attack=0
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        self.stats=[self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA]
        self.av_points=27
        self.xp = xp
        self.hit_dice=hit_dice
        self.nb_hit_dice=0
        self.competence=Competence(self.classe)
        self.competencesList=[]
        self.skills=[0,0,0,0,0,0,0]
        ### Actions during the game ###
        self.action=Actions(self.attack)
        self.feats=[]
        self.x=100
        self.y=400
        ### extern elements ###
        self.difficulty = 10
        self.inventaire = inventaire
        self.armor = dict()
        for i in range(0,6):     # 0 : HEAD 1 : TORSE 2 : COUE  3 BOTTE 4 : MAIN GAUCHE : 5 MAIN DROITE
            self.armor[i] = None
        ### Pictures ###
        self.im_pers=pygame.transform.scale(pygame.image.load(r"Image\perso.png"),(96,147))
        self.lvl_up_img=pygame.transform.scale(pygame.image.load(r"Image\lvl_up.png"),(WINDOWS_SIZE[0]//20,WINDOWS_SIZE[1]//20))

    ####### Def lvl ########

    def levelupchange(self):
        #manage the level up of the caracter
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
            self.__affichage_lvlup()
            print("level up")
            print(self.level)
            ######Global bonus for the level 2######
            if self.level==2:
                self.attack+=1
            elif self.level==3: self.competence.competence3()
            ######Global bonus for the level 4######
            elif self.level==4: 
                self.competence.competence4()
                #choice
                self.__choice()
            elif self.level==5: self.competence.competence5()
            #fin des competence initialisation des statistiques de base
            self.nb_hit_dice=self.level
            self.hp_max=8+self.ability_score(3)
            self.hp_max+=(self.level-1)*(self.hit_dice/2+self.ability_score(3))
            self.hp=self.hp_max

    def __affichage_lvlup(self):
        #manage the display of the lvl up (private)
        temp=pygame.Surface(WINDOWS_SIZE)
        temp.blit(screen,(0,0))
        screen.blit(self.lvl_up_img,(self.x+100,self.y))
        time=pygame.time.get_ticks()
        pygame.display.flip()
        while(pygame.time.get_ticks()<time+1000):
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                    pygame.quit()
        screen.blit(temp, (0,0))
        pygame.display.flip()



    ####### End lvl def #######

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

    def score(self,comp):
        #basic version of the skills effect just to provide proficiency
        #this fonction must be call for all the calculs wich need ability modifier
        select={"str" : 1,"dex" : 2, "con" : 3, "int" : 4, "wis" : 5, "cha" : 6}
        assert(comp in select), "wrong argument for score()" 
        if self.skills[select[comp]]:
            return ability_score(self.skills[select[comp]])+self.proficiency
    
    def __choice(self):
        screen_S=self.__screenSave()
        text=police.Outrun_future.render("Level up !",True,color.RED)
        text2=police.Outrun_future.render("Choose skill or points",True,color.RED)
        board=pygame.transform.scale(pygame.image.load(r"Addon\Menu\UI board Small  parchment.png"),(text2.get_width()+50,text.get_height()*4))
        excl=pygame.transform.scale(pygame.image.load(r"Addon\Menu\Exclamation_Red.png"),(board.get_width()//5,board.get_height()//5))
        board.blit(text,(board.get_width()//2-text.get_width()//2,10))
        board.blit(text2,(board.get_width()//2-text2.get_width()//2,text.get_height()+20))
        excl_rect=board.blit(excl,(board.get_width()//2-excl.get_width()*2,text.get_height()*2+30))
        screen.blit(board,(WINDOWS_SIZE[0]//2-board.get_width()//2,WINDOWS_SIZE[1]//2-board.get_height()//2))
        pygame.display.flip()
        running=True
        while running:
            for events in pygame.event.get():
                if all([events.type==pygame.MOUSEBUTTONUP,excl_rect.collidepoint((pygame.mouse.get_pos()[0]-WINDOWS_SIZE[0]//2+board.get_width()//2,pygame.mouse.get_pos()[1]-WINDOWS_SIZE[1]//2+board.get_height()//2))]):
                    screen.blit(screen_S,(0,0))
                    pygame.display.flip()
                    running=False
                elif events.type==pygame.QUIT:
                    pygame.quit()
                    running=False


    def __screenSave(self):
        screensave=pygame.Surface(WINDOWS_SIZE)
        screensave.blit(screen,(0,0))
        return screensave
