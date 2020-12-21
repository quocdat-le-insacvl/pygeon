from basic_actions import Actions
from settings.screen import screen,WINDOWS_SIZE
from settings import color
from entity import Entity
from fonctions import *
from fonction import basic_checkevent,draw_text
import pygame

buttona,buttons,buttonpa,buttonps=init_buttonsas()
confirm,confirmp=confirm_button()

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
        self.stats_eph=[0,0,0,0,0,0]
        self.points=[0,0,0,0,0,0]
        self.points_eph=[0,0,0,0,0,0]
        self.skills=[0,0,0,0,0,0]
        self.armor_class=self.calcul_armor()
        self.av_points=25
        self.pos_xp = xp
        self.hit_dice=hit_dice
        self.nb_hit_dice=0
        self.competencesList=[]
        ### Actions during the game ###
        self.action=Actions(self.attack)
        self.next_hd_attack=self.action.dice(20)
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
            print("level1")
            self.nb_hit_dice=1
            self.hp_max=8+self.score("con") 
            self.hp=self.hp_max
        elif self.xp>=lvl_XP[self.level-1]:
            self.level+=1
            self.affichage_lvlup()
            self.av_points+=2+self.ability_score(3)
            ######Global bonus for the level 2######
            if self.level==2: print("level2")
            elif self.level==3: print("level3")
            ######Global bonus for the level 4######
            elif self.level==4: 
                print("level4")
                #choice
            #fin des competence initialisation des statistiques de base
            self.nb_hit_dice=self.level
            self.hp_max=8+self.score("con")
            self.hp_max+=(self.level-1)*(self.hit_dice//2+self.score("con"))
            self.hp=self.hp_max

    def point_cost(self,i=0):
        "actualise les stats en fonction des points dans ces dernières, si i=0 actualise les stats constantes, si i=1 les ephemeres"
        if i==0:
            self.stats=[8+self.points[n] if self.stats[n]<14 else 14+(self.points[n]-6)//2 if 14<=self.stats[n]<16 else 16+(self.points[n]-10)//3 if 16<=self.stats[n]<18 else 18 for n in range(6)]
        if i==1:
            self.stats_eph[(8+self.points_eph[n]-self.stats[n] if self.stats[n]<14 else 14-self.stats[n]+(self.points[n]-6)//2 if 14<=self.stats[n]<16 else 16-self.stats[n]+(self.points[n]-10)//3 if 16<=self.stats[n]<18 else 0 for n in range(6))]

    def affichage_lvlup(self):
        #manage the display of the lvl up (private)
        temp=pygame.Surface(WINDOWS_SIZE)
        temp.blit(screen,(0,0))
        screen.blit(self.lvl_up_img,(self.pos_x+100,self.pos_y))
        time=pygame.time.get_ticks()
        pygame.display.flip()
        running=True
        while(pygame.time.get_ticks()<time+1000 and running):
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==K_ESCAPE:
                        running=False
                        pygame.quit()
                elif event.type==pygame.MOUSEBUTTONDOWN or event.type==pygame.KEYDOWN:
                    running=False
                if event.type==pygame.QUIT:
                    running=False
                    pygame.quit()
        screen.blit(temp, (0,0))
        pygame.display.flip()



    ####### End lvl def #######

    def ability_score(self,caracteristique):
        """calcul basic du score en fonction d'une caractéristique passée en paramètre
        STR=0, DEX=1, CON=2, INT=3, WIS=4, CHA=5"""

        return (self.stats[caracteristique]-10)//2


    # def stats_up(self,stat,facteur,temps):
    #     #STR=1, DEX=2, CON=3, INT=4, WIS=5, CHA=6
    #     #facteur c'est le multiplicateur, temps c'est le nombre de tours que la modification prend effet : 0 rend l'effet permanent
    #     stats=[self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA]
    #     self.bonus=Bonus(self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA,temps)
        
    #     stats[stat]=facteur*stats[stat]

    
    def rest(self):
        """vie que récupère le joueur après s'être reposé
        coder un lit pour que le joueur puisse se reposer, faut faire le temps encore"""
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
        """basic version of the skills effect just to provide proficiency
        this fonction must be call for all the calculs wich need ability modifier"""
        select={"str" : 0,"dex" : 1, "con" : 2, "int" : 3, "wis" : 4, "cha" : 5}
        assert(comp in select), "wrong argument for score()" 
        if self.skills[select[comp]]:
            return self.ability_score(select[comp])+self.proficiency
        else :
            return self.ability_score(select[comp])

    def calcul_armor(self, type_of_calcul=0):
        """ refresh the value of the class armor, must add calcul with """
        assert(type_of_calcul==1 or type_of_calcul==0), "must add a valide type of calcul : 1 without armor"
        return self.score("dex")+10
        if(type_of_calcul==1):
            return self.score("dex")+10
    
    ######## All the following fonctions will be for the caractersheet ############

    def caracter_sheet(self):
        assert(self.name!=None and self.classe!=None), "perso not initialised"
        screenS=screen.copy()
        running=True
        "Creer un board et y met les attributs qui ne sont pas censer bouger"
        board=pygame.transform.scale(board_init(),(900,780))
        board.set_colorkey((255,255,255))
        perso=pygame.transform.scale(self.img,(board.get_width()//5,board.get_height()//3))
        board2=board_init()
        board.blit(perso,(10,10))
        boards=pygame.transform.scale(board_init(), (board.get_width()-10,int(board.get_height()//1.5)))
        board.blit(boards,(5,10+board.get_height()//3))
        board2=pygame.transform.scale(board_init(), (int(board.get_width()//1.25-5),board.get_height()//3))
        board.blit(board2,(perso.get_width(),15))
        draw_text(self.name,title,"b",board,perso.get_width()*2.5,board.get_height()//30-10)
        draw_text("Class : "+ self.classe,subtitle,"b",board,perso.get_width()+30,70)
        draw_text("Level : "+str(self.level),subtitle,"b",board,perso.get_width()+30,110)
        draw_text("Attack : "+str(self.attack),subtitle,"b",board,perso.get_width()+30,150)
        draw_text("Hit Dice : "+str(self.hit_dice),subtitle,"b",board,perso.get_width()+30,190)
        draw_text("HP : ",subtitle,"b",board,perso.get_width()+400,70)
        draw_text(str(self.hp) + " / "  + str(self.hp_max),subtitle,color.RED,board,perso.get_width()+490,70)
        draw_text("AC : " + str(self.armor_class),subtitle,"b",board,perso.get_width()+400,110)
        draw_text("Feet : " + str(self.feet),subtitle,"b",board,perso.get_width()+400,150)
        draw_text("Nb HD : " + str(self.nb_hit_dice),subtitle,"b",board,perso.get_width()+400,190)
        draw_text("SKILL POINTS",title2,"b",board,40,50+board.get_height()//3)
        draw_text("AIVABLE",title,"b",board,500,160+board.get_height()//3)
        draw_text("STR",title,"b",board,40,100+board.get_height()//3)
        draw_text("DEX",title,"b",board,40,160+board.get_height()//3)
        draw_text("CON",title,"b",board,40,220+board.get_height()//3)
        draw_text("INT",title,"b",board,40,280+board.get_height()//3)
        draw_text("WIL",title,"b",board,40,340+board.get_height()//3)
        draw_text("CHA",title,"b",board,40,400+board.get_height()//3)
        av=self.av_points
        rectboard=pygame.Rect(screen.get_width()//2-board.get_width()//2,20,0,0)
        click=False
        "initialise la liste de boutons cliquable"
        Blist=self.buttons_init(board,rectboard)
        rect_confirm=self.confirm(board,rectboard,av)
        board1=self.boardSkill(board.copy(),av)
        while running:
            "actualise le board avec les skills points et les buttons si un changement a été fait"
            board1=self.boardSkill(board.copy(),av)
            self.confirm(board1,rectboard,av)
            self.buttons_select(board1,av)  
            
            indice=collides(pygame.mouse.get_pos(),Blist)
            "ici on vérifie si le joueur a fait un click et où"
            if click and indice!=-1:
                self.buttons_select(board1,av,indice)
                if av>0 and indice%2==0:
                    av-=1
                    self.points_eph[(indice+1)//2]+=1
                    self.point_cost(1)
                elif indice%2==1 and self.stats_eph[indice//2]!=0:
                    av+=1
                    self.points_eph[indice//2]-=1
                    self.point_cost(1)
            elif click and rect_confirm.collidepoint(pygame.mouse.get_pos()):
                self.confirm(board1,rectboard,av,True)
            screen.blit(board1,(screen.get_width()//2-board.get_width()//2,20))
            pygame.display.flip()
            running,click=basic_checkevent(click)
        screen.blit(screenS,(0,0))
    

    def boardSkill(self,board,av):
        "actualise le board avec les skills"
        draw_text(str(av),title,"b",board,570,220+board.get_height()//3)
        draw_text(":        "+str(self.stats[0]+self.stats_eph[0]),title,"b",board,150,100+board.get_height()//3)
        draw_text(":        "+str(self.stats[1]+self.stats_eph[1]),title,"b",board,150,160+board.get_height()//3)
        draw_text(":        "+str(self.stats[2]+self.stats_eph[2]),title,"b",board,150,220+board.get_height()//3)
        draw_text(":        "+str(self.stats[3]+self.stats_eph[3]),title,"b",board,150,280+board.get_height()//3)
        draw_text(":        "+str(self.stats[4]+self.stats_eph[4]),title,"b",board,150,340+board.get_height()//3)
        draw_text(":        "+str(self.stats[5]+self.stats_eph[5]),title,"b",board,150,400+board.get_height()//3)
        return board

    def buttons_init(self,board,rectboard):
        "initialise les boutons + et -"
        buttonList=[]
        for n in range(6):
            buttonList.append(replace_rect(rectboard,board.blit(buttona,(345,120+60*n+board.get_height()//3))))
            buttonList.append(replace_rect(rectboard,board.blit(buttonps,(230,120+60*n+board.get_height()//3))))
        return buttonList
    
    
    def buttons_select(self,board,av,selected=-1):
        "actualise les boutons en fonction de av (aivable points) et du clique"
        for n in range(6):
            if av==0:
                board.blit(buttonpa,(345,120+60*n+board.get_height()//3))
            else:
                if n*2==selected:
                    board.blit(buttonpa,(345,120+60*n+board.get_height()//3))
                else:
                    board.blit(buttona,(345,120+60*n+board.get_height()//3))
            if((n+1)*2-1)==selected:
                board.blit(buttonps,(230,120+60*n+board.get_height()//3))
            elif self.stats_eph[n]>0:
                board.blit(buttons,(230,120+60*n+board.get_height()//3))
            elif self.stats_eph[n]==0:
                board.blit(buttonps,(230,120+60*n+board.get_height()//3))
    
    def confirm(self,board,rectboard, chang=0, change=False):
        """permet de creer un bouton de confirmation pour l'attribut av_points, puis peut changer cette attribut"""
        if change:
                self.av_points=chang
                self.points=self.points+self.points_eph
                self.point_cost()
                #self.stats=[self.stats[n]+self.stats_eph[n] for n in range(len(self.stats))]
                self.points_eph=[0,0,0,0,0,0]
                self.stats_eph=[0,0,0,0,0,0]
        if chang!=self.av_points:
            rect=replace_rect(rectboard,board.blit(confirm, (600,board.get_height()//2+200)))
        else:
            rect=replace_rect(rectboard,board.blit(confirmp, (600,board.get_height()//2+200)))
        return rect



    


