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
            self.refresh_display()
            if self.nom != None:
                self.display.blit(animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"],(self.img.get_width()//2-animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"].get_width()//2+150-int(self.img.get_width()//2)+self.decalage_display[0],self.img.get_height()-animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"].get_height()+300-self.img.get_height()+self.decalage_display[1]))
            else:
                self.display.blit(animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"],(self.img.get_width()//2-animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"].get_width()//2+150-int(self.img.get_width()//2)+self.decalage_display[0],self.img.get_height()-animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"].get_height()+300-self.img.get_height()+self.decalage_display[1]))

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
            self.refresh_display()
            if self.nom != None:
                self.display.blit(animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"],(0,0))
            else:
                self.display.blit(animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"],(0,0))
    def refresh_display(self):
        self.display.fill((0,0,0))
        self.display.set_colorkey((0,0,0))
    def move_entity(self,mouvement,map,player):
        pixel_mask = pygame.mask.from_surface(pixel_red) 
        if map.collision.__contains__((self.pos_x- pixel_red.get_width()//2+self.img.get_width()//2,self.pos_y-int(pixel_red.get_height()//1.5)+self.img.get_height())):
            map.collision.remove((self.pos_x- pixel_red.get_width()//2+self.img.get_width()//2,self.pos_y-int(pixel_red.get_height()//1.5)+self.img.get_height()))
        if not player.masks.overlap(pixel_mask,((self.pos_x- pixel_red.get_width()//2+self.img.get_width()//2 + mouvement[0])-player.pos_x,self.pos_y-int(pixel_red.get_height()//1.5)+self.img.get_height()+ mouvement[1]-(player.pos_y+130))):
            for x in self.interaction:
                if map.collision_entity.__contains__((int(x[0]),int(x[1]))):
                    map.collision_entity.remove((int(x[0]),int(x[1])))
                map.collision_entity.append((int(x[0])+mouvement[0],int(x[1])+mouvement[1]))
            map.collision.append((self.pos_x- pixel_red.get_width()//2+self.img.get_width()//2+ mouvement[0],self.pos_y-int(pixel_red.get_height()//1.5)+self.img.get_height()+ mouvement[1]))
            self.pos_x += mouvement[0]
            self.pos_y += mouvement[1]
            
        else:
            #collision.remove((self.pos_x+mouvement[0]+20,self.pos_y+mouvement[1]+130))
            map.collision.append((self.pos_x- pixel_red.get_width()//2+self.img.get_width()//2,self.pos_y-int(pixel_red.get_height()//1.5)+self.img.get_height()))
            
        """def move_entity(self,entity,mouvement,collision_entity,collision,pieds_mask,joueurs):
        Permet de décplacer une entité, gère les cases d'intéraction de l'entité + collision avec joueurs, retourne soit l'entité modifié soit l'entité non modifié de mouvement"""
    def find_nearest_entity(self,list_entity):
        distance = abs(self.pos_x - list_entity[0].pos_x) + abs(self.pos_y - list_entity[0].pos_y)
        entity = list_entity[0]
        for i in range(len(list_entity)):
            if abs(self.pos_x - list_entity[i].pos_x) + abs(self.pos_y - list_entity[i].pos_y) < distance:
                distance = abs(self.pos_x - list_entity[i].pos_x) + abs(self.pos_y - list_entity[i].pos_y)
                entity = list_entity[i]
        return entity
        """def find_nearest_entity(self,player_rect,list_entity):
        Permet de trouver l'entité dans list_entity la plus proche de player_rect
        return Entity la plus proche de player_rect"""
    
    