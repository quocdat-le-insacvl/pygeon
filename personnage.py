
import pygame
from entity import Entity
from settings.load_img import pixel_red, ava_perso
from pygame.locals import *
from items import Sword1,Sword10,Wikitem
from inventory import Inventaire
from settings.screen import screen,LARGEUR as HEIGHT
from fonction import *
from fonctions import *
from settings.police import *
from basic_actions import *
from math import trunc
from fonctions import collides,choices_clickable,board_error
key = list(Wikitem.keys())
pixel_mask = pygame.mask.from_surface(pixel_red)

path_pygeon = os.path.dirname(__file__)
path_save = os.path.join(path_pygeon, 'Save')
path_addon = os.path.join(path_pygeon, 'Addon')

button_ini1=validation_button
buttonp_ini=validation_button_pressed

buttona,buttons,buttonpa,buttonps=init_buttonsas()
confirm,confirmp=confirm_button()

class Object():
    def __init__(self,name,value=None):
        self.name = name
        self.value = value

class Stats():
    def __init__(self,STR=8,DEX=8,CON=8,INT=8,WIS=8,CHA=8,hp=10,hp_max=10):
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        self.hp = hp
        self.hp_max = hp_max
    def update_hp_bar(self,surface,pos_x,pos_y):
        bar_color=(113,255,51)
        hp_pourcent=(self.hp/self.hp_max)*100
        bar_position=(pos_x,pos_y,(hp_pourcent/2 if hp_pourcent>0 else 0),10)
        barmax_color=(255,60,51)
        hp_max_pourcent=self.hp_max/self.hp_max*100
        barmax_position=(pos_x,pos_y,hp_max_pourcent/2,10)
        pygame.draw.rect(surface, barmax_color, barmax_position)
        pygame.draw.rect(surface, bar_color, bar_position)
        #
        s=wblack(ColderWeather,"Level  "+str(self.level))
        s=pygame.transform.scale(s,(s.get_width()//4, s.get_height()//4))
        surface.blit(s,(pos_x,pos_y-20))



class Perso_saveable(): # INTERDICTION DE METTRE DES PYGAMES SURFACE SEULEMENT DES VARIABLES 
    def __init__(self):
        self.classe = ""
        self.level = 1
        self.xp=0
        self.hp = 0
        self.hp_max = 0
        self.proficiency=0
        self.attack=0
        self.feet=0
        self.STR = 0
        self.DEX = 0
        self.CON = 0
        self.INT = 0
        self.WIS = 0
        self.CHA = 0
        self.argent = 0
        self.poid_actuel = 0
        self.poid_max = 0
        self.difficulty = 10
        self.inventaire = 0
        self.pos_x = 0
        self.pos_y = 0
        self.armor = dict()
        for i in range(0,6):     # 0 : HEAD 1 : TORSE 2 : COUE  3 BOTTE 4 : MAIN GAUCHE : 5 MAIN DROITE
            self.armor[i] = None
        self.visible = True 
        
    def load_player(self,perso):
        self.name = perso.name
        self.classe = perso.classe
        self.level = perso.level
        self.xp= perso.xp  
        self.hp = perso.hp
        self.hp_max = perso.hp_max
        self.proficiency= perso.proficiency
        self.attack= perso.attack
        self.feet= perso.feet
        self.STR = perso.STR
        self.DEX = perso.DEX
        self.CON = perso.CON
        self.INT = perso.INT
        self.WIS = perso.WIS
        self.CHA = perso.CHA
        self.inventaire = perso.inventaire
        self.argent = perso.argent
        self.poid_actuel = perso.poid_actuel
        self.poid_max = perso.poid_max
        self.difficulty = perso.difficulty
        self.inventaire = perso.inventaire
        self.armor = perso.armor
        self.pos_x = perso.pos_x
        self.pos_y = perso.pos_y


class Perso(Entity,Stats):
    def __init__(self,STR=12,DEX=8,CON=8,INT=8,WIS=8,CHA=8,hp=10,hp_max=10,inventaire=10,name=None,level=0,xp=0,hit_dice=0,argent=0,player_animation = None,decalage = [0,0],size=(0,0)):
        #Entity().__init__(self,1,1,pygame.transform.scale(pygame.image.load(path.join(path_addon,'Image/perso.png'))),name,"Player",animation_dict=player_animation,decalage = decalage,size=size)
        super().__init__(100,100,pygame.transform.scale(pygame.image.load(path.join(path_addon,'Image/perso.png')),(96,147)),name,"Player",animation_dict=player_animation,decalage = decalage,size=size)
        Stats.__init__(self,STR,DEX,CON,INT,WIS,CHA,hp,hp_max)
        ### Stats ###
        self.level = level
        self.xp=0
        self.skill = []
        self.proficiency=2
        self.attack=0
        self.feet=30
        self.have_mouve = False
        self.stats=[STR,DEX,CON,INT,WIS,CHA]
        #########
        self.stats_eph=[0,0,0,0,0,0]
        self.points=[0,0,0,0,0,0]
        self.points_eph=[0,0,0,0,0,0]
        self.skills=[0,0,0,0,0,0]
        self.chose_skill=False
        self.av_points=15
        self.master=False
        self.masterAction=0

        self.pos_xp = xp
        self.hit_dice=hit_dice
        self.nb_hit_dice=0
        self.argent = argent
        self.poid_actuel = 0
        self.poid_max = 300
        self.competencesList=[]
        self.n_mvt = 1
        self.bouton_comp = dict()
        
        self.visible = True 
        self.chose_skill=False
        ### Actions during the game ###
        self.competencesList=[]
        
        ### Actions during the game ###
        self.action=Actions()
        self.actionP=1
        self.bonusAction=1
        self.crit=False
        ### extern elements ###
        self.difficulty = 10
        self.inventaire = inventaire
        self.crew_mate = []
        self.armor = dict()
        
        for i in range(0,6):     # 0 : HEAD 1 : TORSE 2 : COUE  3 BOTTE 4 : MAIN GAUCHE : 5 MAIN DROITE
            self.armor[i] = None
        self.armor_class=self.calcul_armor()
        ### Pictures ###
        self.avata = ava_perso
        self.is_player = True
        ###Combat###
        self.tour = False
        self.resultat = 0
        self.n_de = 6
        self.is_alive = True

    
    def check_alive(self):
        if self.hp <= 0:
            self.is_alive = False
        


    def load_player(self,perso_saveable):
        self.name = perso_saveable.name
        self.classe = perso_saveable.classe
        self.level = perso_saveable.level
        self.xp= perso_saveable.xp  
        self.hp = perso_saveable.hp
        self.hp_max = perso_saveable.hp_max
        self.proficiency= perso_saveable.proficiency
        self.attack= perso_saveable.attack
        self.feet= perso_saveable.feet
        self.STR = perso_saveable.STR
        self.DEX = perso_saveable.DEX
        self.CON = perso_saveable.CON
        self.INT = perso_saveable.INT
        self.WIS = perso_saveable.WIS
        self.CHA = perso_saveable.CHA
        self.inventaire = perso_saveable.inventaire
        self.argent = perso_saveable.argent
        self.poid_actuel = perso_saveable.poid_actuel
        self.poid_max = perso_saveable.poid_max
        self.difficulty = perso_saveable.difficulty
        self.armor = perso_saveable.armor
        self.pos_x = perso_saveable.pos_x
        self.pos_y = perso_saveable.pos_y
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
            #self.affichage_lvlup()
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

    def update_hp_bar(self,surface,x,y):
        bar_color=(113,255,51)
        hp_pourcent=(self.hp/self.hp_max)*100
        bar_position=(x,y,(hp_pourcent/2 if hp_pourcent>0 else 0),10)
        barmax_color=(255,60,51)
        hp_max_pourcent=self.hp_max/self.hp_max*100
        barmax_position=(x,y,hp_max_pourcent/2,10)
        pygame.draw.rect(surface, barmax_color, barmax_position)
        pygame.draw.rect(surface, bar_color, bar_position)
        s=wblack(ColderWeather,"Level  "+str(self.level))
        s=pygame.transform.scale(s,(s.get_width()//4, s.get_height()//4))
        surface.blit(s,(x,y-20))

    

    
    ######## All the following fonctions will be for the caractersheet ############

    def caracter_sheet(self):
        screenS=screen.copy()
        running=True
        "Creer un board et y met les attributs qui ne sont pas censer bouger"
        board=pygame.transform.scale(board_init(),(900,780))
        rectboard=pygame.Rect(screen.get_width()//2-board.get_width()//2,20,0,0)
        board.set_colorkey((255,255,255))
        board_icon=pygame.transform.scale(board_init(),(board.get_width()//5,board.get_height()//5))
        # board_icon.set_colorkey((0,0,0))
        print(self.classe)
        if self.classe=='sorcerer':
            icone=pygame.transform.scale(wizard_icon,(board_icon.get_width()//2,board_icon.get_height()))
        if self.classe=='fighter':
            icone=pygame.transform.scale(fighter_icon,(board_icon.get_width(),board_icon.get_height()))
        if self.classe=='rogue':
            icone=pygame.transform.scale(rogue_icon,(board_icon.get_width(),board_icon.get_height()))
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
            running,click=basic_checkevent(click, None)
            if click==True:
                if board_rect.collidepoint(pygame.mouse.get_pos())!=True:
                    running=False
                elif indice!=-1:
                    self.skills[indice]=1
                    self.chose_skill=False
                    running=False
        screen.blit(screenS,(0,0))

    """fonctions utiles pour le combat"""

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
            if key[self.armor[4]].wpn_type=="RANGED" or key[self.armor[5]].wpn_type=="RANGED":
                return (bonus_deg+dex)*crit
        elif self.armor[5]!=None and self.armor[4]==None:
            bonus_deg=self.action.dice(key[self.armor[5]].dmg)
            if key[self.armor[4]].wpn_type=="RANGED" or key[self.armor[5]].wpn_type=="RANGED":
                return (bonus_deg+dex)*crit
        if self.armor[4]!=None and self.armor[5]!=None:
            if all([key[self.armor[4]].wpn_type!="Two Handed",key[self.armor[4]].wpn_type!="RANGED",key[self.armor[5]].wpn_type!="RANGED"]):
                bonus_deg+=self.action.dice(key[self.armor[5]].dmg)
            elif key[self.armor[4]].wpn_type=="Two Handed":
                bonus_deg+=(strong//2)*crit  
        return (bonus_deg+strong)*crit
    
    def saving_throw(self,cara,damage,dc):
        """fonction à utiliser pour resister à un sort"""
        select={0 : "dex",1 : "con", 2 : "wis"}
        if self.level//2+self.score(select[cara])>= dc:
            return damage//2
        return damage
    

    
    def createImages(self,name,scale=True,colorkey=(0,0,0),forceScale=False):
        relative_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Donjon/imgs/")
        if name not in os.listdir(relative_path): 
            print("Image %s not in imgs/ directory" %name)
        elif name[-4:] != ".png" and name[-4:] != ".jpg":
            print("Image not a .png or a .jpg")
        else:
            image = pygame.image.load(os.path.join(relative_path,name))
            if image.get_width() >= 128 or image.get_height() >= 128 or forceScale:
                image = pygame.transform.scale(image,(32, 32))
            image.set_colorkey(colorkey)
            return image
    def display_classe(self,surface,x,y):
        name = wblack(ColderWeather,self.classe)
        name = pygame.transform.scale(name,(name.get_width() // 4,name.get_height()//4))
        screen.blit(name,(x,y))
    def display_lvl(self,surface,x,y):
        name = wblack(ColderWeather,str(self.level))
        name = pygame.transform.scale(name,(name.get_width() // 2,name.get_height()//2))
        screen.blit(name,(x,y + name.get_height()))
    def afficher(self):
        #self.perso_screen.blit(self.perso,(self.pos_x,self.pos_y))
        self.rect_perso = pygame.Rect((self.pos_x,self.pos_y),(self.img.get_width(),self.img.get_height()))
        self.rect_persoDonjon = pygame.Rect((self.pos_x,self.pos_y),(32,49))
        return self.img
class Perso_game(Perso):
    def __init__(self,STR,DEX,CON,INT,WIS,CHA,hp,hp_max,inventaire,img,pos_x,pos_y,player_animation = None ,argent = 0,name=None,level=1,xp=0,decalage=[0,0],size=(0,0)):
        Perso.__init__(self,STR,DEX,CON,INT,WIS,CHA,hp,hp_max,inventaire,player_animation=player_animation,name=name,decalage=decalage,size=size)
        self.case_connue = []
        self.sprite = test
        self.mask_surface = pygame.Surface((img.get_width()-40,10))
        self.donjon_surface = pygame.Surface((img.get_width() - 80,10))
        self.mask_surface.fill((255,0,0))
        self.masks = pygame.mask.from_surface(self.mask_surface)
        self.donjon_mask = pygame.mask.from_surface(self.donjon_surface)
        self.swap = False
        self.entity_near = False
        self.swap_entity = False
        self.change_level = False   
        self.change_hupper_level = False  
        self.monstre_near = False
        self.collision_donjon = False
        self.mouvement = [False,False,False,False]
        self.deplacement = [0,0]
        self.nbre_direct = 0
        self.interact_range = (10,10)
        self.know_map = []

        self.display = pygame.Surface((self.img.get_width(),self.img.get_height()))
        self.display.set_colorkey(BLACK)
    def refresh_animation_and_mouvement(self):
        if self.mouvement[0]:
            self.deplacement = [10,-5]
            self.type_animation = "walk_top"
        elif self.mouvement[1]:
            self.deplacement = [-10,+5]
            self.type_animation = "walk_bottom"
        elif self.mouvement[2]:
            self.deplacement = [+10,+5]
            self.type_animation = "walk_right"
        elif self.mouvement[3]:
            self.deplacement = [-10,-5]
            self.type_animation = "walk_left"
        else:
            self.deplacement = [0,0]
            self.type_animation = "idle"     
    def move_player(self,dict_collision,list_with_collide,list_monster,list_coffre):
        self.refresh_animation_and_mouvement()
        self.swap = False
        self.entity_near = False
        self.swap_entity = False
        self.change_level = False
        self.change_hupper_level = False  
        self.collision_donjon = False
        self.monstre_near = False
        entity = None
        possible = True
        for x in dict_collision['change_camera_entity']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.swap_entity = True
        '''for x in list_mooving_entity:
            if x.collide_box.mask.overlap(self.masks,(self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1]):
                self.entity_near = True'''
        '''for x in dict_collision['collision_entity']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.entity_near = True'''
        for x in list_with_collide:
            if x.collide_box.mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x.collide_box.pos_x,(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x.collide_box.pos_y)):
                self.entity_near = True
                entity =  x
        for x in list_monster:
            if x.collide_box_interact.mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x.collide_box_interact.pos_x,(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x.collide_box_interact.pos_y)) and self.visible:
                self.monstre_near = True
                return x
        for x in list_coffre:
            if x.collide_box.mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x.collide_box.pos_x,(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x.collide_box.pos_y)):
                self.entity_near = True
                entity = x
        for x in dict_collision['collision_change_camera']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.swap = True
        for x in dict_collision['collision']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                possible = False
        for x in dict_collision['collision_under_level']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.change_level = True     
        for x in dict_collision['collision_hupper_level']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.change_hupper_level = True  
        for x in dict_collision['collision_donjon']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.collision_donjon = True  

        if possible:
            self.pos_x += self.deplacement[0]
            self.pos_y += self.deplacement[1]

            return entity
        """def move_player():
        Permet de déplcer le player_rect de mouvement check si le joeurs ne collide pas avec un chamgement de caméra ou une entité"""
    def check_user(self,event,key):
        if event.type == KEYDOWN:
            if event.key == key["move up"]:
                self.mouvement[0] = True
            elif event.key == key["move down"]:
                self.mouvement[1] = True
            elif event.key == key["move right"]:
                self.mouvement[2] = True
            elif event.key == key["move left"]:
                self.mouvement[3] = True
                
        if event.type == KEYUP:
            if event.key == key["move up"]:
                self.mouvement[0] = False
            if event.key == key["move down"]:
                self.mouvement[1] = False
            if event.key == key["move right"]:
                self.mouvement[2] = False
            if event.key == key["move left"]:
                self.mouvement[3] = False

    
        '''def interact_with_entity(self,entity):
        Effectue les actions en fonctions du type de l'entité la fonction est à compléter elle ne traite pas tout les types entités''' 
    def transform_display_for_combat(self):
        self.display = pygame.Surface((300,300))
        self.display.set_colorkey((0,0,0))
    def transform_display_for_map(self):
        self.display = pygame.Surface((self.img.get_width(),self.img.get_height()))
        self.display.set_colorkey((0,0,0))
    

    def print_equipement(self,pos_x,pos_y,pos_x_inventory_player,pos_y_inventory_player,also_inventory=True,mouse=False):

        
        display = pygame.Surface((250,200))
        display.set_colorkey(BLACK)
        display_argent = pygame.Surface((200,50))
        display_argent.set_colorkey(BLACK)
        display_argent.blit(pygame.transform.scale(img_inventaire,(200,50)),(0,0))
        draw_text("Argent : %i"%self.argent,ColderWeather_small,WHITE,display_argent,10,5)
        x = 125
        y_ = 100
        display.blit(pygame.transform.scale(img_inventaire,(250,200)),(0,0))
        copy_img = pygame.Surface.copy(self.img)
        copy_img.set_alpha(50)
        display.blit(copy_img,(250//2-self.img.get_width()//2,100-self.img.get_height()//2))
        bouton_arm = dict()
        mouse_slot = self.inventaire.nb_x * self.inventaire.nb_y
        mx,my = pygame.mouse.get_pos()
        mx_display = mx - pos_x
        my_display = my - pos_y

        for i in range(0,4):
            bouton_arm[i] = pygame.Rect(x-25, 50*i,50,50)
            pygame.draw.rect(display,(0,0,1),bouton_arm[i],1)   
        for i in range(0,2):
            bouton_arm[4+i] = pygame.Rect(25+i*150,75,50,50)
            pygame.draw.rect(display,(0,0,1),bouton_arm[4+i],1)  
        screen.blit(display,(pos_x,pos_y))
        screen.blit(display_argent,(pos_x,pos_y+200))
        for i in range(0,6):
            if self.armor[i] != None:
                screen.blit(key[self.armor[i]].wpn_img,(bouton_arm[i].x+pos_x,bouton_arm[i].y+pos_y))
        i=0
        if self.inventaire.have_object == False:
            for i in range(6):
                if bouton_arm[i].collidepoint((mx_display,my_display)):
                    self.inventaire.backpack[mouse_slot] = self.armor[i]
                    self.armor[i] = None
                    self.inventaire.last_moove = mouse_slot+i+1
                    self.inventaire.have_object = True
        i=0
        if self.inventaire.backpack[mouse_slot] != None:
            if any(pygame.mouse.get_pressed()):
                self.have_object =True
                #screen.blit(key[self.inventaire.backpack[mouse_slot]].wpn_img,(mx,my))
            elif not(any(pygame.mouse.get_pressed())):
                for i in range(0,6):
                    if bouton_arm[i].collidepoint((mx_display,my_display)) and key[self.inventaire.backpack[mouse_slot]].wpn_type == i:
                        self.inventaire.backpack[self.inventaire.last_moove] = self.armor[i]
                        self.armor[i] = self.inventaire.backpack[mouse_slot]
                        self.inventaire.backpack[mouse_slot] = None
                        self.inventaire.last_moove = mouse_slot
                        self.inventaire.have_object = False
                    if bouton_arm[i].collidepoint((mx_display,my_display)) and self.inventaire.backpack[mouse_slot]!= None and  key[self.inventaire.backpack[mouse_slot]].wpn_type == 9:
                        self.hp += key[self.inventaire.backpack[mouse_slot]].heal
                        self.inventaire.backpack[self.inventaire.last_items_select] = None
                        self.inventaire.backpack[mouse_slot] = None
        else:
            self.inventaire.have_object = False
            self.inventaire.last_moove = -1
        if also_inventory:
            self.inventaire.print_inventory_bis(pos_x_inventory_player,pos_y_inventory_player,main=False,mouse=mouse)
        if self.inventaire.backpack[mouse_slot] != None:
            screen.blit(key[self.inventaire.backpack[mouse_slot]].wpn_img,(mx,my))
            
    def deplacerDroite(self):
        self.pos_x+=2    
    def deplacerGauche(self):
        self.pos_x -=2
    def deplacerHaut(self):
        self.pos_y -=2
    def deplacerBas(self):
        self.pos_y+=2
    def spell_bar(self,click):
        screen.blit(pygame.transform.scale(img_inventaire,(500,100)),(screen.get_width()//2-250,screen.get_height()-95))
        i = 0
        mx,my = pygame.mouse.get_pos()
        for i in range(5):
            self.bouton_comp[i] = pygame.Rect(85*i+screen.get_width()//2-200, screen.get_height()-80, 75, 75)
            pygame.draw.rect(screen,(0,0,1),self.bouton_comp[i],1)
            if i < len(self.skill):
                screen.blit(pygame.transform.scale(self.skill[i].img,(75,75)),(85*i+screen.get_width()//2-200, screen.get_height()-80))
            if self.bouton_comp[i].collidepoint(mx,my) and click:
                if i < len(self.skill):
                    self.skill[i].cast()
        i=0
        for i in range(len(self.competencesList)):
            screen.blit(pygame.transform.scale(self.competencesList[i].img,(75,75)),(85*i+screen.get_width()//2-200,screen.get_height()-80))
        
img_perso = pygame.transform.scale(pygame.image.load(
    path.join(path_addon, 'Image/perso.png')), (96, 147))

perso_stealth = pygame.transform.scale(pygame.image.load(
    path.join(path_addon, 'Image/real_stealth.png')), (96, 147))


