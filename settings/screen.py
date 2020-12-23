import pygame

LONGUEUR = 1800
LARGEUR = 1080
WINDOWS_SIZE = (LONGUEUR,LARGEUR)
screen = pygame.display.set_mode((LONGUEUR, LARGEUR),pygame.FULLSCREEN,32)
user_size = (pygame.display.Info().current_w,pygame.display.Info().current_h)