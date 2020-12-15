import pygame
from sorcerer import Sorcerer
#it will be from game import perso
from math import trunc
from settings.screen import screen,WINDOWS_SIZE



class Interface():
    def __init__(self):
        super().__init__()
        self.resolution=WINDOWS_SIZE
        self.screen=screen
        self.backgroung=pygame.transform.scale(pygame.image.load(r"Image\backgroung_combat.png"),self.resolution)
        self.case=0
        self.listCase=[]
        self.ini_state=0
        self.perso=Sorcerer()
        # self.background = pygame.image.load('assets/grass.jpg')


    def basic_affichage(self):
        pygame.display.set_caption("projet fighter")
        screen.blit(self.perso.img,(self.perso.pos_x,self.perso.pos_y))
        # self.screen.blit(self.background, (0,-200))
    
    def generer(self):#génère la map et les positions des personnagese en fonction de la taille de l'écran
        f=open("./map.txt","r")
        l=[[i for i in ligne] for ligne in f]
        if self.case==0:
            self.case=pygame.transform.scale(pygame.image.load(r"Image\case.png"),(self.resolution[0]//len(l)-1,self.resolution[0]//len(l)-1))
        num_ligne=0
        rect=screen.blit(self.case,(self.resolution[0]/2,self.resolution[1]/2))
        """
        for n in l:
            if self.ini_state==0:
                self.listCase.append([])
            num_case=0
            #initialise les cases
            for i in n:
                x=round((num_case-num_ligne)*self.case.get_width()/2+self.resolution[0]/2-self.case.get_width()/2)
                y=round((num_case+num_ligne)*self.case.get_height()/4+self.resolution[1]/2-self.case.get_height()*(len(l)+1)/4)
                if i=='W' and self.ini_state==0:
                    self.listCase[num_ligne].append(pygame.Rect(self.case,(x,y)))
                if i=='W':
                    self.screen.blit(self.case,(x,y))
                num_case+=1
            num_ligne+=1
         self.ini_state=1
        print(self.listCase)

        place le joueur sur la nouvelle map
        fighter.x=self.listCase[1][1].centerx 
        fighter.y=self.listCase[1][1].centery
        f.close()

    def coord_block(self,xy):
        # xy[0]=x et xy[1]=y transforme les positions en positions dans la liste de rec
        print((trunc((((xy[0]-self.case.get_width()/2*(len(self.listCase)-xy[0]/self.case.get_width()*2))/self.case.get_width()/2)+(xy[1]-self.case.get_height()/2)/self.case.get_height()*2)),trunc(-((xy[0]-self.case.get_width()/2*(len(self.listCase)-xy[0]/self.case.get_width()*2))/self.case.get_width()/2)+(xy[1]-self.case.get_height()/2)/self.case.get_height()*2)))
        return(0,0)

    def affichage_sort(self):
        #permet d'afficher une tache rouge pour indiquer la surface du sort
        running=True
        r=pygame.transform.scale(pygame.image.load("./case_sort.png"),(self.case.get_width(),self.case.get_height()))
        pos=0
        carre=0
        while running:
            if pos!=carre:
                if pygame.mouse.get_pos()[0]>=self.case.get_height()/4 :
                    self.generer()
                    carre=self.screen.blit(r, (self.listCase[self.coord_block(pygame.mouse.get_pos())[1]][self.coord_block(pygame.mouse.get_pos())[0]].x,self.listCase[self.coord_block(pygame.mouse.get_pos())[1]][self.coord_block(pygame.mouse.get_pos())[0]].y))
            pos=carre
            carre=self.listCase[self.coord_block(pygame.mouse.get_pos())[1]][self.coord_block(pygame.mouse.get_pos())[0]]
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONUP:
                    running=False
                if event.type==pygame.QUIT:
                    running=False
                    pygame.quit()
   
    def affichage(self):
        rec=pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)
        r=pygame.transform.scale(pygame.image.load("./case_sort.png"),(self.case.get_width(),self.case.get_height()))
        running=True
        while running:
            for n in self.listCase:
                for i in n:
                    if i.collidepoint(pygame.mouse.get_pos()):
                        self.generer()
                        self.screen.blit(r,(i.x,i.y))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONUP:
                    running=False
                if event.type==pygame.QUIT:
                    running=False
                    pygame.quit()
    """