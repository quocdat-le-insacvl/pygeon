import os
import pygame
from fighter import Fighter
from math import trunc
fighter=Fighter()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (20,20)

class Interface(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.resolution=[1200,950]
        self.screen = pygame.display.set_mode((self.resolution[0],self.resolution[1]))
        self.case=0
        self.listCase=[]
        self.ini_state=0
        # self.background = pygame.image.load('assets/grass.jpg')


    def basic_affichage(self):
        pygame.display.set_caption("projet fighter")
        # self.screen.blit(self.background, (0,-200))
    
    def generer(self):#génère la map et les positions des personnagese en fonction de la taille de l'écran
        f=open("./map.txt","r")
        l=[[i for i in ligne] for ligne in f]
        if self.case==0:
            self.case=pygame.transform.scale(pygame.image.load("./case.png"),(round(self.resolution[0]/len(l)-1),round(self.resolution[1]/len(l)-1)))
        num_ligne=0
        for n in l:
            if self.ini_state==0:
                self.listCase.append([])
            num_case=0
            #initialise les cases
            for i in n:
                x=round((num_case-num_ligne)*self.case.get_width()/2+self.resolution[0]/2-self.case.get_width()/2)
                y=round((num_case+num_ligne)*self.case.get_height()/4+self.resolution[1]/2-self.case.get_height()/4)
                if i=='W' and self.ini_state==0:
                    self.listCase[num_ligne].append(self.screen.blit(self.case,(x,y)))
                elif i=='W':
                    self.screen.blit(self.case,(x+self.resolution[0]/5,y))
                num_case+=1
            num_ligne+=1
        print(self.listCase)
        self.ini_state=1
        #place le joueur sur la nouvelle map
        fighter.x=self.listCase[1][1].centerx 
        fighter.y=self.listCase[1][1].centery
        f.close()
    """
    def coord_block(self,xy):
        #print(xy[0], 'et', xy[1])
        return (trunc((xy[0]-self.resolution[0]/2+self.case.get_width()*(len(self.listCase))/2)/self.case.get_width()),trunc(xy[1]/(self.case.get_height()/1.8)))
    
    def affichage_sort(self):
        #permet d'afficher une tache rouge pour indiquer la surface du sort
        running=True
        r=pygame.transform.scale(pygame.image.load("./case_sort.png"),(round(self.resolution[0]/7),round(self.resolution[1]/7)))
        # self.generer()
        pos=0
        carre=0
        while running:
            print(self.resolution[0]/2-self.case.get_width()*(len(self.listCase))/2)
            if pygame.mouse.get_pos()[0]>self.resolution[0]/2-self.case.get_width()*(len(self.listCase))/2 :
                carre=self.screen.blit(r, (self.listCase[self.coord_block(pygame.mouse.get_pos())[1]][self.coord_block(pygame.mouse.get_pos())[0]].x,self.listCase[self.coord_block(pygame.mouse.get_pos())[1]][self.coord_block(pygame.mouse.get_pos())[0]].y))
            if pos!=carre:
                o=0
                # self.generer()
            pos=carre
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONUP:
                    running=False
                if event.type==pygame.QUIT:
                    running=False
                    pygame.quit()
    """