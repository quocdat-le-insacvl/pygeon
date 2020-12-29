from settings.color import *
import pygame
from fonction_load_image import image_loader,transform_image
from settings.screen import WINDOWS_SIZE
from os import path,getcwd

path_settings = path.dirname(__file__)
path_pygeon = path.dirname(path_settings)
path_addon = path.join(path_pygeon, 'Addon')
path_police = path.join(path_addon, 'Police')
path_menu = path.join(path_addon, 'Menu')
path_ava = path.join(path_addon, 'avata')
path_light = path.join(path_addon, 'Light')


button=pygame.image.load(path.join(path_addon,'Menu\TextBTN_Medium.png'))
buttonp=pygame.image.load(path.join(path_addon,'Menu\TextBTN_Medium_Pressed.png'))



# LOAD avata for minimap 
ava_perso = pygame.image.load(path.join(path_ava, 'ava_perso.png'))
ava_perso = pygame.transform.scale(ava_perso, (30, 30))
rect_ava_perso = ava_perso.get_rect()
pygame.draw.circle(ava_perso, HALF_RED,rect_ava_perso.center, radius=17, width=3)

# Fog
light_mask = pygame.image.load(path.join(path_light, 'light_medium.png')).convert_alpha()

img_next = pygame.image.load(path.join(path_menu,'TextBTN_Big.png')).convert_alpha()
menu_background = pygame.image.load(path.join(path_menu, 'UI board Large Set.png')).convert_alpha()
#title = pygame.image.load(path.join(path_menu,'IRONY TITLE  empty.png')).convert_alpha()
img_description = pygame.image.load(path.join(path_menu, 'UI board Large stone.png')).convert_alpha()
img_backgrounds_warning = pygame.image.load(path.join(path_menu, 'UI board Small  parchment.png')).convert_alpha()
img_inventaire  = pygame.image.load(path.join(path_menu, 'UI board Large  parchment.png')).convert_alpha()
exclamation = pygame.image.load(path.join(path_menu, 'Exclamation_Gray.png')).convert_alpha()
validation_button = pygame.image.load(path.join(path_menu, 'TextBTN_Medium.png')).convert_alpha()
validation_button_pressed = pygame.image.load(path.join(path_menu, 'TextBTN_Medium_Pressed.png')).convert_alpha()
img_support_warning = pygame.image.load(path.join(path_menu, 'UI board Small  stone.png')).convert_alpha()
img_pressed = pygame.image.load(path.join(path_menu, 'TextBTN_Big.png')).convert_alpha()

# INTRO MENU IMG
path_intro_menu = path.join(path_menu, 'Intro_menu')
D = pygame.image.load(path.join(path_intro_menu, 'menu1.png')).convert_alpha()
DD = pygame.image.load(path.join(path_intro_menu, 'D&D.png')).convert_alpha()
DK = pygame.image.load(path.join(path_intro_menu, 'f11.png')).convert_alpha()

# SOL

pixel_red = pygame.image.load(path.join(path_addon, 'Collide.png')).convert()
pixel_red = pygame.transform.scale(pixel_red,(200,120))
pixel_red.set_colorkey((255,255,255))

collide_map = pygame.image.load(path.join(path_addon,'map_collide.png')).convert()



board_medium = pygame.image.load(path.join(path_menu,'UI board Medium  parchment.png'))

end_game = pygame.image.load(path.join(path_addon, 'end_game.png')).convert_alpha()
end_game = pygame.transform.scale(end_game,(200,200))

road = pygame.image.load(path.join(path_addon, 'floor.PNG')).convert_alpha()
road = pygame.transform.scale(road,(200,110))
road.set_colorkey((255,255,255))
wall = pygame.image.load(path.join(path_addon,"test.png")).convert_alpha()
wall= pygame.transform.scale(wall,(200,205))
wall.set_colorkey((255,255,255))
void = pygame.image.load(path.join(path_addon,"66.png")).convert_alpha()
void = pygame.transform.scale(void,(200,200))
void.set_colorkey((255,255,255))

idle =dict(image_loader(path.join(path_addon, 'idle/')))
transform_image(idle)
walk_bottom =dict(image_loader(path.join(path_addon, 'walk_bottom/')))
transform_image(walk_bottom)
walk_right = dict(image_loader(path.join(path_addon, 'walk_right/')))
transform_image(walk_right)
walk_left = dict(image_loader(path.join(path_addon, 'walk_left/')))
transform_image(walk_left)
walk_top = dict(image_loader(path.join(path_addon, 'walk_top/')))
transform_image(walk_top)
player_animation = dict()
player_animation["idle"] = idle
player_animation["walk_bottom"] = walk_bottom
player_animation["walk_right"] = walk_right
player_animation["walk_left"] = walk_left
player_animation["walk_top"] = walk_top



grass = dict(image_loader(path.join(path_addon, 'Grass/')))
transform_image(grass,0,200,200)
tree = dict(image_loader(path.join(path_addon, 'Tree/')))
transform_image(tree,1,0,80)

seller_1_hide = dict(image_loader(path.join(path_addon, 'seller/seller_5/')))
transform_image(seller_1_hide,3)
seller_1_animation = dict()
seller_1_animation["idle"] = seller_1_hide



wizard_hide = dict(image_loader(path.join(path_addon,'Wizard Pack/idle/')))
transform_image(wizard_hide,2)
wizard_attack = dict(image_loader(path.join(path_addon,'Wizard Pack/attack/')))
transform_image(wizard_attack,2)
wizard_walk = dict(image_loader(path.join(path_addon,'Wizard Pack/walk/')))
transform_image(wizard_walk,2.3)
wizard_animation = dict()
wizard_animation["idle"] = wizard_hide
wizard_animation["attack"] = wizard_attack
wizard_animation["walk"] = wizard_walk

squelton_idle = dict(image_loader(path.join(path_addon,'squeleton_idle/')))
transform_image(squelton_idle,5)
squelton_animation = dict()
squelton_animation["idle"] = squelton_idle

squelton_walk = dict(image_loader(path.join(path_addon,'squeleton_walk/')))
transform_image(squelton_walk,5)
squelton_animation["walk"] = squelton_walk

squelton_attack = dict(image_loader(path.join(path_addon,'squeleton_attack/')))
transform_image(squelton_attack,5)
squelton_animation["attack"] = squelton_attack

dark_wizard_idle = dict(image_loader(path.join(path_addon,'dark_wizard_idle/')))
transform_image(dark_wizard_idle,3)
dark_wizard_animation = dict()
dark_wizard_walk = dict(image_loader(path.join(path_addon,'dark_wizard_walk/')))
transform_image(dark_wizard_walk,3)

dark_wizard_attack = dict(image_loader(path.join(path_addon,'dark_wizard_attack/')))
transform_image(dark_wizard_attack,3)
dark_wizard_animation["idle"] = dark_wizard_idle
dark_wizard_animation["walk"] = dark_wizard_walk
dark_wizard_animation["attack"] = dark_wizard_attack



demon_walk = dict(image_loader(path.join(path_addon, 'demon_walk/')))
transform_image(demon_walk,4.5)
demon_animation = dict()
demon_animation["walk"] = demon_walk

demon_idle = dict(image_loader(path.join(path_addon, 'demon_idle/')))
transform_image(demon_idle,4.5)
demon_animation["idle"] = demon_idle

demon_attack = dict(image_loader(path.join(path_addon, 'demon_attack/')))
transform_image(demon_attack,4.5)
demon_animation["attack"] = demon_attack

demon_1_walk = dict(image_loader(path.join(path_addon, 'demon_1_walk/')))
transform_image(demon_1_walk,4.5)
demon_1_animation = dict()
demon_1_animation["walk"] = demon_1_walk

demon_1_idle = dict(image_loader(path.join(path_addon, 'demon_1_idle/')))
transform_image(demon_1_idle,4.5)
demon_1_animation["idle"] = demon_1_idle

demon_1_attack = dict(image_loader(path.join(path_addon, 'demon_1_attack/')))
transform_image(demon_1_attack,4.5)
demon_1_animation["attack"] = demon_1_attack


fence_1 = pygame.image.load(path.join(path_addon, 'fence_1.png'))
fence_1 = pygame.transform.scale(fence_1,(200,200))
fence_2 = pygame.image.load(path.join(path_addon, 'fence_2.png'))
fence_2 = pygame.transform.scale(fence_2,(200,200))

path_background = path.join(path_addon, 'Background')

fond = pygame.image.load(path.join(path_background, 'wine-wang-sunshineforest-1.jpg'))
fond = pygame.transform.scale(fond,WINDOWS_SIZE)
fond.set_colorkey(BLACK)

case = pygame.image.load(path.join(path_addon, 'case.png'))
case = pygame.transform.scale(case,(pixel_red.get_width(),pixel_red.get_height()))
case.set_colorkey(BLACK)

case_select = pygame.image.load(path.join(path_addon, 'case_select.png'))
case_select = pygame.transform.scale(case_select,(pixel_red.get_width(),pixel_red.get_height()))
case_select.set_colorkey((255,255,255))
#case_select.set_alpha(100)

rune = pygame.image.load(path.join(path_addon, "rune_1.png")).convert_alpha()
rune_1 = pygame.image.load(path.join(path_addon, "rune_2.png")).convert_alpha()

#combat
image_boutton = pygame.image.load(getcwd()+'\\Addon\\Menu\\TextBTN_Small.png')
image_box = pygame.image.load(getcwd()+'\\Addon\\UI board Small Set.png')
image_boutton1 = pygame.image.load(getcwd()+'\\Addon\\Menu\\TextBTN_XSmall.png')
floor_tavern = pygame.image.load(path.join(path_addon,'floor_tavern.png')).convert_alpha()
floor_tavern = pygame.transform.scale(floor_tavern,(floor_tavern.get_width(),floor_tavern.get_width()//2))
def board_init(i=0):
    # create a board and return it, take in arguments the size (tuple) of the board
    if i==0:
        return pygame.image.load(path.join(path_menu, r'UI board Large  parchment.png')).convert_alpha()
    if i==1:
        return pygame.image.load(path.join(path_menu,r'UI board Large stone.png')).convert_alpha()

collide_monster = pygame.image.load(path.join(path_addon,"test_collide_monster.png"))

chair = pygame.image.load(path.join(path_addon,"chair.png")).convert_alpha()
chair = pygame.transform.scale(chair,(95,2*95))
chair_2 = pygame.image.load(path.join(path_addon,"chair_2.png")).convert_alpha()
chair_2 = pygame.transform.scale(chair_2,(95,2*95))
chair_3 = pygame.image.load(path.join(path_addon,"chair_3.png")).convert_alpha()
chair_3 = pygame.transform.scale(chair_3,(95,2*95))

chest = pygame.image.load(path.join(path_addon,"chest.png")).convert_alpha()
chest = pygame.transform.scale(chest,(100,100))

etagere = pygame.image.load(path.join(path_addon,"etagère.png")).convert_alpha()
etagere = pygame.transform.scale(etagere,(150,2*150))

etagere_2 = pygame.image.load(path.join(path_addon,"etagere_2.png")).convert_alpha()
etagere_2 = pygame.transform.scale(etagere_2,(150,2*150))

table = pygame.image.load(path.join(path_addon,"table.png")).convert_alpha()
table = pygame.transform.scale(table,(2*150,2*150))