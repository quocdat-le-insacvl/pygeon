import pygame
from os import *
from settings.load_img import *
from entity import *
from fonction import *
from fonctions import *
from settings.color import *
from Button import *
from settings.setting import *
from settings.police import *
fontObj = pygame.font.Font('FreeSansBold.ttf', 32)
class ControlsMenu():
    def __init__(self, game):
        self.ctrl_list=[int(ctrl) for ctrl in self.search_keys(SETTINGS[2][12:-1])]
        i=0
        self.list_action=[]
        #init name of key
        for k in KEYS_DICO:
            KEYS_DICO[k]=self.ctrl_list[i]
            self.list_action.append(Text(self.game.display, SCREEN_WIDTH*(1+2*(i%2))//5, SCREEN_HEIGHT//3+50*(i//2), k[1:], ColderWeather, WHITE, 40, False))
            i+=1
        #init button
        self.save_text = Validation_screen("Voulez-vous enregistrer ?", display, self.click)
        self.warning_text = Validation_screen("Touches qui se chevauchent", display, self.click)
        self.list_button=[Button(self.game, SCREEN_WIDTH*(2+2*(i%2))//5, SCREEN_HEIGHT//3+50*(i//2), pygame.key.name(self.ctrl_list[i]), ColderWeather, BLACK, 30,button,buttonp) for i in range(len(self.ctrl_list))]
        self.save_button = Button(self.game, 175, 150, "Save", ColderWeather, WHITE, 50,background=button)
        self.background = printbackgrounds(display)
    def search_keys(self,ligne):
        "Get the key from the settings"
        w=''
        flag=False
        for c in SETTINGS[2]:
            if c=="[" or c=="]": flag= not flag
            elif flag and c!=',': w+=c
            if w!='' and (not flag or c==","): 
                yield w
                w=''    
    def display_menu(self):
        """Displays the menu"""
        self.run_display = True 
        while self.run_display:
            self.game.check_events()
            self.game.display.blit(self.menu_background, (0,0))
            #display buttons
            for butt in self.list_button:
                butt.display_button()
                butt.color_on_mouse(WHITE)
            #display texts
            for text in self.list_action:
                text.display_text()
            if self.save_text[0]: self.save_text[1].display_text()
            if self.warning_text[0]: self.warning_text[1].display_text()
            self.return_button.display_button()
            self.return_button.color_on_mouse(WHITE)
            self.save_button.display_button()
            self.save_button.color_on_mouse(WHITE)
            self.display.update()
    def check_input(self, event):
        """Checks user input"""
        for butt in self.list_button:
            if butt.is_clicked(event):  #change the shortcut
                self.save_text[0]=True  #Need to save
                self.warning_text[0]=False
                butt.text='_'
                butt.text_surface = butt.font_obj.render('_', True, pygame.Color(butt.text_color))
                butt.display_button()
                butt.color_on_mouse(WHITE)
                self.redraw_screen()
                run=True
                while run:  #wait for a keys to be pressed
                    for event in pygame.event.get():
                        if event.type==pygame.KEYDOWN:
                            run=False
                            key=pygame.key.name(event.key)
                            butt.text=key
                            butt.text_surface = butt.font_obj.render(key, True, pygame.Color(butt.text_color))
                            butt.rectText = butt.text_surface.get_rect()
                            butt.rectText.center = butt.rect.center
                self.save_button.button_background=button
                self.save_button.text_surface = self.save_button.font_obj.render(self.save_button.text, True, pygame.Color(BLACK))
        if self.save_button.is_clicked(event):  #save all keys
            new_ctrl_list= []
            flag=True
            for butt in self.list_button:   #check if ther is no overlapping keys
                if pygame.key.key_code(butt.text) in new_ctrl_list: flag=False
                new_ctrl_list.append(pygame.key.key_code(butt.text))
            if flag:
                self.ctrl_list=new_ctrl_list
                i=0
                for k in KEYS_DICO:
                    KEYS_DICO[k]=int(self.ctrl_list[i])
                    i+=1
                SETTINGS[2]=f"CTRL_LIST={new_ctrl_list}\n"
                with open('Save/settings.txt','w') as options:
                    options.write("".join(f'{optn}' for optn in SETTINGS))
                self.save_button.button_background=button
                self.save_button.text_surface = self.save_button.font_obj.render(self.save_button.text, True, pygame.Color(WHITE))
                self.warning_text[0],self.save_text[0]=False,False
            else: self.warning_text[0]=True
        if self.return_button.is_clicked(event):
            self.game.current_menu = self.game.options_menu
            self.run_display = False        