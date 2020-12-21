import pygame
from personnage import Perso
from settings import screen
from math import trunc
from fonctions import *
from fonction import basic_checkevent
from settings import color
from settings.load_img import lvl0,lvl1,lvl2

class Sorcerer(Perso):
    "proficient with all simple weapons but cannot wear armor"
    def __init__(self,STR=8,DEX=8,CON=8,INT=8,WIS=8,CHA=8,hp=10,hp_max=10,inventaire=10,name=None,classe=None,level=0,xp=0):
        super().__init__(classe="sorcerer",hit_dice=6)
        self.name="anthozgg"
        self.attack=0
        self.sPoints=0
        self.spells_slots=[]
        self.spells_slots_eph=[]

    
    


    def get_class(self):
        print(self.classe)

    #################Sorts#################
    #Level1:

    def magic_missile(self):
        "ce sort renvoi un generateur qui a la taille de son nombre de hit et qui fait des degats à chaque itérations"
        screenS=screenSave()
        listdeg=[]
        lvl_s=False
        running=True
        click=False
        board=board_with_msg("Choose a lvl to cast your spell")
        boardrect=screen.blit(board,(screen.get_width()//4,screen.get_height()//4))
        rect_list_choice=choices_clickable(board,[lvl1,lvl2],boardrect)
        screen.blit(board,(screen.get_width()//4,screen.get_height()//4))
        pygame.display.flip()
        while running:
            indice=collides(pygame.mouse.get_pos(),rect_list_choice)
            running,click=basic_checkevent(click)
            if click and indice!=-1:
                if indice==0:
                    lvl_s=1
                    running=False
                elif indice==1:
                    lvl_s=2
                    running=False
        if lvl_s:
            for i in range(lvl_s):
                """la liste prend la forme de liste de liste, chaque liste de liste est une action indépendente de la forme
                    [montant degat/soins,type (0=soins, 1=degats), le nombre de cible (ex 1=1 carré), la zone d'effet (1 carré ou 2 cône,
                    0 si l'élement précédent est 1),la range du sort (cible à 4 carrées max), la type de cible (0=soit même, 1=ennemies, 2=alliées),
                    dc (si 0 pas de saving throw possible),type de saving thow (si 0 à dc 0 au type)]"""
                listdeg.append([self.action.dice(4)+1,1,1,0,24,1,0,0]) 
        screen.blit(screenS,(0,0))
        return listdeg

    
    def levelupchange(self):
        super().levelupchange()
        if self.level==1:
            self.spells_slots.append(2)
        elif self.level==2:
            self.spells_slots[0]=3
        elif self.level==3:
            self.spells_slots[0]=4
            self.spells_slots.append(2)
        elif self.level==4:
            self.spells_slots[1]=3
        if self.level>=2:
            self.sPoints=self.level
            self.attack=trunc(self.level/2)

    def convert_sorc(self):
        "permet de convertir des sorcery points en spell slots"
        screenS=screenSave()
        board_with_msg("choisir spell slot (SP) à obtenir")
        


    """to do 

    def convert_spell_slot(self):
    def fireball(self):     |spell lvl4
    def acid_splash(self):  
    def True_strike(self):
    def quickened_spell(self):
    def Distant_spell(self): (optional)
    def twined_spell(self): (optional)
    def learn_spell(self):"""
    
