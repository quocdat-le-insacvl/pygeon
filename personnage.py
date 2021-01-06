from basic_actions import Actions
from settings.screen import screen,WINDOWS_SIZE
from settings import color
from entity import Entity
from fonctions import *
from items import Sword1,Sword10,Wikitem
from fonction import basic_checkevent,draw_text
from settings.load_img import wizard_icon, neutre_icon,fighter_icon
import pygame
key = list(Wikitem.keys())
buttona,buttons,buttonpa,buttonps=init_buttonsas()
confirm,confirmp=confirm_button()

class Object():
    def __init__(self,name,value=None):
        self.name = name
        self.value = value


class Perso(Entity):
    def __init__(self,STR=8,DEX=8,CON=8,INT=8,WIS=8,CHA=8,hp=5,hp_max=5,inventaire=10,name=None,classe=None,level=0,xp=0,hit_dice=0):
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
        self.chose_skill=False
        self.av_points=15
        self.pos_xp = xp
        self.hit_dice=hit_dice
        self.nb_hit_dice=0
        self.competencesList=[]
        self.master=False
        self.masterAction=0
        ### Actions during the game ###
        self.action=Actions()
        self.actionP=1
        self.bonusAction=1
        ### extern elements ###
        self.difficulty = 10
        self.inventaire = inventaire
        self.armor = dict()
        for i in range(0,6):     # 0 : HEAD 1 : TORSE 2 : COUE  3 BOTTE 4 : MAIN GAUCHE : 5 MAIN DROITE
            self.armor[i] = None
        self.armor_class=self.calcul_armor()
        ### Pictures ###
        self.lvl_up_img=pygame.transform.scale(pygame.image.load(r"Image\lvl_up.png"),(WINDOWS_SIZE[0]//20,WINDOWS_SIZE[1]//20))

    ####### Def lvl ########

    def levelupchange(self):
        #manage the level up of the caracter

        lvl_XP = (400,600,800,1200,1600,2400,3200,4800,6400,9600,12800,19200,25600,38400,51200,76800,102400,153600,204800)
        if self.level==0:
            print("selectionner vos premiers attributs")
            self.level=1
            print("level1")
            self.nb_hit_dice=1
            self.hp_max=8+self.score("con") 
            self.hp=self.hp_max
            return True
        elif self.xp>=lvl_XP[self.level-1] and self.level<5:
            self.level+=1
            self.affichage_lvlup()
            self.av_points+=2+self.ability_score(3)
            ######Global bonus for the level 2######
            if self.level==2: 
                print("level2")
                self.chose_skill=True
                self.choseSkill()
            elif self.level==3: 
                print("level3")
            ######Global bonus for the level 4######
            elif self.level==4: 
                print("level4")
                self.master=True
                self.masterAction=1
            elif self.level==5: 
                print("level5")
                self.proficiency=3
            #fin des competence initialisation des statistiques de base
            self.nb_hit_dice=self.level
            self.hp_max=8+self.score("con")
            self.hp_max+=(self.level-1)*(self.hit_dice//2+self.score("con"))
            self.hp=self.hp_max
            return True


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
        """calcul basique du score en fonction d'une caractéristique passée en paramètre
        STR=0, DEX=1, CON=2, INT=3, WIS=4, CHA=5"""

        return (self.handicap(caracteristique)-10)//2


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
        if self.level==4:
            self.masterAction=1

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
    
    def handicap(self,comp):
        "calcul les différents handicapes, liés au poids de l'armure par exemple"
        if comp==1 and self.armor[1]!=None:
            if self.stats[comp]>8+self.key[self.armor[1]].dex_bonus:
                return 8+self.key[self.armor[1]].dex_bonus
        return self.stats[comp]

    def calcul_armor(self, type_of_calcul=0):
        """ refresh the value of the class armor, must add calcul with """
        assert(type_of_calcul==1 or type_of_calcul==0), "must add a valide type of calcul : 1 without armor"
        if type_of_calcul==0:
            if self.armor[1]!=None:
                return self.score("dex")+10+key[armor[1]].armor_bonus
        return self.score("dex")+10
    
    def damage(self):
        "calcule les dommages en fonction de l'arme équipée"
        bonus_deg=0
        if self.armor[4]!=None:
            bonus_deg=self.action.dice(key[armor[4]].dmg)
            if key[self.armor[4]].wpn_type=="RANGED" or key[self.armor[5]].wpn_type=="RANGED":
                return bonus_deg+self.score("dex")
        elif self.armor[5]!=None and self.armor[4]==None:
            bonus_deg=self.action.dice(key[armor[5]].dmg)
            if key[self.armor[4]].wpn_type=="RANGED" or key[self.armor[5]].wpn_type=="RANGED":
                return bonus_deg+self.score("dex")
        if self.armor[4]!=None and self.armor[5]!=None:
            if all([key[self.armor[4]].wpn_type!="Two Handed",key[self.armor[4]].wpn_type!="RANGED",key[self.armor[5]].wpn_type!="RANGED"]):
                bonus_deg+=self.action.dice(key[armor[5]].dmg)
            elif key[self.armor[4]].wpn_type=="Two Handed":
                bonus_deg+=self.score("str")//2    
        return bonus_deg+self.score("str")
    
    ######## All the following fonctions will be for the caractersheet ############

    def caracter_sheet(self):
        #assert(self.name!=None and self.classe!=None), "perso not initialised"
        screenS=screen.copy()
        running=True
        "Creer un board et y met les attributs qui ne sont pas censer bouger"
        board=pygame.transform.scale(board_init(),(900,780))
        rectboard=pygame.Rect(screen.get_width()//2-board.get_width()//2,20,0,0)
        board.set_colorkey((255,255,255))
        board_icon=pygame.transform.scale(board_init(),(board.get_width()//5,board.get_height()//5))
        # board_icon.set_colorkey((0,0,0))
        if self.classe=='sorcerer':
            icone=pygame.transform.scale(wizard_icon,(board_icon.get_width()//2,board_icon.get_height()))
        if self.classe=='fighter':
            icone=pygame.transform.scale(fighter_icon,(board_icon.get_width(),board_icon.get_height()))
        icone.set_colorkey((255,255,255))
        board_icon.blit(icone,(board_icon.get_width()//2-icone.get_width()//2,0))
        rect_icon=screen.blit(board_icon,(rectboard.x-board_icon.get_width()//1.5,rectboard.y+board_icon.get_height()//0.8))
        board_icon2=pygame.transform.scale(board_init(),(board.get_width()//5,board.get_height()//5))
        iconen=pygame.transform.scale(neutre_icon,(trunc(board_icon2.get_width()//1.2),trunc(board_icon2.get_height()//1.2)))
        board_icon2.blit(iconen,(board_icon2.get_width()//2-iconen.get_width()//2,board_icon2.get_height()//2-iconen.get_height()//2))
        perso=pygame.transform.scale(self.img,(board.get_width()//5,board.get_height()//3))
        board2=board_init()
        board.blit(perso,(10+board.get_width()*0.06,10))
        boards=pygame.transform.scale(board_init(), (board.get_width()-10,int(board.get_height()//1.5)))
        board.blit(boards,(5,10+board.get_height()//3))
        board2=pygame.transform.scale(board_init(), (int(board.get_width()//1.4-5),board.get_height()//3))
        board.blit(board2,(perso.get_width()+board.get_width()*0.06,15))
        draw_text(self.name,title,"b",board,perso.get_width()*2.5,board.get_height()//30-10)
        draw_text("Class : "+ self.classe,subtitle,"b",board,perso.get_width()+board.get_width()*0.06+30,70)
        draw_text("Level : "+str(self.level),subtitle,"b",board,perso.get_width()+board.get_width()*0.06+30,110)
        draw_text("Attack : "+str(self.attack),subtitle,"b",board,perso.get_width()+board.get_width()*0.06+30,150)
        draw_text("Hit Dice : "+str(self.hit_dice),subtitle,"b",board,perso.get_width()+board.get_width()*0.06+30,190)
        draw_text("HP : ",subtitle,"b",board,perso.get_width()+board.get_width()*0.06+400,70)
        draw_text(str(self.hp) + " / "  + str(self.hp_max),subtitle,color.RED,board,perso.get_width()+board.get_width()*0.06+490,70)
        draw_text("AC : " + str(self.armor_class),subtitle,"b",board,perso.get_width()+board.get_width()*0.06+400,110)
        draw_text("Feet : " + str(self.feet),subtitle,"b",board,perso.get_width()+board.get_width()*0.06+400,150)
        draw_text("Nb HD : " + str(self.nb_hit_dice),subtitle,"b",board,perso.get_width()+board.get_width()*0.06+400,190)
        draw_text("SKILL POINTS",title2,"b",board,40,50+board.get_height()//3)
        draw_text("AIVABLE",title,"b",board,500,160+board.get_height()//3)
        draw_text("STR",title,"b",board,40,100+board.get_height()//3)
        draw_text("DEX",title,"b",board,40,160+board.get_height()//3)
        draw_text("CON",title,"b",board,40,220+board.get_height()//3)
        draw_text("INT",title,"b",board,40,280+board.get_height()//3)
        draw_text("WIL",title,"b",board,40,340+board.get_height()//3)
        draw_text("CHA",title,"b",board,40,400+board.get_height()//3)
        av=self.av_points
        click=False
        "initialise la liste de boutons cliquable"
        Blist=self.buttons_init(board,rectboard)
        rect_confirm=self.confirm(board,rectboard,av)
        board1=self.boardSkill(board.copy(),av)
        if self.chose_skill==True:
            self.choseSkill()
        screenS2=screenSave()
        while running:
            "actualise le board avec les skills points et les buttons si un changement a été fait"
            screen.blit(screenS2,(0,0))
            board1=self.boardSkill(board.copy(),av)
            self.confirm(board1,rectboard,av)
            self.buttons_select(board1,av)  
            indice=collides(pygame.mouse.get_pos(),Blist)
            "ici on vérifie si le joueur a fait un click et où"
            if click and indice!=-1:
                self.buttons_select(board1,av,indice)
                if av>0 and indice%2==0 and self.stats[indice//2]+self.stats_eph[indice//2]<18:
                    av-=1
                    self.points_eph[(indice+1)//2]+=1
                    self.stats_eph=[8+self.points_eph[n]+self.points[n]-self.stats[n] if self.stats[n]+self.stats_eph[n]<14 else 14-self.stats[n]+
                      (self.points_eph[n]+self.points[n]-6)//2 if 14<=self.stats[n]+self.stats_eph[n]<16 else 16-self.stats[n]+(self.points_eph[n]+
                      self.points[n]-10)//3 for n in range(6)]
                elif indice%2==1 and self.stats_eph[indice//2]!=0:
                    av+=1
                    self.points_eph[indice//2]-=1
                    self.stats_eph=[8+self.points_eph[n]+self.points[n]-self.stats[n] if self.stats[n]+self.stats_eph[n]<14 else 14-self.stats[n]+
                      (self.points_eph[n]+self.points[n]-6)//2 if 14<=self.stats[n]+self.stats_eph[n]<16 else 16-self.stats[n]+(self.points_eph[n]+
                      self.points[n]-10)//3 for n in range(6)]
            elif click and rect_confirm.collidepoint(pygame.mouse.get_pos()):
                self.confirm(board1,rectboard,av,True)
            elif click and rect_icon.collidepoint(pygame.mouse.get_pos()):
                self.stats_eph=[0,0,0,0,0,0]
                self.points_eph=[0,0,0,0,0,0]
                return 1
            screen.blit(board1,(screen.get_width()//2-board.get_width()//2,20))
            screen.blit(board_icon2,(rectboard.x-board_icon.get_width()//1.5,rectboard.y+board_icon.get_height()*0.2))
            pygame.display.flip()
            running,click=basic_checkevent(click)
        self.stats_eph=[0,0,0,0,0,0]
        self.points_eph=[0,0,0,0,0,0]
        screen.blit(screenS,(0,0))
        return 0
    

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
            if self.stats_eph[n]+self.stats[n]!=18:
                buttonList.append(replace_rect(rectboard,board.blit(buttona,(345,120+60*n+board.get_height()//3))))
            else:
                buttonList.append(replace_rect(rectboard,board.blit(buttonpa,(345,120+60*n+board.get_height()//3))))
            buttonList.append(replace_rect(rectboard,board.blit(buttonps,(230,120+60*n+board.get_height()//3))))
        return buttonList
    
    
    def buttons_select(self,board,av,selected=-1):
        "actualise les boutons en fonction de av (aivable points) et du clique"
        for n in range(6):
            if av==0:
                board.blit(buttonpa,(345,120+60*n+board.get_height()//3))
            elif self.stats_eph[n]+self.stats[n]==18:
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
                self.points=[self.points[n]+self.points_eph[n] for n in range(6)]
                self.stats=[8+self.points[n] if self.stats[n]+self.stats_eph[n]<14 else 14+(self.points[n]-6)//2 if 14<=self.stats[n]+
                            self.stats_eph[n]<16 else 16+(self.points[n]-10)//3 if 16<=self.stats[n]+self.stats_eph[n]<18 else 18 for n in range(6)]
                self.points_eph=[0,0,0,0,0,0]
                self.stats_eph=[0,0,0,0,0,0]
        if chang!=self.av_points:
            rect=replace_rect(rectboard,board.blit(confirm, (600,board.get_height()//2+200)))
        else:
            rect=replace_rect(rectboard,board.blit(confirmp, (600,board.get_height()//2+200)))
        return rect
    
    def moove(self):
        if self.bonusAction>0:
            "à completer"
            self.bonusAction-=1
        else:
            running=True
            while running:
                running=board_error("no more bonus action")

    def passTurn(self):
        self.actionP=0
    
    def choseSkill(self):
        """affiche un tableau qui permet de choisir un skill"""
        screenS=screenSave()
        board=board_with_msg("chose a skill between str dex con int wis cha")
        s=wred(subtitle,"str ")
        d=wred(subtitle,"dex ")
        co=wred(subtitle,"con ")
        i=wred(subtitle,"int ")
        w=wred(subtitle,"wis ")
        ch=wred(subtitle,"cha ")
        board_rect=pygame.Rect(screen.get_width()//8,screen.get_height()//8,0,0)
        list_choice=choices_clickable(board,[s,d,co,i,w,ch],board_rect)
        board_rect=screen.blit(board,(screen.get_width()//8,screen.get_height()//8))
        pygame.display.flip()
        running=True
        click=False
        while running:
            indice=collides(pygame.mouse.get_pos(), list_choice)
            running,click=basic_checkevent(click)
            if click==True:
                if board_rect.collidepoint(pygame.mouse.get_pos())!=True:
                    running=False
                elif indice!=-1:
                    self.skills[indice]=1
                    self.chose_skill=False
                    running=False
        screen.blit(screenS,(0,0))