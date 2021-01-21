import pygame,os
from settings.color import * 
""""""
def image_loader(path) -> str:
        for i in os.listdir(path):
            image = pygame.image.load(path + i).convert_alpha()
            image.set_colorkey(LIGHT_GREY)
            yield (i,image)
def transform_image(dict_image,multi=3,width=0,height=0):
        for x in dict_image:
            dict_image[x] = pygame.transform.scale(dict_image[x],(int(multi*dict_image[x].get_width()+width),int(multi*dict_image[x].get_height()+height)))
            dict_image[x].set_colorkey(LIGHT_GREY)
