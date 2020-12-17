import pygame
from settings import police,color
from settings.screen import WINDOWS_SIZE,screen
from settings.load_img import menu_background,img_description

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
        return pygame.image.load(r"Addon\Menu\UI board Large  parchment.png")
    if i==1:
        return pygame.image.load(r"Addon\Menu\UI board Large stone.png")
    

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
def surfacesave(surface):
    #save the current screen on a surface wich is returned
    screensave=pygame.Surface((surface.get_width(),surface.get_height()))
    screensave.blit(surface,(0,0))
    return screensave

    """
        screen.blit(board,(WINDOWS_SIZE[0]//2-board.get_width()//2,WINDOWS_SIZE[1]//2-board.get_height()//2))
        pygame.display.flip()
        running=True
        while running:
            for events in pygame.event.get():
                if all([events.type==pygame.MOUSEBUTTONUP,excl_rect.collidepoint((pygame.mouse.get_pos()[0]-WINDOWS_SIZE[0]//2+board.get_width()//2,pygame.mouse.get_pos()[1]-WINDOWS_SIZE[1]//2+board.get_height()//2))]):
                    screen.blit(screen_S,(0,0))
                    pygame.display.flip()
                    running=False
                elif events.type==pygame.QUIT:
                    pygame.quit()
                    running=False
"""


title=pygame.font.Font(r'Addon\Police\ColderWeather-Regular.ttf', board_init().get_height()//10)
title2=pygame.font.Font(r'Addon\Police\21 Glyphs.ttf', board_init().get_height()//10)
subtitle=pygame.font.Font(r'Addon\Police\ColderWeather-Regular.ttf', board_init().get_height()//20)
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