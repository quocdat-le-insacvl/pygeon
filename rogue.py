import pygame
from settings import police
from personnage import *
from math import trunc
from fonctions import *
from fonction import basic_checkevent,draw_text
from settings import color
from settings.load_img import Rogue_img, neutre_icon, rogue_icon
from items import image
from settings.screen import screen

class Rogue(Perso_game):

    def __init__(self,STR=8,DEX=8,CON=8,INT=8,WIS=8,CHA=8,hp=10,hp_max=10,inventaire=10,name=None,classe=None,level=0,xp=0,decalage=[0,0],size=(0,0),n_case = 0):
        Perso_game.__init__(self,STR,DEX,CON,INT,WIS,CHA,hp,hp_max,inventaire,walk_bottom['walk_bottom_' + str(1) +'.png'],100,100,decalage=decalage,size=size,player_animation=player_animation_sorcerer,name=name)
        self.hit_dice = 6
        self.classe = "rogue"
        
    def saving_throw(self,cara,damage,dc):
        """competence d'amelioration du saving throw de l'assassin"""
        dmg=super().saving_throw(cara,damage,dc)
        if dmg==damage//2 and cara==0 and self.level==2:
            return 0
        else:
            return dmg
    
    def levelupchange(self):
        if super().levelupchange():
            self.attack=self.level-1

    def damage(self,sneak):
        dmg=super().damage()
        if sneak:
            dmg+=self.action.dice(6)
            if self.level>=3:
                dmg+=self.action.dice(12)
            if self.level>=5:
                dmg+=self.action.dice(12)
        return dmg
    def uncanny_dodge(self,damage):
        if self.level>=5:
            damage=damage/2
        return damage
    
    def caracter_sheet(self):
        screenS=screenSave()
        board=pygame.transform.scale(board_init(),(900,780))
        board_icon=pygame.transform.scale(board_init(),(board.get_width()//5,board.get_height()//5))
        iconew=pygame.transform.scale(rogue_icon,(board_icon.get_width(),board_icon.get_height()))
        board_icon.blit(iconew,(board_icon.get_width()//2-iconew.get_width()//2,0))
        board_icon2=pygame.transform.scale(board_init(),(board.get_width()//5,board.get_height()//5))
        iconen=pygame.transform.scale(neutre_icon,(trunc(board_icon2.get_width()//1.2),trunc(board_icon2.get_height()//1.2)))
        board_icon2.blit(iconen,(board_icon2.get_width()//2-iconen.get_width()//2,board_icon2.get_height()//2-iconen.get_height()//2))
        draw_text("Rogue",title,"bl",board,board.get_width()//8,board.get_height()//20)
        perso=pygame.transform.scale(Rogue_img,(board.get_width()//3,board.get_height()//2))
        board.blit(perso,(board.get_width()//14,board.get_height()//7))
        """initialisation de tous les boards avec les choix correspondants aux 5 differents lvl"""
        rect_choices=list() 
        draw_text("You can use stealth on map",text,'bl',board,board.get_width()//18,trunc(board.get_height()*0.65))
        rectboard=pygame.Rect(screen.get_width()//2-board.get_width()//2,20,0,0)
        board_level1=board_with_msg("Unlock at level 1")
        rect_board1=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.03),0,0))
        rect_choices.append(choices_clickable(board_level1,[image['S_Death02.png']],rect_board1))
        board_level1,rect_choices[0]=replace_rects_scale((trunc(board.get_width()*0.5),trunc(board.get_height()*0.2)),board_level1,rect_choices[0],rect_board1)
        board_level2=board_with_msg("Unlock at level 2")
        rect_board2=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.21),0,0))
        rect_choices.append(choices_clickable(board_level2,[image['S_Holy07.png']],rect_board2))
        board_level2,rect_choices[1]=replace_rects_scale((trunc(board.get_width()*0.5),trunc(board.get_height()*0.2)),board_level2,rect_choices[1],rect_board2)
        board_level3=board_with_msg("Unlock at level 3")
        rect_board3=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.39),0,0))
        rect_choices.append(choices_clickable(board_level3,[image['S_Death01.png']],rect_board3))
        board_level3,rect_choices[2]=replace_rects_scale((trunc(board.get_width()*0.5),trunc(board.get_height()*0.2)),board_level3,rect_choices[2],rect_board3)
        board_level4=board_with_msg("Unlock at level 4")
        rect_board4=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.57),0,0))
        rect_choices.append(choices_clickable(board_level4,[image['S_Shadow07.png']],rect_board4))
        board_level4,rect_choices[3]=replace_rects_scale((trunc(board.get_width()*0.5),trunc(board.get_height()*0.2)),board_level4,rect_choices[3],rect_board4)
        board_level5=board_with_msg("Unlock at level 5")
        rect_board5=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.75),0,0))
        rect_choices.append(choices_clickable(board_level5,[image['S_Death01.png'],image['W_Axe001.png']],rect_board5))
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
                    board_with_text("You unlock sneak attack, in battle if a monster is near a wall or an ally sneak attack increase your damage by 1d6")
                elif indice2 == 0:
                    board_with_text("When you take damage from a spell and you success to a dexterity saving throw the damagess are reduces to 0")
                elif indice2 == 1:
                    board_with_text("you could choose a skill, each time you will use an attribute reattach to your skill you will add your proficiency modifier to your score")
                elif indice3 == 0:
                    board_with_text("Sneak attack deals 1d12 more")
                elif indice4 == 0:
                    board_with_text(" Unlock uncanny dodge, when you take damages from attack they are divide par two")
                elif indice5 == 0:
                    board_with_text("Sneak attack deals 1d12 more")
                elif indice5 == 1:
                    board_with_text("proficiency bonus is now at 3")
                running,click=basic_checkevent(click)
                if click==True and rect_icon.collidepoint(pygame.mouse.get_pos()):
                    if super().caracter_sheet()==0:
                        running=False
                pygame.display.flip()
        screen.blit(screenS,(0,0))