import pygame
from settings import police,color
from settings.screen import WINDOWS_SIZE,screen
from settings.load_img import parchment,img_description
from fonction import basic_checkevent,draw_text
from math import trunc

button=pygame.image.load(r"Addon\Menu\TextBTN_Medium.png")
buttonp=pygame.image.load(r"Addon\Menu\TextBTN_Medium_Pressed.png")

def exit_checkevent(event):
    if event.type == pygame.QUIT:
        pygame.quit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return False
    return True

"""quelques fonctions pour accélerer l'écriture d'une certiane couleur"""
def wgrey(police,msg):
    return police.render(msg, True, color.LIGHT_GREY)
def wbrown(police,msg):
    return police.render(msg, True, color.BROWN)
def wred(police,msg):
    return police.render(msg, True, color.RED)
def wyellow(police,msg):
    return police.render(msg, True, color.YELLOW)

def board_init(i=0):
    # create a board and return it
    if i==0:
        return parchment.copy()
    if i==1:
        return img_description.copy()
    

def board_with_msg(message):
    #take a message as argument (string) and creat a board wich is returned
    assert(len(message)<60 and type(message)==str), "message invalid in boarb_with_message"
    text2=subtitle.render(message,True,color.BROWN)
    text2=pygame.transform.scale(text2, (screen.get_width()//2,trunc(text2.get_height()*2)))
    board=pygame.transform.scale(pygame.image.load(r"Addon\Menu\UI board Small  parchment.png"),(int(text2.get_width()*1.2),text2.get_width()//2))
    board.blit(text2,(board.get_width()//2-text2.get_width()//2,text2.get_height()//2))
    return board

def choices_clickable(board,choices,rectboard=pygame.Rect((0,0),(0,0))):
    """prend en argument un liste de choix et un board, les appliquent sur ce dernier,
     si l'on veut recuperer des rects valides donner rectboard en argument"""
    assert(type(board)==pygame.Surface), "choices need a surface"
    assert((type(n)==pygame.Surface for n in choices)), "the choices are an img (surface)"
    listrect=[]
    for n in range(len(choices)):
        choices[n]=pygame.transform.scale(choices[n], (board.get_width()//(len(choices)+1), board.get_height()//3))
        listrect.append(replace_rect(rectboard,board.blit(choices[n],(choices[n].get_width()//(len(choices)+1)*(n+1)+choices[n].get_width()*n,int(board.get_height()*0.8)-choices[n].get_height()))))
    return listrect

def screenSave():
    #save the current screen on a surface wich is returned
    screensave=pygame.Surface(WINDOWS_SIZE)
    screensave.blit(screen,(0,0))
    return screensave

def replace_rect(rectsurface,rect):
    """cette fonction permet de replacer un rectangle blit sur une surface sur les coordonnées du screen
       (evidemment si la surface est scale ou reblit les coordonnées ne sont plus valides)"""
    rect.x=rect.x+rectsurface.x
    rect.y=rect.y+rectsurface.y
    return rect

def replace_rects_scale(scale_values,board,rects,rectboard):
    """cette fonction permet de scale une surface avec les rectangles qui sont sur elle,
    il faut donner, le tuple des nouvelles dimensions, la surface à scale et la liste de 
    rect sur la surface, renvoie le board scale, puis la liste"""
    x=scale_values[0]/board.get_width()
    y=scale_values[1]/board.get_height()
    for n in range(len(rects)):
        rects[n].x=trunc((rects[n].x-rectboard.x)*x)+rectboard.x
        rects[n].width=trunc(rects[n].width*x)
        rects[n].y=trunc((rects[n].y-rectboard.y)*y)+rectboard.y
        rects[n].height=trunc(rects[n].height*y)
    return pygame.transform.scale(board,scale_values),rects


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
    """initialise un bouton de confirmation"""
    t=wbrown(title,"CONFIRM")
    confirm=pygame.transform.scale(button, (t.get_width()+20, t.get_height()))
    confirmp=pygame.transform.scale(buttonp, (t.get_width()+20, t.get_height()))
    confirm.blit(t, (10,5))
    confirmp.blit(t, (10,5)) 
    return confirm,confirmp

def collides(pos,listrect):
    "vérifie la collision d'un point avec une list passés en paramètre"
    for n in range(len(listrect)):
        if listrect[n].collidepoint(pos):
            return n
    return -1

def board_error(message):
    screen.blit(board_with_msg(message),(screen.get_width()//6,screen.get_height()//6))
    pygame.display.flip()
    running=True
    click=False
    while running:
        running,click=basic_checkevent(click)
        if click: running=False
    return running

def board_with_text(msg):
    """blit a board with a text at the mouse position, word len max 30 caracter"""
    mots=msg.split(" ")
    phrase=[""]
    ligne=[]
    i=0
    for n in mots:
        if len(phrase[i])+1+len(n)>30:
            ligne.append(wbrown(subtitle,phrase[i]))
            phrase.append("")
            i+=1
        phrase[i]+=n+" "
    ligne.append(wbrown(subtitle,phrase[i]))
    i+=1
    l=ligne[0]
    for n in ligne:
        if n.get_width()>l.get_width():
            l=n
    board=pygame.transform.scale(board_init(),(l.get_width()+60,ligne[0].get_height()*(i+1)))
    for nb in range(len(ligne)):
        board.blit(ligne[nb],(30,ligne[0].get_height()*nb+ligne[0].get_height()//2))
    if board.get_height()+pygame.mouse.get_pos()[1]<screen.get_height() and board.get_width()+pygame.mouse.get_pos()[0]<screen.get_width():
        screen.blit(board,pygame.mouse.get_pos())
    elif board.get_height()+pygame.mouse.get_pos()[1]>=screen.get_height() and board.get_width()+pygame.mouse.get_pos()[0]<screen.get_width():
        screen.blit(board,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]-board.get_height()))
    elif board.get_height()+pygame.mouse.get_pos()[1]<screen.get_height() and board.get_width()+pygame.mouse.get_pos()[0]>=screen.get_width():
        screen.blit(board,(pygame.mouse.get_pos()[0]-board.get_width(),pygame.mouse.get_pos()[1]))
    else:
        screen.blit(board,(pygame.mouse.get_pos()[0]-board.get_width(),pygame.mouse.get_pos()[1]-board.get_height()))
    
    
    


title=pygame.font.Font(r'Addon\Police\ColderWeather-Regular.ttf', board_init().get_height()//10)
title2=pygame.font.Font(r'Addon\Police\21 Glyphs.ttf', board_init().get_height()//10)
subtitle=pygame.font.Font(r'Addon\Police\ColderWeather-Regular.ttf', board_init().get_height()//13)
sub2=pygame.font.Font(r'Addon\Police\21 Glyphs.ttf', board_init().get_height()//20)
text=pygame.font.Font(r'Addon\Police\ColderWeather-Regular.ttf', board_init().get_height()//17)
astxt=pygame.font.Font(r'Addon\Police\Outrun-future.otf', 20)
astxt.set_bold(1)



# board=board_with_msg("bonjour")
# im=pygame.image.load(r"Addon\end_game.png")
# im2=pygame.image.load(r"Addon\case.png")
# board=choices(board,[im,im2])
# screen.blit(board,(100,100))
# running=True
# while running:
#     pygame.display.flip()
#     exit_checkevent()