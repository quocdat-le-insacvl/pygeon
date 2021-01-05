import pygame
from personnage import Perso
from settings import police
from settings.screen import screen
from math import trunc
from fonctions import *
from fonction import basic_checkevent,draw_text
from settings import color
from settings.load_img import lvl0,lvl1,lvl2,wizard_hide,wizard_icon, neutre_icon
from items import image
from settings.screen import screen

class Sorcerer(Perso):
    "proficient with all simple weapons but cannot wear armor"
    def __init__(self,STR=8,DEX=8,CON=8,INT=8,WIS=8,CHA=8,level=0,xp=0):
        super().__init__(classe="sorcerer",hit_dice=6)
        self.name="anthozgg"
        self.attack=0
        self.sPoints=0
        self.spells_slots=[0,0]
        self.sort1=False
        self.sort2=False
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA

    def levelupchange(self):
        if super().levelupchange():
            if self.level==1:
                self.spells_slots[0]=2
                self.sort1=True
            elif self.level==2:
                self.spells_slots[0]=3
            elif self.level==3:
                self.spells_slots[0]=4
                self.spells_slots[1]=2
                self.sort2=True
            elif self.level==4:
                self.spells_slots[1]=3
            
            if self.level>=2:
                self.sPoints=self.level
                self.attack=trunc(self.level/2)

    #################Sorts#################
    #Level1:

    def magic_missile(self):
        "ce sort renvoi une liste de liste qui a la taille de son nombre de hit si le spell peut être lancé, spell lvl1"
        screenS=screenSave()
        listdeg=[]
        lvl_s=False
        running=True
        click=False
        if any([self.armor[0],self.armor[1],self.armor[2],self.armor[3]]):
            running=board_error("cannot lunch spell and wear armor")
            return False
        board=board_with_msg("Choose a lvl to cast your spell, esc pour annuler")
        boardrect=screen.blit(board,(screen.get_width()//4,screen.get_height()//4))
        rect_list_choice=choices_clickable(board,[lvl1,lvl2],boardrect)
        screen.blit(board,(screen.get_width()//4,screen.get_height()//4))
        pygame.display.flip()
        while running:
            indice=collides(pygame.mouse.get_pos(),rect_list_choice)
            running,click=basic_checkevent(click)
            "vérifie si il reste des spells slots au joueur"
            if (self.spells_slots[0]!=0 or self.spells_slots[1]!=0) and self.actionP>0:
                if click and indice!=-1:
                    if indice==0:
                        if self.spells_slots[0]==0:
                            running=board_error("Not enough spell slot for this lvl")
                        else:
                            lvl_s=1
                            self.spells_slots[0]-=1
                            running=False
                            self.actionP-=1
                    elif indice==1:
                        if self.spells_slots[1]==0:
                            running=board_error("Not enough spell slot for this lvl")
                        else:
                            lvl_s=2
                            self.spells_slots[1]-=1
                            running=False
                            self.actionP-=1
            else:
                running=board_error("no spell slot anymore or no action left")
        if lvl_s:
                """la liste prend la forme de liste de liste, chaque liste de liste est une action indépendente de la forme
                    [montant degat/soins,type (0=soins, 1=degats), le nombre de cible (ex 1=1 carré), la zone d'effet (1 carré ou 2 cône,
                    0 si l'élement précédent est 1),la range du sort (cible à 4 carrées max), la type de cible (0=soit même, 1=ennemies, 2=alliées),
                    dc (si 0 pas de saving throw possible),type de saving thow (si 0 à dc 0 au type)]"""
                listdeg=[[self.action.dice(4)+1,1,1,0,24,1,0,0] for n in range(lvl_s)] 
        screen.blit(screenS,(0,0))
        if listdeg:
            return listdeg

    def convertSP(self):
        "permet de convertir des sorcery points en spell slots"
        screenS=screenSave()
        board=board_with_msg("choisir spell slot a obtenir, esc pour annuler")
        rect_board=pygame.Rect(screen.get_width()//8,screen.get_height()//8,0,0)
        level1=wbrown(subtitle,"Spell slot level1")
        level2=wbrown(subtitle,"Spell slot level2")
        choiceList=choices_clickable(board,[level1,level2],rect_board)
        screen.blit(board,(screen.get_width()//8,screen.get_height()//8))
        pygame.display.flip()
        running=True
        click=False
        "indice pour savoir si une action s'est réalisée"
        while running:
            if self.sPoints>=2 and self.bonusAction>0:
                indice=collides(pygame.mouse.get_pos(),choiceList)
                running,click=basic_checkevent(click)
                if(click and indice!=-1):
                    if indice==0:
                        self.spells_slots[0]+=1
                        self.sPoints-=2
                        self.bonusAction-=1
                        running=False
                    if indice==1:
                        if self.sPoints<3:
                            running=board_error("not enough sorcery points")
                        else:
                            self.spells_slots[1]+=1
                            self.sPoints-=3
                            self.bonusAction-=1
                            running=False
            else:
                running=board_error("not enough point")
        screen.blit(screenS,(0,0))

    def rest(self):
        super().rest()
        if self.level==1:
            self.spells_slots[0]=2
        elif self.level==2:
            self.spells_slots[0]=3
        elif self.level==3:
            self.spells_slots[0]=4
            self.spells_slots[1]=2
        elif self.level==4:
            self.spells_slots[1]=3
        if self.level>=2:
            self.sPoints=self.level

    def convertSpellS(self):
        "permet de convertir des spell slots points en sorcery points"
        screenS=screenSave()
        board=board_with_msg("choisir spell slot a obtenir, esc pour annuler")
        rect_board=pygame.Rect(screen.get_width()//8,screen.get_height()//8,0,0)
        level1=wbrown(subtitle,"2 sorceryP")
        level2=wbrown(subtitle,"3 sorceryP")
        choiceList=choices_clickable(board,[level1,level2],rect_board)
        screen.blit(board,(screen.get_width()//8,screen.get_height()//8))
        pygame.display.flip()
        running=True
        click=False
        while running:
            if self.spells_slots[0]!=0 or self.spells_slots[1]!=0 and self.bonusAction>0:
                indice=collides(pygame.mouse.get_pos(),choiceList)
                running,click=basic_checkevent(click)
                if(click and indice!=-1):
                    if indice==0:
                        if self.level-self.sPoints<2:
                            running=board_error("cannot do that to much sorcery points")
                        elif self.spells_slots[0]==0:
                            running=board_error("not enough sorcery points")
                        else:
                            self.sPoints+=2
                            self.spells_slots[0]-=1
                            self.bonusAction-=1
                            running=False
                    if indice==1:
                        if self.level-self.sPoints<3:
                            running=board_error("cannot do that to much sorcery points")
                        elif self.spells_slots[1]==0:
                            running=board_error("not enough sorcery points")
                        else:
                            self.sPoints+=3
                            self.spells_slots[1]-=1
                            self.bonusAction-=1
                            running=False
            else:
                running=board_error("not enough point")
        screen.blit(screenS,(0,0))

    def firebolt(self):
        "ce sort renvoi une liste de liste qui a la taille de son nombre de hit si le spell peut être lancé, cantrip"
        listdeg=[]
        if any([self.armor[0],self.armor[1],self.armor[2],self.armor[3]]):
            running=board_error("cannot lunch spell and wear armor")
            return False
        """la liste prend la forme de liste de liste, chaque liste de liste est une action indépendente de la forme
        [montant degat/soins,type (0=soins, 1=degats), le nombre de cible (ex 1=1 carré), la zone d'effet (1 carré ou 2 cône,
        0 si l'élement précédent est 1),la range du sort (cible à 4 carrées max), la type de cible (0=soit même, 1=ennemies, 2=alliées),
        dc (si 0 pas de saving throw possible),type de saving thow (si 0 à dc 0 au type)]"""
        if self.actionP>0 or self.bonusAction>0:
            listdeg.append([self.action.dice(9)+1,1,1,0,24,1,0,0])
            if self.bonusAction>0:
                self.bonusAction-=1
            else:
                self.actionP-=1 
            if self.level>=5:
                listdeg.append([self.action.dice(10),1,1,0,24,1,0,0])
        if listdeg:
            return listdeg

    def fireball(self):
        "ce sort renvoi une liste de liste qui a la taille de son nombre de hit si le spell peut être lancé, spell lvl3"
        listdeg=[]
        if any([self.armor[0],self.armor[1],self.armor[2],self.armor[3]]):
            running=board_error("cannot lunch spell and wear armor")
            return False
        if self.spells_slots[1]>0 and self.actionP>0:
            """la liste prend la forme de liste de liste, chaque liste de liste est une action indépendente de la forme
            [montant degat/soins,type (0=soins, 1=degats), le nombre de cible (ex 1=1 carré de proximité, 2 tous les carrés contact a la cible),
            la zone d'effet (1 carré ou 2 cône,0 si l'élement précédent est 1),la range du sort (cible à 4 carrées max),
            la type de cible (0=soit même, 1=ennemies, 2=alliées),dc (si 0 pas de saving throw possible),
            type de saving thow (si 0 à dc 0 au type),1 pour dex, 2 pour con,3 pour will]"""   
            deg=self.action.dice(6)+self.action.dice(6)+self.action.dice(6)+self.action.dice(6)+self.action.dice(6)+self.action.dice(6) 
            listdeg.append([deg,1,2,1,24,1,10+3+self.score("con"),1]) 
            self.spells_slots[1]-=1
            self.actionP-=1
        elif self.sort2==False:
            running=True
            screenS=screenSave()
            while running:
                running=board_error("this spell is not unlock for now")
            screen.blit(screenS,(0,0))
        else:
            running=True
            screenS=screenSave()
            while running:
                running=board_error("not enough spell slot or action to cast this spell")
            screen.blit(screenS,(0,0))
        if listdeg:
            return listdeg
    
    def quick_spell(self):
        if any([self.armor[0],self.armor[1],self.armor[2],self.armor[3]]):
            running=board_error("cannot lunch spell and wear armor")
            return False
        if self.masterAction>0 and self.bonusAction>0:
            self.Action=2
            self.masterAction-=1
            self.bonusAction-=1
        else:
            running=True
            while running:
                running=board_error("no bonus action or Master Action left")
    
    ### caracter sheet du sorcerer ###

    def caracter_sheet(self):
        screenS=screenSave()
        board=pygame.transform.scale(board_init(),(900,780))
        board_icon=pygame.transform.scale(board_init(),(board.get_width()//5,board.get_height()//5))
        iconew=pygame.transform.scale(wizard_icon,(board_icon.get_width()//2,board_icon.get_height()))
        board_icon.blit(iconew,(board_icon.get_width()//2-iconew.get_width()//2,0))
        board_icon2=pygame.transform.scale(board_init(),(board.get_width()//5,board.get_height()//5))
        iconen=pygame.transform.scale(neutre_icon,(trunc(board_icon2.get_width()//1.2),trunc(board_icon2.get_height()//1.2)))
        board_icon2.blit(iconen,(board_icon2.get_width()//2-iconen.get_width()//2,board_icon2.get_height()//2-iconen.get_height()//2))
        draw_text("Sorcerer",title,"b",board,board.get_width()//8,board.get_height()//20)
        perso=pygame.transform.scale(wizard_hide['wizard_idle_1.png'],(board.get_width()//3,board.get_height()//2))
        board.blit(perso,(board.get_width()//14,board.get_height()//7))
        """initialisation de tous les boards avec les choix correspondants aux 5 differents lvl"""
        rect_choices=list()
        draw_text("Sorcery Points : "+ str(self.sPoints),subtitle,'bl',board,board.get_width()//18,trunc(board.get_height()*0.65))
        draw_text("Spells Slots lvl 1 : "+ str(self.spells_slots[0]),subtitle,'bl',board,board.get_width()//18,trunc(board.get_height()*0.65)+50)
        draw_text("Spells Slots lvl 2 : "+ str(self.spells_slots[1]),subtitle,'bl',board,board.get_width()//18,trunc(board.get_height()*0.65)+100)
        rectboard=pygame.Rect(screen.get_width()//2-board.get_width()//2,20,0,0)
        board_level1=board_with_msg("Unlock at level 1")
        rect_board1=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.03),0,0))
        rect_choices.append(choices_clickable(board_level1,[image['S_Magic01.png'],image['S_Fire01.png']],rect_board1))
        print(rect_choices)
        board_level1,rect_choices[0]=replace_rects_scale((trunc(board.get_width()*0.5),trunc(board.get_height()*0.2)),board_level1,rect_choices[0],rect_board1)
        print(rect_choices)
        board_level2=board_with_msg("Unlock at level 2")
        rect_board2=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.21),0,0))
        rect_choices.append(choices_clickable(board_level2,[image['S_Shadow02.png'],image['S_Buff01.png']],rect_board2))
        board_level2,rect_choices[1]=replace_rects_scale((trunc(board.get_width()*0.5),trunc(board.get_height()*0.2)),board_level2,rect_choices[1],rect_board2)
        board_level3=board_with_msg("Unlock at level 3")
        rect_board3=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.39),0,0))
        rect_choices.append(choices_clickable(board_level3,[image['S_Fire02.png']],rect_board3))
        board_level3,rect_choices[2]=replace_rects_scale((trunc(board.get_width()*0.5),trunc(board.get_height()*0.2)),board_level3,rect_choices[2],rect_board3)
        board_level4=board_with_msg("Unlock at level 4")
        rect_board4=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.57),0,0))
        rect_choices.append(choices_clickable(board_level4,[image['S_Buff09.png']],rect_board4))
        board_level4,rect_choices[3]=replace_rects_scale((trunc(board.get_width()*0.5),trunc(board.get_height()*0.2)),board_level4,rect_choices[3],rect_board4)
        board_level5=board_with_msg("Unlock at level 5")
        rect_board5=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.75),0,0))
        rect_choices.append(choices_clickable(board_level5,[image['S_Fire04.png'],image['W_Axe001.png']],rect_board5))
        board_level5,rect_choices[4]=replace_rects_scale((trunc(board.get_width()*0.5),trunc(board.get_height()*0.2)),board_level5,rect_choices[4],rect_board5)
        board.blit(board_level1,(trunc(board.get_width()*0.45),trunc(board.get_height()*0.03)))
        board.blit(board_level2,(trunc(board.get_width()*0.45),trunc(board.get_height()*0.21)))
        board.blit(board_level3,(trunc(board.get_width()*0.45),trunc(board.get_height()*0.39)))
        board.blit(board_level4,(trunc(board.get_width()*0.45),trunc(board.get_height()*0.57)))
        board.blit(board_level5,(trunc(board.get_width()*0.45),trunc(board.get_height()*0.75)))
        running=True
        click=False
        if super().caracter_sheet():
            rect_icon=screen.blit(board_icon2,(rectboard.x-board_icon.get_width()//1.5,rectboard.y+board_icon.get_height()*0.2))
            screen.blit(board,(rectboard.x,rectboard.y))
            screen.blit(board_icon,(rectboard.x-board_icon.get_width()//1.5,rectboard.y+board_icon.get_height()//0.8))
            ScreenS2=screenSave()
            while running:
                screen.blit(ScreenS2,(0,0))
                indice1=collides(pygame.mouse.get_pos(),rect_choices[0])
                indice2=collides(pygame.mouse.get_pos(),rect_choices[1])
                indice3=collides(pygame.mouse.get_pos(),rect_choices[2])
                indice4=collides(pygame.mouse.get_pos(),rect_choices[3])
                indice5=collides(pygame.mouse.get_pos(),rect_choices[4])
                if indice1 == 0:
                    board_with_text("missile magic can be lunch at lvl 1 to lunch one missil or at level 2 to lunch 2 missil, it inflict between 1 and 5 damage")
                elif indice1 == 1:
                    board_with_text("fire bolt is a cantrip he doesn't use spell slot, it can be lunch as a bonus action, it inflicts between 1 and 10 damages")
                elif indice2 == 0:
                    board_with_text("Now you can use sorcery points, the amount is equal to your level you can use sorcery points to recover spell slots or use spell slots to recover sorcery points")
                elif indice2 == 1:
                    board_with_text("you could choose a skill, each time you will use an attribute reattach to your skill you will add your proficiency modifier to your score")
                elif indice3 == 0:
                    board_with_text("You unlock fire ball, this spell deals between 6 and 36 damages in a square area")
                elif indice4 == 0:
                    board_with_text("You unlock your mastery action quick spell, you can use this action one time between 2 rest, this bonus action allow you to lunch 2 spell in the same turn")
                elif indice5 == 0:
                    board_with_text("firebolt lunch two firebolt now")
                elif indice5 == 1:
                    board_with_text("proficiency bonus is now at 3")
                running,click=basic_checkevent(click)
                if click==True and rect_icon.collidepoint(pygame.mouse.get_pos()):
                    if super().caracter_sheet()==0:
                        running=False
                pygame.display.flip()
        screen.blit(screenS,(0,0))

    """to do 
    def acid_splash(self):  (optional)
    def quickened_spell(self):  (optional)
    def Distant_spell(self): (optional)"""
    
