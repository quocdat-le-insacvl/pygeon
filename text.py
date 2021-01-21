  
import pygame as pg
from settings.color import *
from settings.screen import *
from settings.police import *

class Text(pg.sprite.Sprite):
    def __init__(self,combat, text='text', color=WHITE, size_font=50, pos=[LONGUEUR//2 - 50, LARGEUR//2 - 50], font=path.join(path_police, 'ColderWeather-Regular.ttf'), life_time=0,born=0):
        # Call the parent class (Sprite) constructor
        self.combat = combat
        self.groups = combat.texts
        pg.sprite.Sprite.__init__(self, self.groups)
        self.text_contenu = text
        self.spawn_time = pg.time.get_ticks()
        self.life_time = life_time
        self.font = pg.font.Font(font, size_font)
        self.text = self.font.render(self.text_contenu, True, color)
        self.pos = pos
        self.born = born

    def update(self):
        # print("update "+str(pg.time.get_ticks() - self.spawn_time))
        if pg.time.get_ticks() - self.spawn_time >= self.life_time:
            self.combat.next_text = True
            self.kill()
            return True

    def print_text(self):
        if pg.time.get_ticks() - self.spawn_time >= self.born:
            screen.blit(self.text, self.pos)