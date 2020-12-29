import pygame
from entity import Entity
from settings.load_img import pixel_red, ava_perso
from pygame.locals import *
from items import Sword1,Sword10,Wikitem
from inventory import Inventaire
from settings.screen import screen
from fonction import *
from settings.police import *
key = list(Wikitem.keys())
pixel_mask = pygame.mask.from_surface(pixel_red)

path_pygeon = os.path.dirname(__file__)
path_save = os.path.join(path_pygeon, 'Save')
path_addon = os.path.join(path_pygeon, 'Addon')

button_ini1=validation_button
buttonp_ini=validation_button_pressed

buttona,buttons,buttonpa,buttonps=init_buttonsas()
confirm,confirmp=confirm_button()

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


class Perso(Entity):
    def __init__(self,STR=8,DEX=8,CON=8,INT=8,WIS=8,CHA=8,hp=10,hp_max=10,inventaire=10,name=None,classe=None,level=0,xp=0,hit_dice=0,argent=0,player_animation = None):
        super().__init__(100,100,pygame.transform.scale(pygame.image.load(path.join(path_addon,'Image/perso.png')),(96,147)),name,"Player",animation_dict=player_animation)
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
        self.argent = argent
        self.poid_actuel = 0
        self.poid_max = 300
        self.competencesList=[]
        self.bouton_comp = dict()
        # self.skills=[0,0,0,0,0,0,0]
        self.skills = []

        ### Actions during the game ###
        
        self.feats=[]
        ### extern elements ###
        self.difficulty = 10
        self.inventaire = inventaire
        self.armor = dict()
        self.crew_mate = []
        for i in range(0,6):     # 0 : HEAD 1 : TORSE 2 : COUE  3 BOTTE 4 : MAIN GAUCHE : 5 MAIN DROITE
            self.armor[i] = None
        ### Pictures ###
        self.avata = ava_perso
        self.tour = False
        self.resultat = 0
        self.n_de = 6
        
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
        screen.blit(pygame.transform.scale(pygame.image.load(path.join(path_addon,'Image/lvl_up.png')),(WINDOWS_SIZE[0]//20,WINDOWS_SIZE[1]//20)),(self.pos_x+100,self.pos_y))
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
            if click!=True:
                board1=self.boardSkill(board.copy(),av)
                self.confirm(board1,rectboard,av)
                self.buttons_select(board1,av)

            indice=self.collides(pygame.mouse.get_pos(),Blist)
            "ici on vérifie si le joueur a fait un click et où"
            if click and indice!=-1:
                self.buttons_select(board1,av,indice)
                if av>0 and indice%2==0:
                    av-=1
                    self.stats_eph[(indice+1)//2]+=1
                elif indice%2==1 and self.stats_eph[indice//2]!=0:
                    av+=1
                    self.stats_eph[indice//2]-=1
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
        #permet de creer un bouton de confirmation pour l'attribut av_points, puis peut changer cette attribut
        if change:
                self.av_points=chang
                self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA=(self.stats[n]+self.stats_eph[n] for n in range(len(self.stats)))
                self.stats=[self.STR,self.DEX,self.CON,self.INT,self.WIS,self.CHA]
                self.stats_eph=[0,0,0,0,0,0]
        if chang!=self.av_points:
            rect=replace_rect(rectboard,board.blit(confirm, (600,board.get_height()//2+200)))
        else:
            rect=replace_rect(rectboard,board.blit(confirmp, (600,board.get_height()//2+200)))
        return rect

    def collides(self,pos,listrect):
        "vérifie la collision d'un point avec une list passés en paramètre"
        for n in range(len(listrect)):
            if listrect[n].collidepoint(pos):
                return n
        return -1
    
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
    def afficher(self):
        #self.perso_screen.blit(self.perso,(self.pos_x,self.pos_y))
        self.rect_perso = pygame.Rect((self.pos_x,self.pos_y),(self.img.get_width(),self.img.get_height()))
        return self.img

class Perso_game(Perso):
    def __init__(self,STR,DEX,CON,INT,WIS,CHA,hp,hp_max,inventaire,img,pos_x,pos_y,player_animation = None ,argent = 0,name=None,classe=None,level=1,xp=0):
        #Entity.__init__(self,pos_x,pos_y,img,name,"Player",animation_dict=player_animation)
        Perso.__init__(self,STR,DEX,CON,INT,WIS,CHA,hp,hp_max,inventaire,player_animation=player_animation,name=name)
        self.case_connue = []
        self.mask_surface = pygame.Surface((img.get_width()-40,10))
        self.mask_surface.fill((255,0,0))
        self.masks = pygame.mask.from_surface(self.mask_surface)
        self.swap = False
        self.entity_near = False
        self.swap_entity = False
        self.mouvement = [False,False,False,False]
        self.deplacement = [0,0]
        self.n_case = 59
        self.n_mvt = 1
        self.nbre_direct = 0
        self.interact_range = (10,10)

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
    def move_player(self,dict_collision,list_with_collide,list_monster):
        self.refresh_animation_and_mouvement()
        self.swap = False
        self.entity_near = False
        self.swap_entity = False
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
        for x in list_monster:
            if x.collide_box_interact.mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x.collide_box_interact.pos_x,(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x.collide_box_interact.pos_y)):
                return x 
        for x in dict_collision['collision_change_camera']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.swap = True
        for x in dict_collision['collision']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                possible = False
        if possible:
            self.pos_x += self.deplacement[0]
            self.pos_y += self.deplacement[1]
            return None
        """def move_player():
        Permet de déplcer le player_rect de mouvement check si le joeurs ne collide pas avec un chamgement de caméra ou une entité"""
    def check_user(self,event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.mouvement[0] = True
            elif event.key == K_DOWN:
                self.mouvement[1] = True
            elif event.key == K_RIGHT:
                self.mouvement[2] = True
            elif event.key == K_LEFT:
                self.mouvement[3] = True
                
        if event.type == KEYUP:
            if event.key == K_UP:
                self.mouvement[0] = False
            if event.key == K_DOWN:
                self.mouvement[1] = False
            if event.key == K_RIGHT:
                self.mouvement[2] = False
            if event.key == K_LEFT:
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
    def spell_bar(self):
        screen.blit(pygame.transform.scale(img_inventaire,(500,100)),(screen.get_width()//2-250,screen.get_height()-95))
        i = 0
        mx,my = pygame.mouse.get_pos()
        for i in range(5):
            self.bouton_comp[i] = pygame.Rect(85*i+screen.get_width()//2-200, screen.get_height()-80, 75, 75)
            pygame.draw.rect(screen,(0,0,1),self.bouton_comp[i],1)
            if self.bouton_comp[i].collidepoint(mx,my):
                pygame.draw.rect(screen,(255,0,0),self.bouton_comp[i])
        i=0
        for i in range(len(self.competencesList)):
            screen.blit(pygame.transform.scale(self.competencesList[i].img,(75,75)),(85*i+screen.get_width()//2-200,screen.get_height()-80))
        

ava_perso = pygame.transform.scale(pygame.image.load(
    path.join(path_addon, 'Image/perso.png')), (96, 147))

        


