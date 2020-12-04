import pygame
from fighter import Fighter
from math import trunc
fighter=Fighter()


class Interface(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.resolution=[1500,1000]
        self.screen = pygame.display.set_mode((self.resolution[0],self.resolution[1]))
        self.listCase=[]
        # self.background = pygame.image.load('assets/grass.jpg')


    def basic_affichage(self):
        pygame.display.set_caption("projet fighter")
        fighter.update_hp_bar(self.screen)
        # self.screen.blit(self.background, (0,-200))
        pygame.display.flip()
    
    def generer(self):#génère la map et les positions des personnages
        case=pygame.transform.scale(pygame.image.load("./case.png"),(round(self.resolution[0]/7),round(self.resolution[1]/7)))
        f=open("./map.txt","r")
        l=[[i for i in ligne] for ligne in f]
        num_ligne=0
        for n in l:
            self.listCase.append([])
            num_case=0
            #initialise les cases
            for i in n:
                if i=='W':
                    self.listCase[num_ligne].append(self.screen.blit(case,(round(self.resolution[0]/2-case.get_width()*(len(l[0])-1)/2)+case.get_width()*num_case,(case.get_height()/2)*num_ligne)))
                # elif i=='W':
                #     self.listCase[num_ligne].append(self.screen.blit(case,(round(self.resolution[0]/2-case.get_width()*(len(l[0])-1)/2)+case.get_width()*num_case+case.get_width()/2,(case.get_height()/2)*num_ligne)))
                num_case+=1
            num_ligne+=1
        print(self.listCase)
        #place le joueur sur la nouvelle map
        fighter.x=self.listCase[1][1].centerx 
        fighter.y=self.listCase[1][1].centery

    def coord_block(self,xy):
            return (trunc(xy[0]/214),trunc(xy[1]/143))
    
    def affichage_sort(self):
        running=True
        r=pygame.transform.scale(pygame.image.load("./case_sort.png"),(round(self.resolution[0]/7),round(self.resolution[1]/7)))
        while running:
            self.generer()
            self.basic_affichage()
            self.screen.blit(r, (self.listCase[self.coord_block(pygame.mouse.get_pos())[1]][self.coord_block(pygame.mouse.get_pos())[0]].x+1,self.listCase[self.coord_block(pygame.mouse.get_pos())[1]][self.coord_block(pygame.mouse.get_pos())[0]].y))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONUP:
                    running=False
                if event.type==pygame.QUIT:
                    running=False
                    pygame.quit()
                




