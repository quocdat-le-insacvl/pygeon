import pygame
from settings.load_img import pixel_red, light_mask,collide_map,collide_monster
from settings.screen import *
from settings.color import *
from settings.load_img import ava_perso
class Entity():

    def __init__(self,pos_x,pos_y,img,name,which_type,animation_dict = None,talking=None,size=(0,0),decalage = [0,0],size_collide_box=1):
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
        self.display = pygame.Surface(size).convert_alpha()
        self.display.set_colorkey((0,0,0))
        self.display.blit(self.img,(0,0))
        self.animation_dict = animation_dict
        self.frame = 1
        self.talking = talking
        self.interaction = [[self.pos_x,self.pos_y],[self.pos_x,self.pos_y],[self.pos_x,self.pos_y],[self.pos_x,self.pos_y]]
        self.type_animation = "idle"
        self.decalage = decalage
        self.avata = pygame.transform.scale(img, (30, 30))
        self.is_hidden = True
        self.seen = False
        self.last_know_pos = (0, 0)
        self.shadow = img
        self.collide_box = Collide_box(size_collide_box)
    def update_center(self):
        self.center = [self.pos_x + self.img.get_width()//2,self.pos_y + self.img.get_height()//2]
    def animate(self):
        if self.type_animation != "" and self.animation_dict != None :
            animation = self.animation_dict[self.type_animation]
            self.frame += 0.05
            if self.frame > len(animation)+1:
                self.frame=1
            self.refresh_display()
            self.display.blit(animation[self.type_animation + "_" + str(int(self.frame)) + ".png"],(self.img.get_width()//2-animation[self.type_animation + "_" + str(int(self.frame)) + ".png"].get_width()//2+150-int(self.img.get_width()//2)+self.decalage[0],self.img.get_height()-animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"].get_height()+300-self.img.get_height()+self.decalage[1]))
            #self.display.blit(animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"],(150-animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"].get_width()//2,self.img.get_height()-animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"].get_height()+300-self.img.get_height()+self.decalage_display[1]))
    def animate_map(self,flip=False):
        if self.type_animation != "" and self.animation_dict != None :
            animation = self.animation_dict[self.type_animation]
                #self.display.blit(animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"],(0,0))
            self.frame += 0.05
            if self.frame > len(animation)+1:
                self.frame=1
            if not flip:
                self.img = animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"]
            else:
                self.img = pygame.transform.flip(animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"],True,False)
                self.img.set_colorkey(BLACK)
    def refresh_display(self):
        self.display.fill((0,0,0))
        self.display.set_colorkey((0,0,0))
    def move_entity(self,mouvement,player):
        if not player.masks.overlap(self.collide_box.mask,((self.collide_box.pos_x + mouvement[0])-player.pos_x,(self.collide_box.pos_y+ mouvement[1])-(player.pos_y+130))):
            self.pos_x += mouvement[0]
            self.pos_y += mouvement[1]
            self.update_pos_collide()
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
    def update_pos_collide(self):
        self.collide_box.pos_x = int ( self.pos_x - self.collide_box.img_collide.get_width()//2 + self.img.get_width()//2 )
        self.collide_box.pos_y = int ( self.pos_y + self.img.get_height() - self.collide_box.img_collide.get_height()//2)
class Chest(Entity):
    def __init__(self,pos_x,pos_y,img,name,which_type,inventaire):
        super().__init__(pos_x,pos_y,img,name,which_type)
        self.inventaire = inventaire
        
    def loot_chest(self):
        self.inventaire.loot_chest()

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
        self.rect_zoom = pygame.Rect(
            0, 0, (self.zoom_x-MINIMAP_SCALE) * 4, (self.zoom_y-MINIMAP_SCALE) * 4)
        self.zoom_map = self.display_with_nature.subsurface(self.rect_zoom)
        self.zoom_map_fog = self.game.fog.surface.subsurface(self.rect_zoom)
        # Screen_Square in minimap
        self.mini_screen_width = self.zoom_x / self.rect.width * MINIMAP_SCALE
        self.mini_screen_height = self.zoom_y / self.rect.height * MINIMAP_SCALE
        self.mini_screen_rect = pygame.Rect(
            0, 0, self.mini_screen_width, self.mini_screen_height)

    def draw_minimap(self):
        self.draw_surface()
        self.draw_white_square()
        self.check_entity()
        self.draw_entity(self.player, True)
        self.screen_square()

    def draw_white_square(self):
        minimap_rect = pygame.Rect(
            self.TOP_LEFT_X, self.TOP_LEFT_Y, MINIMAP_SCALE, MINIMAP_SCALE)
        pygame.draw.rect(self.screen, WHITE, minimap_rect, width=3)

    def draw_white_square_zoom(self):
        minimap_rect = pygame.Rect(
            MINIMAP_SCALE / 2, MINIMAP_SCALE * 3/4, self.zoom_x - MINIMAP_SCALE, self.zoom_y - MINIMAP_SCALE)
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
        if self.player.pos_x - self.scale < 0:
            self.rect.right = 0
        elif self.player.pos_x + self.scale > self.size_big_map[0]:  # width
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
            self.map_sp_fog = self.game.fog.surface.subsurface(self.rect)
        except:
            pass
        
        # self.map_sp.blit(
        #     ava_perso, (self.player.pos_x, self.player.pos_y))
        minimap = pygame.transform.scale(self.map_sp, (MINIMAP_SCALE, MINIMAP_SCALE))
        self.screen.blit(minimap, (self.TOP_LEFT_X, self.TOP_LEFT_Y))
        minimap_fog = pygame.transform.scale(self.map_sp_fog, (MINIMAP_SCALE, MINIMAP_SCALE))
        self.screen.blit(minimap_fog, (self.TOP_LEFT_X, self.TOP_LEFT_Y), special_flags=pygame.BLEND_MULT)

    def zoom_minimap(self):
        if self.player.pos_x - self.zoom_x < 0:
            self.rect_zoom.right = 0
        elif self.player.pos_x + self.zoom_x > self.size_big_map[0]:  # width
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
            self.zoom_map_fog = self.game.fog.surface.subsurface(self.rect_zoom)
        except:
            pass
        minimap = pygame.transform.scale(self.zoom_map, (self.zoom_x - MINIMAP_SCALE, self.zoom_y - MINIMAP_SCALE))
        self.screen.blit(minimap, (MINIMAP_SCALE / 2, MINIMAP_SCALE * 3/4))
        minimap_fog = pygame.transform.scale(self.zoom_map_fog, (self.zoom_x - MINIMAP_SCALE, self.zoom_y - MINIMAP_SCALE))
        self.screen.blit(minimap_fog, (MINIMAP_SCALE/2, MINIMAP_SCALE * 3/4), special_flags=pygame.BLEND_MULT)
        self.draw_white_square_zoom()
        # Not work proprely now
        # self.check_entity_zoom()
       # self.zoom_draw_perso()

    # draw position of player or show monsters, NPCs in minimaps
    def draw_entity(self, entity, real):
        if real : 
            x_real = entity.pos_x - self.rect.left
            y_real = entity.pos_y - self.rect.top
            x_mini = x_real / self.rect.width * MINIMAP_SCALE
            y_mini = y_real / self.rect.height * MINIMAP_SCALE
            self.screen.blit(entity.avata, (self.TOP_LEFT_X +
                                            x_mini, self.TOP_LEFT_Y + y_mini))
        else:
            x_real = entity.last_know_pos[0] - self.rect.left
            y_real = entity.last_know_pos[1] - self.rect.top
            x_mini = x_real / self.rect.width * MINIMAP_SCALE
            y_mini = y_real / self.rect.height * MINIMAP_SCALE
            mini_shadow = pygame.transform.scale(entity.shadow, (30, 30))
            self.screen.blit(mini_shadow, (self.TOP_LEFT_X +
                                            x_mini, self.TOP_LEFT_Y + y_mini))

    def draw_entity_zoom(self, entity):
        x_real = entity.pos_x - self.rect.left
        y_real = entity.pos_y - self.rect.top
        x_mini = x_real / self.rect.width * (self.zoom_x - MINIMAP_SCALE)
        y_mini = y_real / self.rect.height * (self.zoom_y - MINIMAP_SCALE)
        bigger_ava = pygame.transform.scale(entity.avata, (50, 50))
        self.screen.blit(bigger_ava, (MINIMAP_SCALE/2 +
                                      x_mini, MINIMAP_SCALE * 3/4 + y_mini))
        
    # Verify if a monster in the view of the player => draw it on minimap
    def check_entity(self):
        for entity in self.game.list_mooving_entity:
            # Check color , it's mean, if the monster is in the fog, he is hidden
            if not entity.is_hidden:            
                # Check position
                if self.rect.left < entity.pos_x < self.rect.right and self.rect.top < entity.pos_y < self.rect.bottom:
                    self.draw_entity(entity, True)
                                    
            elif entity.seen:
                self.draw_entity(entity, False)


    def check_entity_zoom(self):
        for entity in self.game.list_mooving_entity:
            if self.rect.left < entity.pos_x < self.rect.right and self.rect.top < entity.pos_y < self.rect.bottom:
                self.draw_entity_zoom(entity)
            


    # Not nessary for this moment
    def screen_square(self):
        # print(self.game.center_x, self.game.center_y)
        # print(self.player.pos_x, self.player.pos_y)
        x_real = self.player.pos_x - self.rect.left
        y_real = self.player.pos_y - self.rect.top
        x_mini = x_real / self.rect.width * MINIMAP_SCALE
        y_mini = y_real / self.rect.height * MINIMAP_SCALE
        self.mini_screen_rect.center = (x_mini + self.TOP_LEFT_X, y_mini + self.TOP_LEFT_Y)
        # print(self.mini_screen_rect)
        pygame.draw.rect(self.screen, WHITE, self.mini_screen_rect, width=1)

    # Not work in this moment
    def zoom_draw_perso(self):
        x_real = self.player.pos_x - self.rect_zoom.left
        y_real = self.player.pos_y - self.rect_zoom.top
        # ==> Talet
        x_mini = x_real / self.rect_zoom.width * (self.zoom_x - MINIMAP_SCALE)
        y_mini = y_real / self.rect_zoom.height * (self.zoom_y - MINIMAP_SCALE)
        self.screen.blit(
            ava_perso, (MINIMAP_SCALE + x_mini, MINIMAP_SCALE + y_mini))

    # 

class Fog:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        self.screen = screen
        self.surface = pygame.Surface(self.game.map.display.get_size()).convert()
        self.surface.fill(NIGHT_COLOR)
        # self.surface.set_colorkey(BLACK)
        self.light_image = light_mask
        self.light_image = pygame.transform.scale(
            self.light_image, LIGHT_RADIUS)
        self.light_rect = self.light_image.get_rect()

    def draw_fog(self):
        self.light_rect.center = (self.player.pos_x+self.player.img.get_width()//2, self.player.pos_y+self.player.img.get_height()//2)
        self.surface.blit(self.light_image, self.light_rect)

class Collide_box():
    def __init__(self,size=1):
        self.size = size
        self.img_collide = pygame.transform.scale(collide_monster,(190*self.size*2,190*self.size))
        self.img_collide.set_colorkey(WHITE)
        self.mask = pygame.mask.from_surface(self.img_collide)
        self.pos_x = 0
        self.pos_y = 0
    