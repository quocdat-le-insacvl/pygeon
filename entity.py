import pygame
from settings.load_img import pixel_red
from settings.screen import *
from settings.color import *
class Entity():

    def __init__(self,pos_x,pos_y,img,name,which_type,animation_dict = None,talking=None,size=(0,0)):
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
    def update_center(self):
        self.center = [self.pos_x + self.img.get_width()//2,self.pos_y + self.img.get_height()//2]
    def animate(self):
        if self.type_animation != "" and self.animation_dict != None :
            animation = self.animation_dict[self.type_animation]
            self.frame += 0.05
            if self.frame > len(animation)+1:
                self.frame=1
            #self.display = pygame.Surface((animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"].get_width(),animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"].get_height()))
            self.display.fill((0,0,0))
            self.display.blit(animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"],(self.img.get_width()//2-animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"].get_width()//2+150-int(self.img.get_width()//2),self.img.get_height()-animation[ self.nom + "_" + self.type_animation + "_" + str(int(self.frame)) + ".png"].get_height()+300-self.img.get_height()))
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
            

WIDTH = screen.get_width()     
HEIGHT = screen.get_height()
MINIMAP_SCALE = 300
class Minimap:
    def __init__(self, game, display_with_nature):
        self.game = game
        self.player = self.game.player
        self.display_with_nature = display_with_nature
        self.screen = screen
        self.map = self.game.map
        self.map_height = len(self.map)
        self.map_width = len(self.map[0])
        self.TOP_LEFT_X = WIDTH - MINIMAP_SCALE
        self.TOP_LEFT_Y = HEIGHT - MINIMAP_SCALE
        self.surface = pygame.Surface((MINIMAP_SCALE,  MINIMAP_SCALE))
        self.surface.set_alpha(50)                # alpha level
        self.surface.fill(BLUE)
        SCALE = 10*MINIMAP_SCALE
        self.scale = SCALE / 2
        self.rect = pygame.Rect(0, 0, SCALE, SCALE)
        self.size_big_map = self.display_with_nature.get_size()

    def draw_minimap(self):
        self.draw_surface()
        # self.draw_white_square()
        #self.draw_dot_pos(self.game.player.pos_x, self.game.player.pos_y, RED)
        # for mob in self.game.mobs:
        #     self.draw_dot_pos(mob.pos, GREEN)

    def draw_surface(self):
        """ 
        L'algo de cette partie est le suivant : utiliser pygame.transform.scale pour minimiser 
        la grande carte a une petite carte (minimap) puis blit sur screen 
        # Il reste des problemes a regler : self.map_sp est parfois dehors le surface display_with_nature
        # a cause de method  subsurface() 
        === > Probleme resolu!
        """
        ## Set center of Rect 
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
            
        try: 
            self.map_sp = self.display_with_nature.subsurface(self.rect)
        except:
            pass
        minimap = pygame.transform.scale(self.map_sp, (MINIMAP_SCALE, MINIMAP_SCALE))
        self.screen.blit(minimap , (self.TOP_LEFT_X, self.TOP_LEFT_Y))

    # draw position of player , or monster
    def draw_dot_pos(self, pos_x, pos_y, color):
        X = self.TOP_LEFT_X + pos_x / (self.map_width * 190) * MINIMAP_SCALE
        Y = self.TOP_LEFT_Y + pos_y / (self.map_height * 190) * MINIMAP_SCALE
        pygame.draw.circle(self.screen, color, (X, Y), radius=6, width=0)
