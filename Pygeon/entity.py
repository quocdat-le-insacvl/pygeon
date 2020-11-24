import pygame
class Entity():
    def __init__(self,pos_x,pos_y,img,name,which_type,hitbox):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.img = img
        self.name = name
        self.which_type = which_type
        self.center = [pos_x + img.get_width()//2,pos_y + img.get_height()//2]
        self.rect = pygame.Rect(pos_x,pos_y,img.get_width(),img.get_height())
        self.hitbox = hitbox
    def update_center(self):
        self.center = [self.pos_x + self.img.get_width()//2,self.pos_y + self.img.get_height()//2]