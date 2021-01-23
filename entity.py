import pygame
from settings.load_img import pixel_red, light_mask, collide_map, collide_monster
from settings.screen import *
from settings.color import *
from settings.load_img import ava_perso
from pygame.locals import *


class Entity():

    def __init__(self, pos_x, pos_y, img, name, which_type, animation_dict=None, talking=None, size=(0, 0), decalage=[0, 0], size_collide_box=1,donjon=False):
        if size == (0, 0):
            size = (img.get_width(), img.get_height())
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.img = img
        self.name = "Monstre"
        self.type = which_type
        self.nom = name
        self.center = [pos_x + img.get_width()//2, pos_y + img.get_height()//2]
        self.rect = pygame.Rect(
            pos_x, pos_y, self.img.get_width(), self.img.get_height())
        self.display = pygame.Surface(size).convert_alpha()
        self.display.set_colorkey((0, 0, 0))
        self.display.blit(self.img, (0, 0))
        self.animation_dict = animation_dict
        self.frame = 1
        self.talking = talking
        self.interaction = [[self.pos_x, self.pos_y], [self.pos_x, self.pos_y], [
            self.pos_x, self.pos_y], [self.pos_x, self.pos_y]]
        self.type_animation = "idle"
        self.decalage = decalage
        self.avata = pygame.transform.scale(img, (30, 30))
        self.is_hidden = True
        self.seen = False
        self.last_know_pos = (0, 0)
        self.shadow = img
        self.collide_box = Collide_box(size_collide_box,donjon=donjon)

    
    def update_center(self):
        self.center = [self.pos_x + self.img.get_width()//2,
                       self.pos_y + self.img.get_height()//2]

    def trouver_case(self,liste_case):
        for x in liste_case:
            if x.in_case == self:
                return x
        return liste_case[0]
    def animate_attack(self):
        one_complete = False
        if self.type_animation != "" and self.animation_dict != None:
            animation = self.animation_dict[self.type_animation]
            self.frame += 0.17
            if self.frame > len(animation)+1:
                self.frame = 1
                one_complete=True
            self.refresh_display()
            self.display.blit(animation[self.type_animation + "_" + str(int(self.frame)) + ".png"], (self.img.get_width()//2-animation[self.type_animation + "_" + str(int(self.frame)) + ".png"].get_width()//2+150-int(
                self.img.get_width()//2)+self.decalage[0], self.img.get_height()-animation[self.type_animation + "_" + str(int(self.frame)) + ".png"].get_height()+300-self.img.get_height()+self.decalage[1]))
        else:
            self.display.blit(self.img, (0, 0))
        return one_complete
            #self.display.blit(animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"],(150-animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"].get_width()//2,self.img.get_height()-animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"].get_height()+300-self.img.get_height()+self.decalage_display[1]))
    def animate(self):
        one_complete = False
        if self.type_animation != "" and self.animation_dict != None:
            animation = self.animation_dict[self.type_animation]
            self.frame += 0.08
            if self.frame > len(animation)+1:
                self.frame = 1
                one_complete=True
            self.refresh_display()
            self.display.blit(animation[self.type_animation + "_" + str(int(self.frame)) + ".png"], (self.img.get_width()//2-animation[self.type_animation + "_" + str(int(self.frame)) + ".png"].get_width()//2+150-int(
                self.img.get_width()//2)+self.decalage[0], self.img.get_height()-animation[self.type_animation + "_" + str(int(self.frame)) + ".png"].get_height()+300-self.img.get_height()+self.decalage[1]))
            #print(f'Taille de l image ({self.img.get_width()},{self.img.get_height()})\n')    
        
        else:
             
            self.display.blit(self.img, (0, 0))
        return one_complete
            #self.display.blit(animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"],(150-animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"].get_width()//2,self.img.get_height()-animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"].get_height()+300-self.img.get_height()+self.decalage_display[1]))
    def animate_map(self, flip=False,scale=None):
        if self.type_animation != "" and self.animation_dict != None:
            animation = self.animation_dict[self.type_animation]
            #self.display.blit(animation[ self.type_animation + "_" + str(int(self.frame)) + ".png"],(0,0))
            self.frame += 0.05
            if self.frame > len(animation)+1:
                self.frame = 1
            if not flip:
                self.img = animation[self.type_animation +
                                     "_" + str(int(self.frame)) + ".png"]
            else:
                
                self.img = pygame.transform.flip(
                    animation[self.type_animation + "_" + str(int(self.frame)) + ".png"], True, False)
                
                self.img.set_colorkey(BLACK)
            if scale != None:
                    self.img = pygame.transform.scale(self.img,scale)

    def refresh_display(self):
        self.display.fill((0, 0, 0))
        self.display.set_colorkey((0, 0, 0))

    def move_entity(self, mouvement, player):
        if not player.masks.overlap(self.collide_box.mask, ((self.collide_box.pos_x + mouvement[0])-player.pos_x, (self.collide_box.pos_y + mouvement[1])-(player.pos_y+130))):
            self.pos_x += mouvement[0]
            self.pos_y += mouvement[1]
            self.update_pos_collide()
        """def move_entity(self,entity,mouvement,collision_entity,collision,pieds_mask,joueurs):
        Permet de décplacer une entité, gère les cases d'intéraction de l'entité + collision avec joueurs, retourne soit l'entité modifié soit l'entité non modifié de mouvement"""

    def find_nearest_entity(self, list_entity):
        distance = abs(
            self.pos_x - list_entity[0].center[0]) + abs(self.pos_y - list_entity[0].center[1])
        entity = list_entity[0]
        for i in range(len(list_entity)):
            if abs(self.pos_x - list_entity[i].center[0]) + abs(self.pos_y - list_entity[i].center[1]) < distance:
                distance = abs(
                    self.pos_x - list_entity[i].center[0]) + abs(self.pos_y - list_entity[i].center[1])
                entity = list_entity[i]
        return entity
        """def find_nearest_entity(self,player_rect,list_entity):
        Permet de trouver l'entité dans list_entity la plus proche de player_rect
        return Entity la plus proche de player_rect"""

    def update_pos_collide(self):
        self.collide_box.pos_x = int(
            self.pos_x - self.collide_box.img_collide.get_width()//2 + self.img.get_width()//2)
        self.collide_box.pos_y = int(
            self.pos_y + self.img.get_height() - self.collide_box.img_collide.get_height()//2)


class Chest(Entity):
    def __init__(self, pos_x, pos_y, img, name, which_type, inventaire):
        super().__init__(pos_x, pos_y, img, name, which_type,size_collide_box=2)
        self.inventaire = inventaire
        
    def loot_chest(self):
        self.inventaire.loot_chest()





class Collide_box():
    def __init__(self, size=1,donjon=False):
        self.size = size
        if donjon:
            self.img_collide = pygame.transform.scale(collide_monster, (60,30))
        else:
            self.img_collide = pygame.transform.scale(
                collide_monster, (190*self.size*2, 190*self.size))
        self.img_collide.set_colorkey(WHITE)
        self.mask = pygame.mask.from_surface(self.img_collide)
        self.pos_x = 0
        self.pos_y = 0


class ChatBox:
    def __init__(self, game):
        self.game = game
        self.surface = pygame.Surface((400, 320)).convert()
        self.surface.fill((200, 200, 200))
        self.rect = self.surface.get_rect()
        self.rect.bottomleft = (0, self.game.screen.get_height())
        self.font = pygame.font.Font(None, 24)
        self.log = []
        # self.COLOR_INACTIVE = pygame.Color("lightskyblue3")
        # self.COLOR_ACTIVE = pygame.Color((255, 255, 255))
        # self.active = False
        self.input_box = InputBox(
            self, 0, self.game.screen.get_height() - 64, 400, 32)
        # Position beginning to print the log
        self.y_start = self.game.screen.get_height() - 64 - 32

    def update(self):
        self.input_box.update()

    def draw(self):
        self.game.screen.blit(self.surface, self.rect,
                              special_flags=BLEND_MULT)
        self.print_log()
        self.input_box.draw(self.game.screen)

    def handle_event(self, event):
        active = self.input_box.handle_event(event)
        return active

    def print_log(self):
        # print(self.log)
        x = 5
        y = self.y_start
        sp = max(0, len(self.log) - 8)
        offset = min(self.input_box.camera, sp)
        for i in range(offset, len(self.log)):
            # type(text) == str
            # print(self.log[i])
            if type(self.log[i]) == tuple:
                if self.log[i][0] == "combat":
                    txt_surface = self.font.render(self.log[i][1], True, (255, 0, 0))
                if self.log[i][0] == "info":
                    txt_surface = self.font.render(self.log[i][1], True, (255, 255, 255))
            else:
                txt_surface = self.font.render(self.log[i], True, (255, 255, 255))
            self.game.screen.blit(txt_surface, (x, y))
            y -= 25
            if y < self.rect.top:
                break

    def write_log(self, text):
        self.log.insert(0, text)
        self.input_box.camera = 0


class InputBox:

    def __init__(self, chat_box, x, y, w, h, text='Chat here ...'):
        self.chat_box = chat_box
        self.COLOR_INACTIVE = pygame.Color((150, 150, 150))
        self.COLOR_ACTIVE = pygame.Color((255, 255, 255))
        self.FONT = pygame.font.Font(None, 25)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
        self.first = True
        self.camera = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.text = ""
                self.active = not self.active
                if self.first:
                    self.first = False
                    self.text = ''
            else:
                self.active = False
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_RETURN:
                    self.chat_box.log.insert(0, self.text)
                    self.text = ''
                    self.camera = 0
                elif event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.FONT.render(
                    self.text, True, self.color)
        if not self.first and not self.active:
            self.text = "Use mouse's wheel to scroll!!!!"
            self.txt_surface = self.FONT.render(
                self.text, True, self.color)
        # Mouse wheel
        if event.type == MOUSEWHEEL:
            pos = pygame.mouse.get_pos()
            if 0 < pos[0] < self.chat_box.surface.get_width() and self.chat_box.game.screen.get_height() > pos[1] > self.chat_box.game.screen.get_height() - self.chat_box.surface.get_height():
                self.camera += event.y
                self.camera = 0 if self.camera < 0 else self.camera

        return self.active

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+10))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class NPC(Entity):
    def __init__(self,message,quest=None,pos_x=0,pos_y=0,img=None,name=""):
        Entity.__init__(self, pos_x, pos_y, img, name, "NPC")
        self.message = message
        self.quest = quest
        self.update_pos_collide()