import pygame
from settings import screen,police,color


class Lvl_up_mecanic():

    def choice(self):
        screen_S=self.__screenSave()
        text=police.Outrun_future.render("Level up !",False,color.RED)
        text2=police.Outrun_future.render("Choose skill or points",False,color.RED)
        board=pygame.transform.scale(pygame.image.load(r"Addon\Menu\UI board Small  parchment.png"),(text2.get_width()+50,text.get_height()*4))
        excl=pygame.transform.scale(pygame.image.load(r"Addon\Menu\Exclamation_Red.png"),(board.get_width()//5,board.get_height()//5))
        board.blit(text,(board.get_width()//2-text.get_width()//2,10))
        board.blit(text2,(board.get_width()//2-text2.get_width()//2,text.get_height()+20))
        excl_rect=board.blit(excl,(board.get_width()//2-excl.get_width()*2,text.get_height()*2+30))
        screen.screen.blit(board,(screen.LONGUEUR//2-board.get_width()//2,screen.LARGEUR//2-board.get_height()//2))
        pygame.display.flip()
        running=True
        while running:
            for events in pygame.event.get():
                if all([events.type==pygame.MOUSEBUTTONUP,excl_rect.collidepoint((pygame.mouse.get_pos()[0]-screen.LONGUEUR//2+board.get_width()//2,pygame.mouse.get_pos()[1]-screen.LARGEUR//2+board.get_height()//2))]):
                    print("ok\n")
                    screen.screen.blit(screen_S,(0,0))
                    pygame.display.flip()
                    running=False
                elif events.type==pygame.QUIT:
                    pygame.quit()
                    running=False


    def __screenSave(self):
        screensave=pygame.Surface(screen.WINDOWS_SIZE)
        screensave.blit(screen.screen,(0,0))
        return screensave