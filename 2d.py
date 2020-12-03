import pygame, sys,pickle,os
import numpy
import math
import random
from pygame import mixer
from script import pack,player,Wikitem,playerbis,pack_bis,entity_1,tavern
from pygame.locals import *
from settings.screen import LARGEUR, LONGUEUR, screen,WINDOWS_SIZE
from settings.police import Drifftype,ColderWeather,Rumbletumble,coeff,coeff1,coeff2,ColderWeather_small
from settings.load_img import *
from settings.color import *

pygame.init()
clock = pygame.time.Clock()

class two_d():
    def __init__(self):
        self.test = pygame.image.load(r'C:\Users\Antho\Desktop\Pygeon\pygeon\pixel_red.png')
        self.joueurs = pygame.image.load(r'C:\Users\Antho\Desktop\Pygeon\pygeon\Addon\walk_bottom\walk_bottom_1.png')
        self.joueurs = pygame.transform.scale(self.joueurs,(100,100))
        self.pieds = pygame.Surface((100,10))
    def print_map(self):
        test= False
        running = True
        test_mask = pygame.mask.from_surface(self.test)
        #self.test.set_colorkey(WHITE)
        mouvement = [False,False,False,False]

        test_rect = self.test.get_rect()
        ox =500 - test_rect.centerx
        oy = 500 - test_rect.centery
        ox_1 = 1000 - test_rect.centerx
        oy_1 = 1000 - test_rect.centery
        pos_x,pos_y = 0,0
        self.pieds.fill(RED)
        joueurs_mask = pygame.mask.from_surface(self.joueurs)
        pieds_mask =pygame.mask.from_surface(self.pieds)
        while running:

            mx,my = pygame.mouse.get_pos()
            screen.fill(LIGHT_GREY)
            screen.blit(self.test,(ox,oy))
            screen.blit(self.joueurs,(pos_x,pos_y))
            screen.blit(self.test,(ox_1,oy_1))
            screen.blit(self.pieds,(pos_x,pos_y+90))
            offset = (ox,90-oy)
            offset_1 = (ox_1,90-oy_1)
            off_list = list()
            off_list.append(offset_1)
            off_list.append(offset)
            test = False

            if mouvement[0]:
                for i in range(len(off_list)):
                    if test_mask.overlap(pieds_mask,((pos_x)-off_list[i][0],(pos_y+1-off_list[i][0]))):
                        self.test.set_colorkey(BLACK)
                if not test:
                    pos_y += 1

            elif mouvement[1]:
                for i in range(len(off_list)):
                    if test_mask.overlap(pieds_mask,((pos_x)-off_list[i][0],(pos_y-off_list[i][0]))):
                        self.test.set_colorkey(BLACK)
                if not test:
                    pos_y -= 1

            elif mouvement[2]:
                for i in range(len(off_list)):
                    if test_mask.overlap(pieds_mask,((pos_x+1)-off_list[i][0],(pos_y-off_list[i][0]))):
                        self.test.set_colorkey(BLACK)
                if not test:
                    pos_x += 1
            elif mouvement[3]:
                for i in range(len(off_list)):
                    if test_mask.overlap(pieds_mask,((pos_x-1)-off_list[i][0],(pos_y-off_list[i][0]))):
                        self.test.set_colorkey(BLACK)
                if not test:
                    pos_x -= 1

            for event in pygame.event.get():
                if event.type == QUIT:
                        sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        mouvement[0] = True
                    if event.key == K_DOWN:
                        mouvement[1] = True
                    if event.key == K_RIGHT:
                        mouvement[2] = True
                    if event.key == K_LEFT:
                        mouvement[3] = True
                if event.type == KEYUP:
                    if event.key == K_UP:
                        mouvement[0] = False
                    if event.key == K_DOWN:
                        mouvement[1] = False
                    if event.key == K_RIGHT:
                        mouvement[2] = False
                    if event.key == K_LEFT:
                        mouvement[3] = False  
            pygame.display.update()
            running = self.checkevent()
    def checkevent(self):
            global screen
            global WINDOWS_SIZE
            global fullscreen
            self.click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return False
                if event.type == VIDEORESIZE:
                    if not fullscreen:
                        WINDOWS_SIZE = (event.w,event.h)
                        screen = pygame.display.set_mode(WINDOWS_SIZE,pygame.RESIZABLE,32)
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True     
                    
            return True

two = two_d()
two.print_map()