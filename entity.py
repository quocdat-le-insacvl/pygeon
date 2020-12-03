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

        self.display = pygame.Surface((img.get_width(),img.get_height()))
        self.display.set_colorkey((0,0,0))
        self.display.blit(img,(0,0))
        self.hitbox = hitbox
    def update_center(self):
        self.center = [self.pos_x + self.img.get_width()//2,self.pos_y + self.img.get_height()//2]

tavern_img = pygame.image.load(r'tavern_1.png').convert_alpha()
tavern_img = pygame.transform.scale(tavern_img,(2*tavern_img.get_width(),2*tavern_img.get_height()))
tavern_2_img = pygame.image.load(r'C:\Users\Antho\Desktop\Pygeon\pygeon\Addon\tavern_2.png').convert_alpha()
tavern_2_img = pygame.transform.scale(tavern_2_img,(2*tavern_2_img.get_width(),2*tavern_2_img.get_height()))
demon = pygame.image.load(r'Addon\demon_walk\walk_1.png').convert_alpha()
demon = pygame.transform.scale(demon,(10*demon.get_width(),10*demon.get_height()))
vendeur_1 = pygame.image.load(r'C:\Users\Antho\Desktop\Pygeon\pygeon\Addon\seller\seller_1_hide_1.png').convert_alpha()
vendeur_1 = pygame.transform.scale(vendeur_1,(3*vendeur_1.get_width(),3*vendeur_1.get_height()))


entity_1 = Entity(9250-tavern_img.get_width()//2,175-tavern_img.get_height()//2,tavern_img,'Seller','Seller',100)
entity_2 = Entity(9000,1000,demon,'Seller','Seller',100)
entity_3 = Entity(9000,2000,tavern_2_img,'Seller','Build',100)
entity_4 = Entity(9250,485,vendeur_1,'Pierre','Seller',100)

list_entity = []
#list_entity.append(entity_1)
list_entity.append(entity_2)
list_entity.append(entity_3)
list_entity.append(entity_4)