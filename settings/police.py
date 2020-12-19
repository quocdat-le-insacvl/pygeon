import pygame
from os import path
from settings.screen import LARGEUR
from settings.load_img import board_init
pygame.init()

coeff = 10
coeff1 = 14
coeff2 = 8

# ERROR WITH PATH , so I will fix it like this
path_settings = path.dirname(__file__)
path_pygeon = path.dirname(path_settings)
path_addon = path.join(path_pygeon, 'Addon')
path_police = path.join(path_addon, 'Police')

#AlphaWood =
path_ColderWeather = path.join(path_police, 'ColderWeather-Regular.ttf')
#ColderWeather = pygame.font.Font(r'Addon\Police\ColderWeather-Regular.ttf',LARGEUR//coeff1)
ColderWeather = pygame.font.Font(path_ColderWeather,LARGEUR//coeff1)
#Drifftype =  pygame.font.Font(r'Addon\Police\Drifttype Solid.ttf',LARGEUR//coeff)
Drifftype = pygame.font.Font(path.join(path_police, 'Drifttype Solid.ttf'), LARGEUR//coeff)

#Outrun_future =
Rumbletumble = pygame.font.Font(path.join(path_police, 'rumbletumble.ttf'), LARGEUR//coeff2)
ColderWeather_small = pygame.font.Font(path.join(path_police, 'ColderWeather-Regular.ttf'), 30)


title = pygame.font.Font(path.join(path_addon,r'Police\ColderWeather-Regular.ttf' ), board_init().get_height()//10)
title2=pygame.font.Font(path.join(path_addon,r'Police\21 Glyphs.ttf' ), board_init().get_height()//10)
subtitle=pygame.font.Font(path.join(path_addon,r'Police\ColderWeather-Regular.ttf' ), board_init().get_height()//20)
sub2=pygame.font.Font(path.join(path_addon,r'Police\21 Glyphs.ttf' ), board_init().get_height()//20)
text=pygame.font.Font(path.join(path_addon,r'Police\ColderWeather-Regular.ttf' ), board_init().get_height()//30)
astxt=pygame.font.Font(path.join(path_addon,r'Police\Outrun-future.otf' ), 20)
astxt.set_bold(1)