import pygame

LONGUEUR = 1700
LARGEUR = 1080
WINDOWS_SIZE = (LONGUEUR,LARGEUR)
screen = pygame.display.set_mode((LONGUEUR, LARGEUR),pygame.RESIZABLE,32)
user_size = (pygame.display.Info().current_w,pygame.display.Info().current_h)