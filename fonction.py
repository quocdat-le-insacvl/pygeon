import pickle,os
from pygame.locals import *
from settings import police,color
from settings.screen import *
from settings.police import *
from settings.load_img import *
from settings.color import *
import random
# from script import demon_shadow


### Fixing path
path_pygeon = os.path.dirname(__file__)
path_save = os.path.join(path_pygeon, 'Save')
path_addon = os.path.join(path_pygeon, 'Addon')
# path_son = os.path.join(path_addon, 'Son')
path_police = os.path.join(path_addon, 'Police')
# path_menu = os.path.join(path_addon, 'Menu')
# path_demon_walk = os.path.join(path_addon, 'demon_walk')
# path_seller = os.path.join(path_addon, 'seller')
###------------------------


"""def draw_text
    Affiche un text avec la police (font) avec la couleur (color) sur un pygame surface (surface) a la position x , y"""
def draw_text(text, font, color, surface, x, y):
    if color=="bl":
        color=BLACK
    if color=="b":
        color=BROWN
    if color=="y":
        color=YELLOW
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
"""def create_text_click
    Crée un bouton par rapport un a un text passer en paramettre
    return True si l'utilisateur click sur le bouton"""
def create_text_click(text,font,color,display,click,x=0,y=0):
        text_width, text_height = font.size(text)
        button_1 = pygame.Rect(x - text_width // 2, y, text_width, text_height)
        draw_text(text,font,color,display,x - text_width // 2,y)
        if bouton_click(button_1,display,click):
            return True
"""def creation img_text_click
    Crée un bouton (pygame Rect) par rapport a une image passez en paramettre et l'affiche a l'endroit demandé
    return True si l'utilisateur click sur le bouton"""
def creation_img_text_click(img,text,font,color,display,click,x=0,y=0,button=1,left=0,right=0,Click = True):
        text_width, text_height = font.size(text)
        if img.get_width() < text_width:
            img = pygame.transform.scale(img,(text_width+50,img.get_height()))
        if(left):
            x = 0
            y = display.get_height()-img.get_height()
        elif(right):
            x = display.get_width()-img.get_width()
            y = display.get_height()-img.get_height()
        else:
            x = x-img.get_width()//2
            y = y-img.get_height()//2
        display.blit(img,(x,y))
        button_crea = pygame.Rect(x,y,img.get_width(),img.get_height())
        draw_text(text,font,color,display,x+img.get_width()//2-text_width//2,y+img.get_height()//2-img.get_height()//2)
        if Click :
            if bouton_click(button_crea,display,click):
                return True
        else:
            mx,my = pygame.mouse.get_pos()
            return button_crea.collidepoint((mx,my))
"""def validation_screen
    Affiche un message (text) pour valider une action / lancer une autre
    return True si click sur bouton suivant"""
def Validation_screen(text,display,click,choice=False):
        running = True
        while running:
            # Backgrounds :
            global img_backgrounds_warning
            #printbackgrounds(display)
            #display.fill(LIGHT_GREY)
            img_backgrounds_warning = pygame.transform.scale(img_backgrounds_warning,(display.get_width()//2,display.get_height()//4))
            display.blit(img_backgrounds_warning,(display.get_width()//2-img_backgrounds_warning.get_width()//2,display.get_height()//2-img_backgrounds_warning.get_height()))
            display.blit(exclamation,(display.get_width()//2+img_backgrounds_warning.get_width()//2.5,display.get_height()//2-1.1*img_backgrounds_warning.get_height()))
            text_width, text_height = ColderWeather_small.size(text)
            draw_text(text,ColderWeather_small,WHITE,display,display.get_width()//2-text_width//2,display.get_height()//2-text_height//2-img_backgrounds_warning.get_height()//2)
            pygame.display.update()
            if not choice :
                if creation_img_text_click(validation_button,"Valider",ColderWeather,WHITE,display,click,display.get_width()//2,display.get_height()//2):
                    return True
            else:
                if creation_img_text_click(validation_button,"Oui",ColderWeather,WHITE,display,click,display.get_width()//2-200,display.get_height()//2):
                    return True
                elif creation_img_text_click(validation_button,"Non",ColderWeather,WHITE,display,click,display.get_width()//2+200,display.get_height()//2):
                    return False
            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            running,click = basic_checkevent(click)
            pygame.display.update()
"""def printbackgrounds
    Afficher le backgrounds des menus sur display"""
def printbackgrounds(display):
        display.fill(LIGHT_GREY)
        global menu_background
        menu_background = pygame.transform.scale(menu_background,(display.get_width(),display.get_height()))
        display.blit(menu_background,(0,0))
"""def bouton_click
    Entrées :
        - Bouton Pygame Rect
        - Click Booléan
        - Display Pygame Surface
        - Constant_click Si Vrai regarde si le souris est sur le bouton (sans cliquer)
    return vrai si click sur un bouton"""
def bouton_click(bouton,display,click,constant_click = 0):
        # TEST : BOUTON EST CLIQUE ?
        mx, my = pygame.mouse.get_pos()
        mx = display.get_width() * mx / screen.get_width()
        my = display.get_height() * my / screen.get_height()
        return bouton.collidepoint((mx,my)) and click
"""def basic_checkevent
    Check les evenements utilisateur
    return Faux si press ESCAPE vrai sinon
    return Click Vrai si utlisateur click faux sinon"""
def basic_checkevent(click):
    click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False,click
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    return True,click
"""def load_game
    Affiche le menu de Sauvegarde et permet de sauvegarder "perso" dans un fichier choisit par l'utilisateur ou à l'inverse de charger un perso provenant de sauvegarde
    return perso Donné charger de sauvegarde 1 / Ou perso d'entré si juste sauvegarder"""
def load_game(click,perso):
        running = True
        Choose = False
        click=False
        num = 0
        display = pygame.Surface((1980,1024))
        while running:

            printbackgrounds(display)
            #screen.blit(img_next,(LONGUEUR-338  ,LARGEUR-112))
            #screen.blit(img_next,(0,LARGEUR-112))

            button_save_1 = pygame.Rect(100,100,display.get_width()//2-150,display.get_height()//2-150)
            button_save_2 = pygame.Rect(display.get_width()//2,100,display.get_width()//2-150,display.get_height()//2-150)
            button_save_3 = pygame.Rect(100,display.get_height()//2,display.get_width()//2-150,display.get_height()//2-150)
            button_save_4 = pygame.Rect(display.get_width()//2,display.get_height()//2,display.get_width()//2-150,display.get_height()//2-150)

            if num == 1 : pygame.draw.rect(display,RED,button_save_1)
            else : pygame.draw.rect(display,LIGHT_GREY,button_save_1,1)
            if num == 2 : pygame.draw.rect(display,RED,button_save_2)
            else : pygame.draw.rect(display,LIGHT_GREY,button_save_2,1)
            if num == 3 : pygame.draw.rect(display,RED,button_save_3)
            else : pygame.draw.rect(display,LIGHT_GREY,button_save_3,1)
            if num == 4 : pygame.draw.rect(display,RED,button_save_4)
            else : pygame.draw.rect(display,LIGHT_GREY,button_save_4,1)

            text_width, text_height = ColderWeather.size("Sauvegarde 1")
            path = r"Save\\"
            if os.path.getsize(os.path.join(path_save, 'sauvegarde')) > 0 :
                with open(os.path.join(path_save, 'sauvegarde'),'rb') as fichier:
                    mon_depickler = pickle.Unpickler(fichier)
                    inter = mon_depickler.load()
                    draw_text("Sauvegarde 1",ColderWeather,LIGHT_GREY,display,button_save_1.width//2-text_width//4,100+text_height//4)
                    draw_text("Nom : %s"%(inter.name),ColderWeather,LIGHT_GREY,display,button_save_1.width//2-text_width//4,200+text_height)
                    if bouton_click(button_save_1,display,click):
                        Choose = True
                        num = 1
                        choose_path = path + 'sauvegarde'
            else : draw_text("VIDE",ColderWeather,LIGHT_GREY,display,button_save_1.width//2-text_width//4,100+text_height//4)

            if os.path.getsize(os.path.join(path_save, 'sauvegarde2')) > 0 :
                with open(os.path.join(path_save, 'sauvegarde2'),'rb') as fichier:
                    mon_depickler = pickle.Unpickler(fichier)
                    inter = mon_depickler.load()
                    draw_text("Sauvegarde 2",ColderWeather,LIGHT_GREY,display,(100-text_width//2+(display.get_width()//2-100)//2)+display.get_width()//2-100,100+text_height//4)
                    draw_text("Nom : %s"%(inter.name),ColderWeather,LIGHT_GREY,display,(100-text_width//2+(display.get_width()//2-100)//2)+display.get_width()//2-100,200+text_height)
                    if bouton_click(button_save_2,display,click):
                        Choose = True
                        num = 2
                        choose_path = path + 'sauvegarde2'
            else : draw_text("VIDE",ColderWeather,LIGHT_GREY,display,button_save_1.width//2-text_width//4,100+text_height//4)

            if os.path.getsize(os.path.join(path_save, 'sauvegarde3')) > 0 :
                with open(os.path.join(path_save, 'sauvegarde3'),'rb') as fichier:
                    mon_depickler = pickle.Unpickler(fichier)
                    inter = mon_depickler.load()
                    draw_text("Sauvegarde 3",ColderWeather,LIGHT_GREY,display,100-text_width//2+(display.get_width()//2-100)//2,text_height//4+display.get_height()//2)
                    draw_text("Nom : %s"%(inter.name),ColderWeather,LIGHT_GREY,display,100-text_width//2+(display.get_width()//2-100)//2,text_height//4+display.get_height()//2+200)
                    if bouton_click(button_save_3,display,click):
                        Choose = True
                        num = 3
                        choose_path = path + 'sauvegarde3'
            else : draw_text("VIDE",ColderWeather,LIGHT_GREY,display,button_save_1.width//2-text_width//4,100+text_height//4)

            if os.path.getsize(os.path.join(path_save, 'sauvegarde4')) > 0 :
                with open(os.path.join(path_save, 'sauvegarde4'),'rb') as fichier:
                    mon_depickler = pickle.Unpickler(fichier)
                    inter = mon_depickler.load()
                    draw_text("Sauvegarde 4",ColderWeather,LIGHT_GREY,display,(100-text_width//2+(display.get_width()//2-100)//2)+display.get_width()//2-100,text_height//4+display.get_height()//2)
                    draw_text("Nom : %s"%(inter.name),ColderWeather,LIGHT_GREY,display,(100-text_width//2+(display.get_width()//2-100)//2)+display.get_width()//2-100,text_height//4+display.get_height()//2+200)
                    if bouton_click(button_save_4,display,click):
                        Choose = True
                        num = 4
                        choose_path = path + 'sauvegarde4'
            else : draw_text("VIDE",ColderWeather,LIGHT_GREY,display,button_save_1.width//2-text_width//4,100+text_height//4)


            if (Choose):
                if creation_img_text_click(img_next,"Sauvegarder",ColderWeather,WHITE,display,click,0,0,right=1):
                    if perso.name == None:
                        Validation_screen("Erreur : Nom incorrect",display,click)
                    else:
                        click = False
                        text = 'Etes vous sur de vouloir sauvegarder ?'
                        if(Validation_screen(text,display,click)):
                            with open(choose_path,'wb') as fichier:
                                mon_pickler = pickle.Pickler(fichier)
                                mon_pickler.dump(perso)

                if creation_img_text_click(img_next,"Charger",ColderWeather,WHITE,display,click,0,0,left=1):
                    click = False
                    if (Validation_screen('Etes vous sur de vouloir charger ?',display,click)):
                        with open(choose_path,'rb') as fichier:
                            mon_depickler = pickle.Unpickler(fichier)
                            perso = mon_depickler.load()
                        return perso

            screen.blit(pygame.transform.scale(display,WINDOWS_SIZE),(0,0))
            running,click = basic_checkevent(click)
            pygame.display.update()

""" def load_map
    Chargement de la carte, crée une nouvelle ligne a chaque \n
    Return Map Une liste de liste contenant des charactères"""
def load_map(path):
    f = open(path,'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    map = []
    for row in data:
        map.append(list(row))
    return map
""" def print_map(self,Map,display):
        Affichage de la carte sur un Display,Chaque numéro contenue dans Map correspond a une case précise du sol et à une propriété
        Return Display Pygame Surface qui contient le sol de la carte
        Return collision Liste de position pour pixel_red (bloc de collision) permet de faire les collision
        Return collision_change_camera List de position pour pixel (bloc de collision) permet de changer l'affichage
        Return tree_position List de postion des Arbres
        Return collision_entity List de position pour pixel_red (bloc de collision) permet l'interaction avec les entitées fixes"""
"""def print_mooving_entity
    Affiche les entités non static sur le display"""


def exit_checkevent(event):
    if event.type == pygame.QUIT:
        pygame.quit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return False
    return True

def wgrey(police,msg):
    return police.render(msg, True, color.LIGHT_GREY)
def wbrown(police,msg):
    return police.render(msg, True, color.BROWN)
def wred(police,msg):
    return police.render(msg, True, color.RED)
def wyellow(police,msg):
    return police.render(msg, True, color.YELLOW)


def replace_rect(rectsurface,rect):
    """cette fonction permet de replacer un rectangle blit sur une surface sur les coordonnées du screen
       (evidemment si la surface est scale ou reblit les coordonnées ne sont plus valides)"""
    rect.x=rect.x+rectsurface.x
    rect.y=rect.y+rectsurface.y
    return rect

def init_buttonsas():
    #initialise les boutons + et -
    add=wbrown(astxt,"+")
    buttonpa=pygame.transform.scale(buttonp, (70, add.get_height()))
    buttonps=pygame.transform.scale(buttonp, (70, add.get_height()))
    buttonpa.blit(add,(buttonpa.get_width()//2-add.get_width()//2,buttonpa.get_height()//2-add.get_height()/2))
    sub=wbrown(astxt,"-")
    buttonps.blit(sub,(buttonps.get_width()//2-sub.get_width()//2,buttonps.get_height()//2-sub.get_height()/2))
    buttonAdd=pygame.transform.scale(button, (70, add.get_height()))
    buttonSub=pygame.transform.scale(button, (70, add.get_height()))
    buttonAdd.blit(add,(buttonAdd.get_width()//2-add.get_width()//2,buttonAdd.get_height()//2-add.get_height()/2))
    buttonSub.blit(sub,(buttonSub.get_width()//2-sub.get_width()//2,buttonSub.get_height()//2-sub.get_height()/2))
    return buttonAdd,buttonSub,buttonpa,buttonps

def confirm_button():
    t=wbrown(title,"CONFIRM")
    confirm=pygame.transform.scale(button, (t.get_width()+20, t.get_height()))
    confirmp=pygame.transform.scale(buttonp, (t.get_width()+20, t.get_height()))
    confirm.blit(t, (10,5))
    confirmp.blit(t, (10,5)) 
    return confirm,confirmp

def board_with_msg(message):
    #take a message as argument (string) and creat a board wich is returned
    assert(len(message)<35 and type(message)==str), "message invalid in boarb_with_message"
    text2=police.Outrun_future.render(message,True,color.RED)
    board=pygame.transform.scale(pygame.image.load(r"Addon\Menu\UI board Small  parchment.png"),(text2.get_width()+200,text2.get_height()*4))
    board.blit(text2,(board.get_width()//2-text2.get_width()//2,text2.get_height()+20))
    return board


def choices(board,choices):
    assert(type(board)==pygame.Surface), "choices need a surface"
    assert(len(choices)<=5), "to much choice"
    assert((type(n)==pygame.Surface for n in choices)), "the choices are an img (surface)"
    for n in range(len(choices)):
        choices[n]=pygame.transform.scale(choices[n], (board.get_width()//(len(choices)+1), board.get_height()//3))
        board.blit(choices[n],(choices[n].get_width()//(len(choices)+1)*(n+1)+choices[n].get_width()*n,board.get_height()-choices[n].get_height()-30))
    return board


def screenSave():
    #save the current screen on a surface wich is returned
    screensave=pygame.Surface(WINDOWS_SIZE)
    screensave.blit(screen,(0,0))
    return screensave

def print_mooving_entity(game, display,list_entity,center_x,center_y):
    for entity in list_entity:
        # Use try to prevent the entity who is out of the map 
        try : 
            # Dat's note : 
            # if hidden, check if him go out of the zone visible
            # Check if the monster in the fog => he is hidden !
            if game.fog.surface.get_at((entity.pos_x, entity.pos_y)) != NIGHT_COLOR:
                entity.is_hidden = False
                entity.seen = True
                display.blit(entity.display, (entity.pos_x + center_x, entity.pos_y+center_y))
                entity.last_know_pos = (entity.pos_x, entity.pos_y)
            else:
                entity.is_hidden = True
        except:
            print("Error of entity : ", entity.name, entity , " out of the map !")
            
        # If he was seen but now he is hidden => draw his shadow (by the last position)
        if entity.seen and entity.is_hidden:
            display.blit(entity.shadow, (entity.last_know_pos[0] +
                                         center_x, entity.last_know_pos[1] + center_y))




