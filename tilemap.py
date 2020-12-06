import pygame as pg
from settings.settings import *
from sprites import *
from os import path

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, game, filename):
        self.game = game
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip().split(" "))
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        game_folder = path.dirname(__file__)
        self.img_folder = path.join(game_folder, 'img')
        self.data_wall = []
        
    def render(self, surface):
        for row, tiles in enumerate(self.data):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    self.data_wall.append([col, row])
                # Load image
                tile += ".png"
                image = pg.image.load(path.join(self.img_folder, tile)).convert_alpha()
                # Scale image 
                image = pg.transform.scale(image, (TILESIZE, TILESIZE))
                surface.blit(image, (col * TILESIZE, row * TILESIZE))


    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)


class Minimap:
    def __init__(self, game):
        self.game = game
        self.TOP_LEFT_X = WIDTH - MINIMAP_SCALE
        self.TOP_LEFT_Y = HEIGHT - MINIMAP_SCALE
        self.surface = pg.Surface((MINIMAP_SCALE,  MINIMAP_SCALE))
        self.surface.set_alpha(50)                # alpha level
        self.surface.fill(BLUE)
        
    def draw_minimap(self):
        self.draw_surface()
        self.draw_white_square()
        self.draw_dot_pos(self.game.player.pos, RED)
        for mob in self.game.mobs:
            self.draw_dot_pos(mob.pos, GREEN)
            
    def draw_surface(self):
        self.game.screen.blit(self.surface, (WIDTH - MINIMAP_SCALE, HEIGHT - MINIMAP_SCALE))

    def draw_white_square(self):
        SQUARE_X = self.TOP_LEFT_X + -self.game.camera.camera.left / self.game.map.width * MINIMAP_SCALE
        SQUARE_Y = self.TOP_LEFT_Y + -self.game.camera.camera.top / self.game.map.height * MINIMAP_SCALE
        SQUARE_WIDTH_X = WIDTH / self.game.map.width * MINIMAP_SCALE
        SQUARE_WIDTH_Y = HEIGHT / self.game.map.height * MINIMAP_SCALE
        minimap_rect = pg.Rect(SQUARE_X, SQUARE_Y, SQUARE_WIDTH_X, SQUARE_WIDTH_Y)
        pg.draw.rect(self.game.screen, WHITE, minimap_rect, width=1)
    
    # draw position of player , or monster
    def draw_dot_pos(self, pos, color):
        X = self.TOP_LEFT_X + pos[0] / self.game.map.width * MINIMAP_SCALE
        Y = self.TOP_LEFT_Y + pos[1] / self.game.map.height * MINIMAP_SCALE
        pg.draw.circle(self.game.screen, color, (X, Y), radius=6, width=0)
