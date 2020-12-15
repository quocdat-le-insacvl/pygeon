import pygame
from fonction_load_image import image_loader,transform_image
from settings.screen import WINDOWS_SIZE
"""
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

pixel_red = pygame.image.load(r'Addon\Collide.png').convert()
pixel_red = pygame.transform.scale(pixel_red,(200,120))
pixel_red.set_colorkey((255,255,255))
board_medium = pygame.image.load(r'Addon\Menu\UI board Medium  parchment.png')

end_game = pygame.image.load(r'Addon\end_game.png').convert_alpha()
end_game = pygame.transform.scale(end_game,(200,200))
road = pygame.image.load(r'Addon\floor.PNG').convert_alpha()
road = pygame.transform.scale(road,(200,110))
road.set_colorkey((255,255,255))

walk_bottom =dict(image_loader('Addon/walk_bottom/'))
transform_image(walk_bottom)
walk_right = dict(image_loader('Addon/walk_right/'))
transform_image(walk_right)
walk_left = dict(image_loader('Addon/walk_left/'))
transform_image(walk_left)
walk_top = dict(image_loader('Addon/walk_top/'))
transform_image(walk_top)
demon_walk = dict(image_loader('Addon/demon_walk/'))
transform_image(demon_walk,3)
grass = dict(image_loader('Addon/grass/'))
transform_image(grass,0,200,200)
tree = dict(image_loader('Addon/Tree/'))
transform_image(tree,1,0,80)

seller_1_hide = dict(image_loader('Addon/seller/'))
transform_image(seller_1_hide,3)
seller_1_animation = dict()
seller_1_animation["idle"] = seller_1_hide

wizard_hide = dict(image_loader('Addon/Wizard Pack/idle/'))
transform_image(wizard_hide,2)
wizard_attack = dict(image_loader('Addon/Wizard Pack/attack/'))
transform_image(wizard_attack,2)
wizard_animation = dict()
wizard_animation["idle"] = wizard_hide
wizard_animation["attack"] = wizard_attack

squelton_idle = dict(image_loader('Addon/squeleton_idle/'))
transform_image(squelton_idle,5)
squelton_animation = dict()
squelton_animation["idle"] = squelton_idle

dark_wizard_idle = dict(image_loader('Addon/dark_wizard_idle/'))
transform_image(dark_wizard_idle,0,2*wizard_hide["wizard_idle_1.png"].get_width(),2*wizard_hide["wizard_idle_1.png"].get_height())
dark_wizard_animation = dict()
dark_wizard_animation["idle"] = dark_wizard_idle


fence_1 = pygame.image.load(r'Addon\fence_1.png')
fence_1 = pygame.transform.scale(fence_1,(200,200))
fence_2 = pygame.image.load(r'Addon\fence_2.png')
fence_2 = pygame.transform.scale(fence_2,(200,200))

fond = pygame.image.load(r'Addon\Background\wine-wang-sunshineforest-1.jpg')
fond = pygame.transform.scale(fond,WINDOWS_SIZE)
case = pygame.image.load(r'Addon\case.png')
case = pygame.transform.scale(case,(pixel_red.get_width(),pixel_red.get_height()))
"""
case_select = pygame.image.load(r'Addon\case_select.png')
case_select = pygame.transform.scale(case_select,(pixel_red.get_width(),pixel_red.get_height()))
case_select.set_colorkey((255,255,255))
case_select.set_alpha(100)

rune = pygame.image.load(r"Addon\rune_1.png").convert_alpha()
rune_1 = pygame.image.load(r"Addon\rune_2.png").convert_alpha()

sheep = pygame.image.load(r'Addon\sheep.PNG').convert()
sheep.set_colorkey((255,255,255))