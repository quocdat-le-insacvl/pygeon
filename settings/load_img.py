import pygame

img_next = pygame.image.load(r'Addon\Menu\TextBTN_Big.png')
menu_background = pygame.image.load(r'Addon\Menu\UI board Large Set.png')
title = pygame.image.load(r'Addon\Menu\IRONY TITLE  empty.png')
img_description = pygame.image.load(r'Addon\Menu\UI board Large stone.png')
img_backgrounds_warning = pygame.image.load(r'Addon\Menu\UI board Small  parchment.png')
exclamation = pygame.image.load(r'Addon\Menu\Exclamation_Gray.png')
validation_button = pygame.image.load(r'Addon\Menu\TextBTN_Medium.png')
img_support_warning = pygame.image.load(r'Addon\Menu\UI board Small  stone.png')
img_pressed = pygame.image.load(r'Addon\Menu\TextBTN_Big.png')

# INTRO MENU IMG 

D = pygame.image.load(r'Addon\Menu\Intro_menu\menu1.png')
DD = pygame.image.load(r'Addon\Menu\Intro_menu\D&D.png')
DK = pygame.image.load(r'Addon\Menu\Intro_menu\f11.png')

# SOL 


arbre = pygame.image.load(r'arbre.png')
arbre = pygame.transform.scale(arbre,(200,300)).convert_alpha()
arbre_2 = pygame.image.load(r'C:\Users\Antho\Desktop\Pygeon\pygeon\settings\tree_2.png')
arbre_2 = pygame.transform.scale(arbre_2,(200,300)).convert_alpha()
pixel_red = pygame.image.load(r'Collide.png').convert()
pixel_red = pygame.transform.scale(pixel_red,(200,120))
pixel_red.set_colorkey((255,255,255))
#pixel_red.set_colorkey((0,0,0))
end_game = pygame.image.load(r'Addon\end_game.png').convert_alpha()
end_game = pygame.transform.scale(end_game,(200,200))
road = pygame.image.load(r'C:\Users\Antho\Desktop\Pygeon\pygeon\settings\floor.PNG').convert_alpha()
road = pygame.transform.scale(road,(200,110))
road.set_colorkey((255,255,255))
