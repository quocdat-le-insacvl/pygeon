import pygame
from fonction import well_print_on_display,printbackgrounds,basic_checkevent,draw_text,Validation_screen,creation_img_text_click
from settings.screen import screen
from settings.load_img import *
from settings.police import *
from items import GoldCoin,A_Armor04,A_Armor05,Key1,Wikitem


key = list(Wikitem.keys())

class Quest():
    def __init__(self,text,reward_gold,reward_items,pos_x=0,pos_y=0):
        self.text = text
        self.reward_gold = reward_gold
        self.reward_items = reward_items
        self.is_accomplish = False
        self.is_accept = False
        self.pos_x = pos_x
        self.pos_y = pos_y
    def print_text(self,click=False):
        display = pygame.Surface((500,500))
        display.blit(pygame.transform.scale(img_inventaire,(500,500)),(0,0))
        display = well_print_on_display(display,self.text)
        screen.blit(display,(self.pos_x,self.pos_y))
        if creation_img_text_click(validation_button,"Accepter",ColderWeather_small,WHITE,screen,click,self.pos_x+250,self.pos_y+480,transform=True):
            self.is_accept = True
            return 1
        
    def print_reward(self,click=False):
        display = pygame.Surface((500,250))
        display.blit(pygame.transform.scale(img_inventaire,(500,250)),(0,0))
        draw_text(str(self.reward_gold),ColderWeather_small,WHITE,display,380,180)
        display.blit(pygame.transform.scale(GoldCoin.wpn_img,(50,50)),(430,180))
        draw_text("Recompense : ",ColderWeather_small,WHITE,display,30,20)
        i=0
        for x in self.reward_items:
            display.blit(pygame.transform.scale(x.wpn_img,(50,50)),(30+i*50,70))
            i+=1
        screen.blit(display,(self.pos_x+500,self.pos_y))
    def quest_accomplish(self,player):
        if self.is_accomplish:
            player.argent += self.reward_gold
            for x in self.reward_items:
                player.inventaire.ajouteritems(x)

test = Quest("Bonjour Aventurier ! J'ai perdu mes clés vous pouvez m'aider à les retrouver ? ",50,[A_Armor04,A_Armor05])
running = True
click = False


class Quest_find_items(Quest):
    def __init__(self,text,reward_gold,reward_items,looking_for):
        super().__init__(text,reward_gold,reward_items)
        self.items = looking_for

    def got_items(self,player):
        if self.is_accept:
            click = False
            display = pygame.Surface((screen.get_width(),screen.get_height()))
            display.set_colorkey((0,0,0))
            
            for i in range(len(player.inventaire.backpack)):
                if player.inventaire.backpack[i] != None:
                    if key[player.inventaire.backpack[i]] == self.items:
                        self.is_accomplish = True
                        Validation_screen("Merci Beaucoup ! Prenez la récompense",display,click)
                        return True
            Validation_screen("Vous n'avez pas encore le bonnes items !",display,click)
            return False
            screen.blit(display,(0,0))
    def print_items(self):
        draw_text("Item : ",ColderWeather_small,WHITE,screen,self.pos_x+100,self.pos_y+400)
        screen.blit(self.items.wpn_img,(225,400))
        
class Quest_kill_monster(Quest):
    def __init__(self,text,reward_gold,reward_items,which_monster):
        super().__init__(text,reward_gold,reward_items)
        self.monster = which_monster
    def is_alive(self):
        display = pygame.Surface((screen.get_width(),screen.get_height()))
        display.set_colorkey((0,0,0))
        if not self.monster.is_alive:
            self.is_accomplish = True
            Validation_screen("Merci Beaucoup ! Prenez la récompense",display,click)
            return True
        else:
            Validation_screen("Vous n'avez pas encore tue le monstre !",display,click)
            return False
            screen.blit(display,(0,0))
    def print_monster(self):
        draw_text("Monstre : ",ColderWeather_small,WHITE,screen,self.pos_x+100,self.pos_y+400)
        screen.blit(self.monster.avata,(225,400))
ouvrir_porte = Quest_find_items("Bonjour Aventurier ! J'ai perdu mes clés dans un coffre proche d ici pouvez vous m aider a les retrouver",50,[A_Armor04],Key1)
#kill_monster = Quest_kill_monster("Bonjour Aventurier ! Un monstre m'empeche de recolter mes champs pouvez vous m'aider ?",50,[A_Armor04,A_Armor05],player)
"""
while running:
    
    ouvrir_porte.print_text()
    ouvrir_porte.print_reward()
    ouvrir_porte.print_items()
    if click:
        ouvrir_porte.got_items(player)
    kill_monster.print_text(click)
    kill_monster.print_reward()
    kill_monster.print_monster()
    running,click = basic_checkevent(click)
    pygame.display.update()"""