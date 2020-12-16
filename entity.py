import pygame
from settings.load_img import pixel_red
from settings.screen import *
from settings.color import *
from settings.load_img import ava_perso
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
        distance = abs(self.pos_x - list_entity[0].center[0]) + abs(self.pos_y - list_entity[0].center[1])
        entity = list_entity[0]
        for i in range(len(list_entity)):
            if abs(self.pos_x - list_entity[i].center[0]) + abs(self.pos_y - list_entity[i].center[1]) < distance:
                distance = abs(self.pos_x - list_entity[i].center[0]) + abs(self.pos_y - list_entity[i].center[1])
                entity = list_entity[i]
        return entity
        """def find_nearest_entity(self,player_rect,list_entity):
        Permet de trouver l'entité dans list_entity la plus proche de player_rect
        return Entity la plus proche de player_rect"""
    
    


WIDTH = screen.get_width()
HEIGHT = screen.get_height()
MINIMAP_SCALE = 300
class Minimap:
    def __init__(self, game, display_with_nature):
        self.game = game
        self.player = self.game.player
        self.display_with_nature = display_with_nature
        self.screen = screen
        self.map = self.game.map.map
        self.map_height = len(self.map)
        self.map_width = len(self.map[0])
        self.TOP_LEFT_X = WIDTH - MINIMAP_SCALE
        self.TOP_LEFT_Y = HEIGHT - MINIMAP_SCALE
        self.surface = pygame.Surface((MINIMAP_SCALE,  MINIMAP_SCALE))
        self.surface.set_alpha(50)                # alpha level
        self.surface.fill(BLUE)
        SCALE = 10*MINIMAP_SCALE
        self.SCALE = SCALE
        self.scale = SCALE / 2
        self.rect = pygame.Rect(0, 0, SCALE, SCALE)
        self.size_big_map = self.display_with_nature.get_size()
        self.zoom_x, self.zoom_y = self.screen.get_size()
        self.rect_zoom = pygame.Rect(0, 0, self.zoom_x * 3, self.zoom_y * 3)
        self.zoom_map = self.display_with_nature.subsurface(self.rect_zoom)

    def draw_minimap(self):
        self.draw_surface()
        self.draw_white_square()
        self.draw_perso()
        #self.draw_dot_pos(self.game.player.pos_x, self.game.player.pos_y, RED)
        # for mob in self.game.mobs:
        #     self.draw_dot_pos(mob.pos, GREEN)

    def draw_white_square(self):
        minimap_rect = pygame.Rect(self.TOP_LEFT_X, self.TOP_LEFT_Y, MINIMAP_SCALE, MINIMAP_SCALE)
        pygame.draw.rect(self.screen, WHITE, minimap_rect, width=3)

    def draw_white_square_zoom(self):
        minimap_rect = pygame.Rect(
            MINIMAP_SCALE, MINIMAP_SCALE, self.zoom_x - MINIMAP_SCALE, self.zoom_y - MINIMAP_SCALE)
        pygame.draw.rect(self.screen, WHITE, minimap_rect, width=3)

    def draw_surface(self):
        """
        L'algo de cette partie est le suivant : utiliser pygame.transform.scale pour minimiser
        la grande carte a une petite carte (minimap) puis blit sur screen
        # Il reste des problemes a regler : self.map_sp est parfois dehors le surface display_with_nature
        # a cause de method  subsurface()
        === > Probleme resolu!
        """

        """ Create les regles pour le Rectangle est toujours dans le surface"""
        if self.player.pos_x - self.scale < 0 :
            self.rect.right = 0
        elif self.player.pos_x + self.scale > self.size_big_map[0] : #width
            self.rect.left = self.size_big_map[0]
        else:
            self.rect.centerx = self.player.pos_x

        if self.player.pos_y - self.scale < 0:
            self.rect.top = 0
        elif self.player.pos_y + self.scale > self.size_big_map[1]:
            self.rect.bottom = self.size_big_map[1]
        else:
            self.rect.centery = self.player.pos_y

        # try pour etre sur que le programme marche toujours bien
        try:
            self.map_sp = self.display_with_nature.subsurface(self.rect)
        except:
            pass
        # self.map_sp.blit(
        #     ava_perso, (self.player.pos_x, self.player.pos_y))
        minimap = pygame.transform.scale(self.map_sp, (MINIMAP_SCALE, MINIMAP_SCALE))
        self.screen.blit(minimap , (self.TOP_LEFT_X, self.TOP_LEFT_Y))


    def zoom_minimap(self):
        # CARRY_SCALE = self.scale
        # self.scale =

        if self.player.pos_x - self.zoom_x < 0:
            self.rect_zoom.right = 0
        elif self.player.pos_x + self.zoom_x > self.size_big_map[0] : #width
            self.rect_zoom.left = self.size_big_map[0]
        else:
            self.rect_zoom.centerx = self.player.pos_x

        if self.player.pos_y - self.zoom_y < 0:
            self.rect_zoom.top = 0
        elif self.player.pos_y + self.zoom_y > self.size_big_map[1]:
            self.rect_zoom.bottom = self.size_big_map[1]
        else:
            self.rect_zoom.centery = self.player.pos_y
        # try pour etre sur que le programme marche toujours bien
        try:
            self.zoom_map = self.display_with_nature.subsurface(self.rect_zoom)
        except:
            pass
        # self.map_sp.blit(
        #     ava_perso, (self.player.pos_x, self.player.pos_y))
        minimap = pygame.transform.scale(
            self.zoom_map, (self.zoom_x - 300, self.zoom_y - 300))
        self.screen.blit(minimap, (300, 300))
        self.draw_white_square_zoom()

    # draw position of player , or monster
    def draw_perso(self):
        # draw the perso au milieu de minimap si pos.rect === pos.perso
        if self.rect.centerx == self.player.pos_x and self.rect.centery == self.player.pos_y:
            self.screen.blit(
                ava_perso, (self.TOP_LEFT_X + MINIMAP_SCALE/2, self.TOP_LEFT_Y + MINIMAP_SCALE / 2))
        # si c'est pas le cas, je calcule pos_player_real par rapport aux le self.rect
        # puis je vais utiliser Theoreme Talet pour trouver la position finale de perso sur le minimap
        else:
            x_real = self.player.pos_x - self.rect.left
            y_real = self.player.pos_y - self.rect.top
            # ==> Talet
            x_mini = x_real / self.rect.width * MINIMAP_SCALE
            y_mini = y_real / self.rect.height * MINIMAP_SCALE
            self.screen.blit(
                ava_perso, (self.TOP_LEFT_X + x_mini, self.TOP_LEFT_Y + y_mini))


class Fog:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        self.screen = screen
        self.fog = pygame.Surface((18000, 10000))
        self.fog.set_alpha(50)                # alpha level
        self.fog.fill(BLACK)

    def update(self):
        pass

    def draw_fog(self):
        self.screen.blit(self.fog, (self.game.center_x, self.game.center_y))
