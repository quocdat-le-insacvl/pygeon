import pygame
from perso import Personnage
from donjon import Donjon
#<------Creation du donjon------>
#Appuyez sur espace pour quitter la partie
#Appuyez sur la touche i pour interagir avec des composants (escalier uniquement)
# /!\ il faut se coller à l'escalier pour interagir avec
#la direction se fait avec les touches directionnelles



pygame.init()


pygame.display.set_caption("Test") 

#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1800,1080))
camera = pygame.Surface((1000,1000))
screen.fill((255,255,255))
pygame.display.flip()
perso = Personnage(screen)
donjon = Donjon(2,screen,perso)
#donjon.load("test1.txt")
donjon.creationDonjon()
donjon.affichageDonjon()
donjon.runningDonjon()


