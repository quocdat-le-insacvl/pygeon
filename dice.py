from random import randrange
import pygame as pg

class Dice(pg.sprite.Sprite):
    """
    def __init__(self, game, image, num):
        super().__init__()
        self.groups = game.dices
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.name = image
        self.numero = num  # pour savoir le type du de
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect(center=(WIDTH, HEIGHT - 3 * TILESIZE))
            #center=(config.SCALE*3+60, config.SCREEN_Y - 2*config.SCALE+40))
        self.rotated_surface = None
        self.rotated_rect = None

    def rotate(self, angle):
        self.rotated_surface = pg.transform.rotozoom(self.image, -angle, 1)
        # to not overwrite the original image surface
        self.rotated_rect = self.rotated_surface.get_rect(center=(WIDTH, HEIGHT - 3 * TILESIZE))
            #center=(config.SCALE*3+60, config.SCREEN_Y - 2*config.SCALE+40))
        # return rotated_surface, rotated_rect
    
    def draw(self):
        self.game.screen.blit(self.rotated_surface, self.rotated_rect)
    """