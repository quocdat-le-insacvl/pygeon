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
def createImages(name,relative_path,scale=True,colorkey=(0,0,0),forceScale=False,scaled=(0,0),autocolorkey=False):
    tailleMax = [70,70]

    erreur = "erreur.jpg"
    image = pygame.image.load(os.path.join(relative_path,erreur))
    ratio = 1
    if name not in os.listdir(relative_path):
        print("Image %s not in imgs/ directory" %name)
    elif name[-4:] != ".png" and name[-4:] != ".jpg":
        print("Image not a .png or a .jpg")
    else:
        image = pygame.image.load(os.path.join(relative_path,name))
        if scaled[0] != 0 and scaled[1] !=0 :
            image = pygame.transform.scale(image,(round(scaled[0]), round(scaled[1])))
        elif ((image.get_width() >= tailleMax[0] or image.get_height() >= tailleMax[1]) and scale )or forceScale:
            if tailleMax[0]!=0 and tailleMax[1] !=0:
                ratio = image.get_width()/tailleMax[0]
                if image.get_height() > image.get_width():
                    ratio = image.get_height()/tailleMax[1]
            image = pygame.transform.scale(image,(round(image.get_width()/ratio), round(image.get_height()/ratio)))
        if autocolorkey:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)
    return image
