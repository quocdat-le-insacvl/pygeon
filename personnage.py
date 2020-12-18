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
        self.skills=[0,0,0,0,0,0,0]
        ### Actions during the game ###
        
        self.feats=[]
        ### extern elements ###
        self.difficulty = 10
        self.inventaire = inventaire
        self.armor = dict()
        for i in range(0,6):     # 0 : HEAD 1 : TORSE 2 : COUE  3 BOTTE 4 : MAIN GAUCHE : 5 MAIN DROITE
            self.armor[i] = None
        ### Pictures ###
        self.lvl_up_img=pygame.transform.scale(pygame.image.load(path.join(path_addon,'Image/lvl_up.png')),(WINDOWS_SIZE[0]//20,WINDOWS_SIZE[1]//20))
        self.avata = ava_perso
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

class Perso_game(Perso):
    def __init__(self,STR,DEX,CON,INT,WIS,CHA,hp,hp_max,inventaire,img,pos_x,pos_y,player_animation = None ,argent = 0,name=None,classe=None,level=1,xp=0):
        #Entity.__init__(self,pos_x,pos_y,img,name,"Player",animation_dict=player_animation)
        Perso.__init__(self,STR,DEX,CON,INT,WIS,CHA,hp,hp_max,inventaire,player_animation=player_animation)
        self.case_connue = []
        self.mask_surface = pygame.Surface((img.get_width()-40,10))
        self.mask_surface.fill((255,0,0))
        self.masks = pygame.mask.from_surface(self.mask_surface)
        self.swap = False
        self.entity_near = False
        self.swap_entity = False
        self.mouvement = [False,False,False,False]
        self.deplacement = [0,0]
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
    def move_player(self,dict_collision):
        self.refresh_animation_and_mouvement()
        self.swap = False
        self.entity_near = False
        self.swap_entity = False
        possible = True
        for x in dict_collision['change_camera_entity']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.swap_entity = True
        for x in dict_collision['collision_entity']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.entity_near = True
        for x in dict_collision['collision_change_camera']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                self.swap = True
        for x in dict_collision['collision']:
            if pixel_mask.overlap(self.masks,((self.pos_x+self.deplacement[0]+10)-x[0],(self.pos_y+self.deplacement[1]+self.img.get_height()-15)-x[1])):
                possible = False
        if possible:
            self.pos_x += self.deplacement[0]
            self.pos_y += self.deplacement[1]
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
        self.img.set_alpha(50)
        display.blit(self.img,(250//2-self.img.get_width()//2,100-self.img.get_height()//2))
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
        screen.blit(display_argent,(pos_x+250,pos_y+200))
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