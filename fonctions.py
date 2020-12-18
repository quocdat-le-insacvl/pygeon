import pygame
from settings import police,color
from settings.screen import WINDOWS_SIZE,screen
from settings.load_img import parchment,img_description

button=pygame.image.load(r"Addon\Menu\TextBTN_Medium.png")
buttonp=pygame.image.load(r"Addon\Menu\TextBTN_Medium_Pressed.png")

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

def board_init(i=0):
    # create a board and return it, take in arguments the size (tuple) of the board
    if i==0:
        return parchment.copy()
    if i==1:
        return img_description.copy()
    

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

title=pygame.font.Font(r'Addon\Police\ColderWeather-Regular.ttf', board_init().get_height()//10)
title2=pygame.font.Font(r'Addon\Police\21 Glyphs.ttf', board_init().get_height()//10)
subtitle=pygame.font.Font(r'Addon\Police\ColderWeather-Regular.ttf', board_init().get_height()//13)
sub2=pygame.font.Font(r'Addon\Police\21 Glyphs.ttf', board_init().get_height()//20)
text=pygame.font.Font(r'Addon\Police\ColderWeather-Regular.ttf', board_init().get_height()//30)
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