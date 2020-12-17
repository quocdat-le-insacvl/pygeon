from competences import Competence
from basic_actions import Actions
from settings.screen import screen,WINDOWS_SIZE
from fonctions import subtitle,subtitle,text
from settings import color
from entity import Entity
from fonctions import *
import pygame

button_ini1=pygame.image.load(r"Addon\Menu\TextBTN_Medium.png")
buttonp_ini=pygame.image.load(r"Addon\Menu\TextBTN_Medium_Pressed.png")

class Object():
    def __init__(self,name,value=None):
        self.name = name
        self.value = value


class Perso(Entity):
    def __init__(self,STR=8,DEX=8,CON=8,INT=8,WIS=8,CHA=8,hp=10,hp_max=10,inventaire=10,name=None,classe=None,level=0,xp=0,hit_dice=0):
        super().__init__(100,100,pygame.transform.scale(pygame.image.load(r"Image\perso.png"),(96,147)),name,"perso")
        ### Stats ###
        self.classe = classe
        self.level = level
        self.xp=0
        self.hp = hp
        self.hp_max = hp_max
        self.proficiency=2
        self.attack=0
        self.feet=30
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        self.stats=[self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA]
        self.armor_class=self.calcul_armor()
        self.stats_eph=[0,0,0,0,0,0]
        self.av_points=27
        self.pos_xp = xp
        self.hit_dice=hit_dice
        self.nb_hit_dice=0
        self.competence=Competence(self.classe)
        self.competencesList=[]
        self.skills=[0,0,0,0,0,0,0]
        ### Actions during the game ###
        self.action=Actions(self.attack)
        self.feats=[]
        ### extern elements ###
        self.difficulty = 10
        self.inventaire = inventaire
        self.armor = dict()
        for i in range(0,6):     # 0 : HEAD 1 : TORSE 2 : COUE  3 BOTTE 4 : MAIN GAUCHE : 5 MAIN DROITE
            self.armor[i] = None
        ### Pictures ###
        self.lvl_up_img=pygame.transform.scale(pygame.image.load(r"Image\lvl_up.png"),(WINDOWS_SIZE[0]//20,WINDOWS_SIZE[1]//20))

    ####### Def lvl ########

    def levelupchange(self):
        #manage the level up of the caracter
        #lvl max=5, change position of float("inf") to change the max lvl

        lvl_XP = (400,600,800,1200,float("inf"),1600,2400,3200,4800,6400,9600,12800,19200,25600,38400,51200,76800,102400,153600,204800)
        if self.level==0:
            print("selectionner vos premiers attributs")
            self.level=1
            self.competence.competence1()
            self.nb_hit_dice=1
            self.hp_max=8+self.ability_score(2) 
            self.hp=self.hp_max
        elif self.xp>=lvl_XP[self.level-1]:
            self.level+=1
            self.affichage_lvlup()
            self.av_points+=2+self.ability_score(3)
            ######Global bonus for the level 2######
            if self.level==2: self.competence.competence3()
            elif self.level==3: self.competence.competence3()
            ######Global bonus for the level 4######
            elif self.level==4: 
                self.competence.competence4()
                #choice
            elif self.level==5: self.competence.competence5()
            #fin des competence initialisation des statistiques de base
            self.nb_hit_dice=self.level
            self.hp_max=8+self.ability_score(2)
            self.hp_max+=(self.level-1)*(self.hit_dice/2+self.ability_score(2))
            self.hp=self.hp_max

    def affichage_lvlup(self):
        #manage the display of the lvl up (private)
        temp=pygame.Surface(WINDOWS_SIZE)
        temp.blit(screen,(0,0))
        screen.blit(self.lvl_up_img,(self.pos_x+100,self.pos_y))
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
        #STR=0, DEX=1, CON=2, INT=3, WIS=4, CHA=5

        return (self.stats[caracteristique]-10)//2


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
        bar_position=(self.pos_x,self.pos_y,(hp_pourcent/2 if hp_pourcent>0 else 0),10)
        barmax_color=(255,60,51)
        hp_max_pourcent=self.hp_max/self.hp_max*100
        barmax_position=(self.pos_x,self.pos_y,hp_max_pourcent/2,10)
        pygame.draw.rect(surface, barmax_color, barmax_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def score(self,comp):
        #basic version of the skills effect just to provide proficiency
        #this fonction must be call for all the calculs wich need ability modifier
        select={"str" : 0,"dex" : 1, "con" : 2, "int" : 3, "wis" : 4, "cha" : 5}
        assert(comp in select), "wrong argument for score()" 
        if self.skills[select[comp]]:
            return ability_score(self.skills[select[comp]])+self.proficiency

    def calcul_armor(self, type_of_calcul=0):
        # refresh the value of the class armor, must add calcul with 
        assert(type_of_calcul==1 or type_of_calcul==0), "must add a valide type of calcul : 1 without armor"
        return self.ability_score(1)+10
        if(type_of_calcul==1):
            return self.ability_score(1)+10
    
    ######## All the following fonctions will be for the caractersheet ############

    def caracter_sheet(self):
        assert(self.name!=None and self.classe!=None), "perso not initialised"
        screenS=screenSave()
        running=True
        board=board_init()
        perso=pygame.transform.scale(self.img,(board.get_width()//5,board.get_height()//3))
        board2=pygame.transform.scale(board, (int(board.get_width()//1.25-5),board.get_height()//3))
        board.blit(perso,(10,10))
        t=wbrown(title,self.name)
        board2.blit(t,(board2.get_width()//2-t.get_width()//2,0))
        s=wbrown(subtitle,"Class : " + self.classe)
        board2.blit(s,(40,t.get_height()))
        s=wbrown(subtitle,"HP : ")
        board2.blit(s,(board2.get_width()//2,t.get_height()))
        s2=wred(subtitle,str(self.hp) + " / "  + str(self.hp_max))
        board2.blit(s2,(board2.get_width()//2+s.get_width(),t.get_height()))
        s=wbrown(subtitle,"Lvl : " + str(self.level))
        board2.blit(s,(40,t.get_height()*(1.5)-10))
        s=wbrown(subtitle,"AC : " + str(self.armor_class))
        board2.blit(s,(board2.get_width()//2,t.get_height()*(1.5)-10))
        s=wbrown(subtitle,"Atck : " + str(self.attack))
        board2.blit(s,(40,t.get_height()*(2)-20))
        s=wbrown(subtitle,"Feet : " + str(self.feet))
        board2.blit(s,(board2.get_width()//2,t.get_height()*(2)-20))
        s=wbrown(subtitle,"Hit Dice Type : " + str(self.hit_dice))
        board2.blit(s,(40,t.get_height()*(2.5)-30))
        s=wbrown(subtitle,"Number Hit Dice : " + str(self.nb_hit_dice))
        board2.blit(s,(board2.get_width()//2,t.get_height()*(2.5)-30))
        board.blit(board2,(perso.get_width(),15))
        boardn=board.copy()
        av=self.av_points
        board=self.boardSkill(board,av)
        board=pygame.transform.scale(board, (screen.get_height()-40, screen.get_height()-40))
        screen.blit(board,(screen.get_width()//2-board.get_width()//2,20))
        rectcf=self.confirm(board)
        buttonList=self.buttons_select(av)
        pygame.display.flip()
        while running:
            pygame.display.flip()
            achang=False
            av1=av
            indice=-1
            indice=self.collides(pygame.mouse.get_pos(),buttonList)
            for event in pygame.event.get():
                running=exit_checkevent(event)
                if all([event.type==pygame.MOUSEBUTTONDOWN, indice%2==0]) or all([event.type==pygame.MOUSEBUTTONDOWN,indice!=-1,av!=self.av_points,indice%2==1]):
                    board=boardn.copy()
                    screen.blit(screenS,(0,0))
                    board=self.boardSkill(board,av)
                    board=pygame.transform.scale(board, (screen.get_height()-40, screen.get_height()-40))
                    screen.blit(board,(screen.get_width()//2-board.get_width()//2,20))
                    rectcf=self.confirm(board)
                    self.buttons_select(av,indice)
                    pygame.display.flip()
                    running1=True
                    while running1:
                        indice= self.collides(pygame.mouse.get_pos(),buttonList)
                        for event2 in pygame.event.get():
                            if all([event2.type!=pygame.MOUSEBUTTONUP,indice!=-1])!=True:
                                if all([indice!=-1, av!=0]) or all([indice!=-1,av!=self.av_points,indice%2==1]):
                                    if indice%2==0:
                                        self.stats_eph[indice//2]+=1
                                        av-=1
                                    elif indice%2==1:
                                        if self.stats_eph[indice//2]>=1:
                                            self.stats_eph[indice//2]-=1
                                            av+=1
                            running1=False
                            self.buttons_select(av)
                                

                                    
                if all([event.type==pygame.MOUSEBUTTONDOWN, self.collide(pygame.mouse.get_pos(),rectcf), av!=self.av_points]):
                    self.confirm(board)
                    running2=True
                    while running2:
                        pygame.display.flip()
                        for event2 in pygame.event.get():
                            if all([event2.type!=pygame.MOUSEBUTTONUP, self.collide(pygame.mouse.get_pos(),rectcf), av!=self.av_points])!=True:
                                if self.collide(pygame.mouse.get_pos(),rectcf):
                                    achang=self.confirm(board,av,change=True)
                                    self.buttons_select(av)
                                else:
                                    self.confirm(board,av)
                            running2=False
            if running==False:
                self.stats_eph=[0,0,0,0,0,0]
                screen.blit(screenS,(0,0))
                pygame.display.flip()
            elif av1!=av or achang:
                board=boardn.copy()
                screen.blit(screenS,(0,0))
                board=self.boardSkill(board,av)
                board=pygame.transform.scale(board, (screen.get_height()-40, screen.get_height()-40))
                screen.blit(board,(screen.get_width()//2-board.get_width()//2,20))
                rectcf=self.confirm(board,av)
                buttonList=self.buttons_select(av)

    

    def boardSkill(self,board1,av):
        board=board_init()
        board.set_colorkey(color.BLACK)
        t=wbrown(title2,"SKILL POINTS")
        board.blit(t,(40,40))
        n=wbrown(title, "AIVABLE")
        board2=pygame.transform.scale(board_init(), (n.get_width()+20, n.get_height()+100))
        board.blit(board2,(140+t.get_width(),board.get_height()//2-100))
        a=wbrown(title,str(av))
        board.blit(n, (150+t.get_width(),board.get_height()//2-90))
        board.blit(a, (223+t.get_width(),board.get_height()//2-30))
        s=wbrown(title, "STR")
        board.blit(s,(50,s.get_height()+20))
        s2=wbrown(title, ":        "+str(self.stats[0]+self.stats_eph[0]))
        board.blit(s2,(s.get_width()+80,s.get_height()+20))
        s3=wbrown(title, "DEX")
        board.blit(s3,(50,s.get_height()*2+20))
        s2=wbrown(title, ":        "+str(self.stats[1]+self.stats_eph[1]))
        board.blit(s2,(s.get_width()+80,s.get_height()*2+20))
        s3=wbrown(title, "CON")
        board.blit(s3,(50,s.get_height()*3+20))
        s2=wbrown(title, ":        "+str(self.stats[2]+self.stats_eph[2]))
        board.blit(s2,(s.get_width()+80,s.get_height()*3+20))
        s3=wbrown(title, "INT")
        board.blit(s3,(50,s.get_height()*4+20))
        s2=wbrown(title, ":        "+str(self.stats[3]+self.stats_eph[3]))
        board.blit(s2,(s.get_width()+80,s.get_height()*4+20))
        s3=wbrown(title, "WIS")
        board.blit(s3,(50,s.get_height()*5+20))
        s2=wbrown(title, ":        "+str(self.stats[4]+self.stats_eph[4]))
        board.blit(s2,(s.get_width()+80,s.get_height()*5+20))
        s3=wbrown(title, "CHA")
        board.blit(s3,(50,s.get_height()*6+20))
        s2=wbrown(title, ":        "+str(self.stats[5]+self.stats_eph[5]))
        board.blit(s2,(s.get_width()+80,s.get_height()*6+20))
        board=pygame.transform.scale(board, (board1.get_width()-10,int(board.get_height()//1.5)))
        board1.blit(board,(5,10+board1.get_height()//3))
        return board1

    def buttons_select(self,av,selected=-1):
        buttonList=[]
        buttonpa=buttonp_ini.copy()
        add=wbrown(astxt,"+")
        buttonpa=pygame.transform.scale(buttonpa, (70, add.get_height()))
        buttonps=pygame.transform.scale(buttonpa, (70, add.get_height()))
        buttonpa.blit(add,(buttonpa.get_width()//2-add.get_width()//2,buttonpa.get_height()//2-add.get_height()/2))
        sub=wbrown(astxt,"-")
        buttonps.blit(sub,(buttonps.get_width()//2-sub.get_width()//2,buttonps.get_height()//2-sub.get_height()/2))
        buttonAdd=button_ini1.copy()
        buttonAdd=pygame.transform.scale(buttonAdd, (70, add.get_height()))
        buttonSub=pygame.transform.scale(buttonAdd, (70, add.get_height()))
        buttonAdd.blit(add,(buttonAdd.get_width()//2-add.get_width()//2,buttonAdd.get_height()//2-add.get_height()/2))
        buttonSub.blit(sub,(buttonSub.get_width()//2-sub.get_width()//2,buttonSub.get_height()//2-sub.get_height()/2))
        for n in range(6):
            if av==0:
                buttonList.append(screen.blit(buttonpa,(WINDOWS_SIZE[0]//2-WINDOWS_SIZE[0]//10,WINDOWS_SIZE[1]//16.5*(n+1)+20+screen.get_height()//2.6)))
            else:
                if n*2==selected:
                    buttonList.append(screen.blit(buttonpa,(WINDOWS_SIZE[0]//2-WINDOWS_SIZE[0]//10,WINDOWS_SIZE[1]//16.5*(n+1)+20+screen.get_height()//2.6)))
                else:
                    buttonList.append(screen.blit(buttonAdd,(WINDOWS_SIZE[0]//2-WINDOWS_SIZE[0]//10,WINDOWS_SIZE[1]//16.5*(n+1)+20+screen.get_height()//2.6)))
            if((n+1)*2-1)==selected:
                buttonList.append(screen.blit(buttonps,(WINDOWS_SIZE[0]//2-WINDOWS_SIZE[0]//5.5,WINDOWS_SIZE[1]//16.5*(n+1)+20+screen.get_height()//2.6)))
            elif self.stats_eph[n]>0 and av!=self.av_points:
                buttonList.append(screen.blit(buttonSub,(WINDOWS_SIZE[0]//2-WINDOWS_SIZE[0]//5.5,WINDOWS_SIZE[1]//16.5*(n+1)+20+screen.get_height()//2.6)))
            elif self.stats_eph[n]==0 or av==self.av_points:
                buttonList.append(screen.blit(buttonps,(WINDOWS_SIZE[0]//2-WINDOWS_SIZE[0]//5.5,WINDOWS_SIZE[1]//16.5*(n+1)+20+screen.get_height()//2.6)))
        return buttonList
    
    def confirm(self,board, chang=0, change=False):
        #permet de creer un bouton de confirmation pour l'attribut av_points, puis peut changer cette attribut
        button=button_ini1.copy()
        buttonp=buttonp_ini.copy()
        t=wbrown(title,"CONFIRM")
        button=pygame.transform.scale(button, (t.get_width()+20, t.get_height()))
        buttonp=pygame.transform.scale(buttonp, (t.get_width()+20, t.get_height()))
        button.blit(t, (button.get_width()//2-t.get_width()//2, button.get_height()//2-t.get_height()//2))
        buttonp.blit(t, (button.get_width()//2-t.get_width()//2, button.get_height()//2-t.get_height()//2))
        i=0
        if change:
                self.av_points=chang
                self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA=(self.stats[n]+self.stats_eph[n] for n in range(len(self.stats)))
                self.stats=[self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA]
                self.stats_eph=[0 for n in range(len(self.stats_eph))]
        if chang!=self.av_points:
            rect=screen.blit(button, (screen.get_width()//2+board.get_width()//2.8-t.get_width(),int(board.get_height()*0.8)))
        else:
            rect=screen.blit(buttonp, (screen.get_width()//2+board.get_width()//2.8-t.get_width(),int(board.get_height()*0.8)))
        return rect


    def repair_coord(self,pos,rect):
        x,y=pos
        x=x-rect.x
        y=y-rect.y      
        return x,y
    
    def coord(self,pos,surface):
        x=pos[0]*surface.get_width()/screen.get_width()
        y=pos[1]*surface.get_height()/screen.get_height()  
        return x,y

    def collides(self,pos,listrect):
        for n in range(len(listrect)):
            if listrect[n]:
                if listrect[n].collidepoint(pos):
                    return n
        return -1
    
    def collide(self,pos,rect):
        if rect.collidepoint(pos):
            return True
        return False
