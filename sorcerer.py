import pygame
from personnage import Perso_game
from settings import police
from settings.screen import screen
from math import trunc
from fonctions import *
from fonction import basic_checkevent
from settings import color
from settings.load_img import lvl0,lvl1,lvl2,walk_bottom

class Sorcerer(Perso_game):
    "proficient with all simple weapons but cannot wear armor"
    def __init__(self,STR=8,DEX=8,CON=8,INT=8,WIS=8,CHA=8,hp=10,hp_max=10,inventaire=10,name=None,classe=None,level=0,xp=0):
        Perso_game.__init__(self,STR,DEX,CON,INT,WIS,CHA,hp,hp_max,inventaire,walk_bottom['walk_bottom_' + str(1) +'.png'],100,100)
        self.name="anthozgg"
        self.attack=0
        self.sPoints=0
        self.spells_slots=[0,0]
        self.sort1=False
        self.sort2=False

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
            for i in range(lvl_s):
                """la liste prend la forme de liste de liste, chaque liste de liste est une action indépendente de la forme
                    [montant degat/soins,type (0=soins, 1=degats), le nombre de cible (ex 1=1 carré), la zone d'effet (1 carré ou 2 cône,
                    0 si l'élement précédent est 1),la range du sort (cible à 4 carrées max), la type de cible (0=soit même, 1=ennemies, 2=alliées),
                    dc (si 0 pas de saving throw possible),type de saving thow (si 0 à dc 0 au type)]"""
                listdeg.append([self.action.dice(4)+1,1,1,0,24,1,0,0]) 
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
        """la liste prend la forme de liste de liste, chaque liste de liste est une action indépendente de la forme
        [montant degat/soins,type (0=soins, 1=degats), le nombre de cible (ex 1=1 carré), la zone d'effet (1 carré ou 2 cône,
        0 si l'élement précédent est 1),la range du sort (cible à 4 carrées max), la type de cible (0=soit même, 1=ennemies, 2=alliées),
        dc (si 0 pas de saving throw possible),type de saving thow (si 0 à dc 0 au type)]"""
        if self.actionP>0 or self.bonusAction>0:
            listdeg.append([self.action.dice(10),1,1,0,24,1,0,0])
            if self.bonusAction>0:
                self.bonusAction-=1
            else:
                self.actionP-=1 
            if self.level>=5:
                listdeg.append([self.action.dice(10),1,1,0,24,1,0,0])
        if listdeg:
            return listdeg

    def fireball(self):
        "ce sort renvoi une liste de liste qui a la taille de son nombre de hit si le spell peut être lancé, spell lvl4"
        listdeg=[]
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
        if self.masterAction>0 and self.bonusAction>0:
            self.Action=2
            self.masterAction-=1
            self.bonusAction-=1
        else:
            running=True
            while running:
                running=board_error("no bonus action or Master Action left")
    

    """to do 
    def acid_splash(self):  (optional)
    def quickened_spell(self):  (optional)
    def Distant_spell(self): (optional)"""
    
