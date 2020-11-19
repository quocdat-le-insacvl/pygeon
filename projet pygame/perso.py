import pygame

class Perso(pygame.sprite.Sprite):


    def __init__(self):
        super().__init__()
        self.v=0
        self.o=0
        self.t=0

    def animation(self,screen):
        if(pygame.time.get_ticks()>=self.t):
            self.v=(self.v+200)%400
            self.t+=750
        image=self.image.subsurface((self.o,self.v,200,200))
        screen.blit(image, (self.x,self.y))
