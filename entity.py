import pygame
from settings.load_img import pixel_red
class Entity():

    def __init__(self,pos_x,pos_y,img,name,which_type,animation_dict = None,talking=None,size=(0,0),decalage = [0,0]):
        if size == (0,0):
            size = (img.get_width(),img.get_height())
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.img = img
        self.name = name
        self.type = which_type
        self.nom = name
        self.center = [pos_x + img.get_width()//2,pos_y + img.get_height()//2]
        self.rect = pygame.Rect(pos_x,pos_y,self.img.get_width(),self.img.get_height())
        self.display = pygame.Surface(size)
        self.display.set_colorkey((0,0,0))
        self.display.blit(self.img,(0,0))
        self.animation_dict = animation_dict
        self.frame = 1
        self.talking = talking
        self.interaction = [[self.pos_x,self.pos_y],[self.pos_x,self.pos_y],[self.pos_x,self.pos_y]]
        self.type_animation = "idle"
        self.decalage_display = decalage
    def update_center(self):
        self.center = [self.pos_x + self.img.get_width()//2,self.pos_y + self.img.get_height()//2]
    def animate(self):
        if self.type_animation != "" and self.animation_dict != None :
            animation = self.animation_dict[self.type_animation]
            self.frame += 0.05
            if self.frame > len(animation)+1:
                self.frame=1
            self.display = pygame.Surface((300,300))
            self.display.set_colorkey((0,0,0))
            self.display.fill((0,0,0))
            self.display.blit(animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"],(self.img.get_width()//2-animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"].get_width()//2+150-int(self.img.get_width()//2)+self.decalage_display[0],self.img.get_height()-animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"].get_height()+300-self.img.get_height()+self.decalage_display[1]))
    def update_interact(self):
        self.interaction[0] = [ self.pos_x + 95 - pixel_red.get_width()//2 + self.img.get_width()//2 , 47+self.pos_y+self.img.get_height()-pixel_red.get_height()//1.5]
        self.interaction[1] = [ self.pos_x - pixel_red.get_width()//2 + self.img.get_width()//2 , 47*2+self.pos_y+self.img.get_height()-pixel_red.get_height()//1.5]
        self.interaction[2] = [ self.pos_x - 95 - pixel_red.get_width()//2 + self.img.get_width()//2 , 47+self.pos_y+self.img.get_height()-pixel_red.get_height()//1.5]
    def animate_map(self):
        if self.type_animation != "" and self.animation_dict != None :
            animation = self.animation_dict[self.type_animation]
            self.frame += 0.05
            if self.frame > len(animation)+1:
                self.frame=1
            #self.display = pygame.Surface((animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"].get_width(),animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"].get_height()))
            self.display.fill((0,0,0))
            self.display.blit(animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"],(0,0))