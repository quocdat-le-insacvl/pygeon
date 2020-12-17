import pygame
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,20)
LONGUEUR = 1800
LARGEUR = 1080
WINDOWS_SIZE = (LONGUEUR,LARGEUR)
screen = pygame.display.set_mode((LONGUEUR, LARGEUR),pygame.RESIZABLE,32)
user_size = (pygame.display.Info().current_w,pygame.display.Info().current_h)