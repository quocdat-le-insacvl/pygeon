import pygame
from fighter import Fighter
pygame.init()
fighter=Fighter()
running=True
while running:
    fighter.xp+=1000
    pygame.display.set_caption("test")
    pygame.display.set_mode((1500, 1000))
    fighter.levelupchange()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()