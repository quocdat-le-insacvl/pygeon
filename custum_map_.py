import pygame
import pygame
from math import trunc
import pygame as pg
from pygame.locals import *
from fonction import *
from settings.screen import *
from settings.color import *
from settings.load_img import *
from settings.police import *
from fonction import *
center_x = 0
center_y = 0

click = False




TILESIZE = 48
TAILLE_X = 75
TAILLE_Y = 75
LONGUEUR = TILESIZE * TAILLE_X
LARGEUR = TILESIZE * TAILLE_Y


GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (140, 140, 140)

pg.init()
clock = pg.time.Clock()
global collide_map
collide_map = pygame.transform.scale(collide_map,(TILESIZE*2,TILESIZE))
collide_map.set_colorkey(WHITE)
collide_map_mask = pygame.mask.from_surface(collide_map)
mouse_surface = pygame.Surface((1,1))
mouse_surface.fill(RED)
mouse_mask = pygame.mask.from_surface(mouse_surface)
road = pygame.transform.scale(road,(TILESIZE*2,TILESIZE))
dict_case = dict()
dict_case['1'] = collide_map
dict_case['2'] = road

class Map_editor:
    def __init__(self, Taille_x, Taille_y):
        self.taille_x = Taille_x
        self.taille_y = Taille_y
        self.LONGUEUR = Taille_x * TILESIZE
        self.LARGEUR = Taille_y * TILESIZE
        self.walls = []
        self.map = [[]]
        self.case_select = '1'
        self.case_collide = []
        self.cord_collide = []
        self.display = pygame.Surface((max(Taille_x,Taille_y)*2*TILESIZE,(max(Taille_x,Taille_y)*2*TILESIZE)))
        self.display.fill(BURGUNDY)
        self.display.set_colorkey(BURGUNDY)
        self.camera_x = -self.display.get_width()//2 + screen.get_width()//2
        self.camera_y = -self.display.get_height()//2 + screen.get_height()//2
        self.running = True
        self.click = False
    def draw(self):
        global road
        road = pygame.transform.scale(road,(TILESIZE*2,TILESIZE))
        road.set_colorkey(BURGUNDY)
        for wall in self.walls:
            self.display.blit(collide_map,(standard_vec_into_iso(wall[0]*TILESIZE,wall[1]*TILESIZE)[0],standard_vec_into_iso(wall[0]*TILESIZE,wall[1]*TILESIZE)[1]+self.display.get_height()//2-TILESIZE//2))
        screen.blit(self.display,(self.camera_x,self.camera_y))
    def init_collid(self):
        x,y=0,0
        self.map = [[ '0' for i in range(self.taille_y)] for j in range(self.taille_x)]
        for x in range(self.taille_x):
            y = 0
            for y in range(self.taille_y):
                self.case_collide.append((x,y))
                self.cord_collide.append((x,y))
    def init_cord(self):
        for i in range(len(self.case_collide)):
            self.cord_collide[i] = (int(standard_vec_into_iso(self.case_collide[i][0]*TILESIZE,self.case_collide[i][1]*TILESIZE)[0]),int(standard_vec_into_iso(self.case_collide[i][0]*TILESIZE,self.case_collide[i][1]*TILESIZE)[1]+self.display.get_height()//2-TILESIZE//2))
    def refresh(self):
        i=0
        for ligne in self.map:
            for case in ligne:
                if case != '0':
                    self.display.blit(dict_case[case],self.cord_collide[i])
                i += 1
    def draw_grid(self):
        for x in range(0, self.LONGUEUR+TILESIZE, TILESIZE):
            pg.draw.line(self.display, LIGHTGRAY,  (standard_vec_into_iso(x,0)[0],standard_vec_into_iso(x,0)[1]+self.display.get_width()//2),  (standard_vec_into_iso(x,self.LARGEUR)[0],standard_vec_into_iso(x,self.LARGEUR)[1]+self.display.get_height()//2))
        for y in range(0, self.LARGEUR+TILESIZE, TILESIZE):
            pg.draw.line(self.display, LIGHTGRAY,  (standard_vec_into_iso(0,y)[0],standard_vec_into_iso(0,y)[1]+self.display.get_width()//2),  (standard_vec_into_iso(self.LONGUEUR,y)[0],standard_vec_into_iso(self.LONGUEUR,y)[1]+self.display.get_height()//2))
        screen.blit(self.display,(self.camera_x,self.camera_y))
    def check_event(self):
        
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                if event.key == pg.K_m:
                    # dump the wall list for saving
                    print([(int(loc.x), int(loc.y)) for loc in g.walls])
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
                mx,my = pg.mouse.get_pos()
                mx_on_display = mx - self.camera_x
                my_on_display = my - self.camera_y
                i=0
                for x in self.cord_collide:
                    if collide_map_mask.overlap(mouse_mask,(mx_on_display-x[0],my_on_display-x[1])):
                        self.map[self.case_collide[i][0]][self.case_collide[i][1]] = self.case_select 
                        self.display.blit(collide_map,self.cord_collide[i])
                    i+=1
                
            else:
                self.click = False
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.camera_y +=100
                elif event.key == K_DOWN:
                    self.camera_y -=100
                elif event.key == K_RIGHT:
                    self.camera_x -=100
                elif event.key == K_LEFT:
                    self.camera_x +=100
                    
    def save_map(self,path):
        fichier = open(path, "w")
        for x in reversed(self.map):
            for f in x:
                fichier.write(f)
            fichier.write("\n")
        fichier.close()
    def print_menu_editor(self):
        self.init_collid()
        self.init_cord()
        while self.running:
            screen.fill(DARKGRAY)
            self.draw_grid()
            self.draw()
            if creation_img_text_click(img_next,"Sauvegarder",ColderWeather,WHITE,screen,self.click,right=1):
                self.save_map("map_generator.txt")
            if creation_img_text_click(img_next,"Continuer",ColderWeather,WHITE,screen,self.click,left=1):
                self.running = False
            else:
                self.check_event()
            
            pg.display.update()

def standard_vec_into_iso(x,y):
    x_iso = x + y 
    y_iso = -0.5*x + 0.5*y
    return (x_iso,y_iso)
def iso_vec_into_standard(x,y):
    x_stand = 0.5*x - y
    y_stand = 0.5*x + y
    return (x_stand,y_stand)

