import pygame
from personnage import *
from settings.load_img import fighter_icon,neutre_icon,fighter_img
from items import image
from settings.screen import screen
from math import trunc
from fonctions import *
from fonction import basic_checkevent,draw_text
from settings import color

class Fighter(Perso):

    def __init__(self):
        "proficent avec toutes les armes"
        super().__init__(classe="fighter")
        self.hit_dice=10
        "si SW (Second Wind) est a true il est utilisable"
        self.SW=False

    def levelupchange(self):
        if super().levelupchange() :
            self.attack=self.level
            if self.level==1:
                self.SW=True

    def rest(self):
        super().rest()
        self.SW=True

    ### Actions ###
    def secondWind(self):
        if self.SW==True:
            if self.Action>0:
                if self.level>=3:
                    self.Action-=1
                    self.SW=False
                    return [[self.level,0,1,0,12,2,0,0]for n in range(3)]
                else:
                    hp_bonus=self.action.dice(10)
                    if hp_bonus+self.hp>self.hp_max:
                        self.hp=self.hp_max
                    else:
                        self.hp+=hp_bonus
                    self.Action-=1
                    self.SW=False
        else:
            running=True
            while running:
                running=board_error("no Second Wind left")

    ### Bonus Actions ###
    def extra_attack(self):
        if self.masterAction>0 and self.bonusAction>0:
            self.Action=2
            self.masterAction-=1
            self.bonusAction-=1
        else:
            running=True
            while running:
                running=board_error("no bonus action or Master Action left")
    
    ###Passives###
    def calcul_armor(self,type_of_calcul=0):
        if self.level>=2:
            return super().calcul_armor()+1
        return super().calcul_armor()
    def damage(self):
        if self.level>=2:
            return super().damage()+1
        return super().damage()
    
    ### caracter sheet du sorcerer ###

    def caracter_sheet(self):
        screenS=screenSave()
        board=pygame.transform.scale(board_init(),(900,780))
        board_icon=pygame.transform.scale(board_init(),(board.get_width()//5,board.get_height()//5))
        iconew=pygame.transform.scale(fighter_icon,(board_icon.get_width(),board_icon.get_height()))
        board_icon.blit(iconew,(board_icon.get_width()//2-iconew.get_width()//2,0))
        board_icon2=pygame.transform.scale(board_init(),(board.get_width()//5,board.get_height()//5))
        iconen=pygame.transform.scale(neutre_icon,(trunc(board_icon2.get_width()//1.2),trunc(board_icon2.get_height()//1.2)))
        board_icon2.blit(iconen,(board_icon2.get_width()//2-iconen.get_width()//2,board_icon2.get_height()//2-iconen.get_height()//2))
        draw_text("Fighter",title,"bl",board,board.get_width()//8,board.get_height()//20)
        perso=pygame.transform.scale(fighter_img,(board.get_width()//3,board.get_height()//2))
        board.blit(perso,(board.get_width()//14,board.get_height()//7))
        """initialisation de tous les boards avec les choix correspondants aux 5 differents lvl"""
        rect_choices=list()
        if self.SW:
            draw_text("Second Wind : Active",text,'b',board,board.get_width()//18,trunc(board.get_height()*0.65))
        else:
            draw_text("Second Wind : Inactive",text,'b',board,board.get_width()//18,trunc(board.get_height()*0.65))
        if self.master==False:
            draw_text("unlock master skill lvl 4",text,'b',board,board.get_width()//18,trunc(board.get_height()*0.65)+50)
        else:
            if self.masterAction:
                draw_text("master action : Active",text,'b',board,board.get_width()//18,trunc(board.get_height()*0.65)+50)
            else:
                draw_text("Master Action : Inactive",text,'b',board,board.get_width()//18,trunc(board.get_height()*0.65)+50)
        rectboard=pygame.Rect(screen.get_width()//2-board.get_width()//2,20,0,0)
        board_level1=board_with_msg("Unlock at level 1")
        rect_board1=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.03),0,0))
        rect_choices.append(choices_clickable(board_level1,[image['S_Holy02.png']],rect_board1))
        board_level1,rect_choices[0]=replace_rects_scale((trunc(board.get_width()*0.5),trunc(board.get_height()*0.2)),board_level1,rect_choices[0],rect_board1)
        board_level2=board_with_msg("Unlock at level 2")
        rect_board2=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.21),0,0))
        rect_choices.append(choices_clickable(board_level2,[image['W_Sword007.png'],image['S_Buff01.png']],rect_board2))
        board_level2,rect_choices[1]=replace_rects_scale((trunc(board.get_width()*0.5),trunc(board.get_height()*0.2)),board_level2,rect_choices[1],rect_board2)
        board_level3=board_with_msg("Unlock at level 3")
        rect_board3=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.39),0,0))
        rect_choices.append(choices_clickable(board_level3,[image['S_Holy05.png']],rect_board3))
        board_level3,rect_choices[2]=replace_rects_scale((trunc(board.get_width()*0.5),trunc(board.get_height()*0.2)),board_level3,rect_choices[2],rect_board3)
        board_level4=board_with_msg("Unlock at level 4")
        rect_board4=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.57),0,0))
        rect_choices.append(choices_clickable(board_level4,[image['S_Buff08.png']],rect_board4))
        board_level4,rect_choices[3]=replace_rects_scale((trunc(board.get_width()*0.5),trunc(board.get_height()*0.2)),board_level4,rect_choices[3],rect_board4)
        board_level5=board_with_msg("Unlock at level 5")
        rect_board5=replace_rect(rectboard,pygame.Rect(trunc(board.get_width()*0.45),trunc(board.get_height()*0.75),0,0))
        rect_choices.append(choices_clickable(board_level5,[image['W_Axe001.png']],rect_board5))
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
                    board_with_text("You unlock Second Wind, you can use it to recover between 1 and 10 hp")
                elif indice2 == 0:
                    board_with_text("Now when you wear an armor, the bonus armor is increase by 1, the damage of your weapons are increase by one too")
                elif indice2 == 1:
                    board_with_text("you could choose a skill, each time you will use an attribute reattach to your skill you will add your proficiency modifier to your score")
                elif indice3 == 0:
                    board_with_text("Second wind can heal up to 3 allies now and the amount of hp recovered is equal to your level")
                elif indice4 == 0:
                    board_with_text("You unlock your Master Action, you can use it one time between 2 rest, when you use it youcan do 2 actions in the same turn")
                elif indice5 == 0:
                    board_with_text("proficiency bonus is now at 3")
                running,click=basic_checkevent(click)
                if click==True and rect_icon.collidepoint(pygame.mouse.get_pos()):
                    if super().caracter_sheet()==0:
                        running=False
                pygame.display.flip()
        screen.blit(screenS,(0,0))

"""to do:
    def action_surge(self): |lvl1
    def champion(self): |lvl3
    def extra_attack(self): |lvl4
    toutes les comp avec items"""

        
