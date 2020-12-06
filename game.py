import pygame as pg
import sys
from os import path
from pygame.constants import K_g
from settings.settings import *
from sprites import *
from tilemap import *
#from fonctions import *
import time, math
from combat import *
from level import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.spider_img = pg.image.load(path.join(img_folder, SPIDER_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.texts = pg.sprite.Group()
        self.spiders = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'zombie':
                Mob(self, tile_object.x, tile_object.y)
            if tile_object.name == 'spider':
               self.spider = Spider(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.level = Level(self)
        
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.texts.update()
        # self.dices.update()
        self.camera.update(self.player)
        self.level.update()
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)
        
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # self.draw_log()
        for text in self.texts:
            text.print_text()
        self.draw_status()
        self.draw_minimap()
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                """ if event.key == K_g:
                    self.dice_evt.resume(0,20)
                    self.dice_evt.actdamage = False
                    self.dice_evt.reset_all()
                    self.tour_jouer = True
                    self.tour_monster = False """

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def draw_status(self):
        color=WHITE
        size_font=20
        level_pos=[WIDTH - 200, 50]
        monster_pos = [WIDTH - 200, 70]
        _font='freesansbold.ttf'
        font = pg.font.Font(_font, size_font)
        level_text = font.render("Level : {}".format(self.level.level), True, color)
        monster_text = font.render("Monster left : {}".format(self.level.num_monster), True, color)
        self.screen.blit(level_text,  level_pos)
        self.screen.blit(monster_text, monster_pos)

    def draw_minimap(self):
        TOP_LEFT_X = WIDTH - MINIMAP_SCALE
        TOP_LEFT_Y = HEIGHT - MINIMAP_SCALE
        s = pg.Surface((MINIMAP_SCALE,  MINIMAP_SCALE))
        s.set_alpha(50)                # alpha level
        s.fill(BLUE)          # this fills the entire surface
        # (0,0) are the top-left coordinates
        self.screen.blit(s, (WIDTH- MINIMAP_SCALE, HEIGHT - MINIMAP_SCALE))
        SQUARE_X = TOP_LEFT_X + -self.camera.camera.left / self.map.width * MINIMAP_SCALE 
        SQUARE_Y = TOP_LEFT_Y + -self.camera.camera.top / self.map.height * MINIMAP_SCALE
        SQUARE_WIDTH_X = WIDTH / self.map.width * MINIMAP_SCALE
        SQUARE_WIDTH_Y = HEIGHT / self.map.height * MINIMAP_SCALE
        minimap_rect = pg.Rect(SQUARE_X, SQUARE_Y, SQUARE_WIDTH_X, SQUARE_WIDTH_Y)
        pg.draw.rect(self.screen, WHITE, minimap_rect, width=1)
        PERSO_X = TOP_LEFT_X + self.player.pos[0] / self.map.width * MINIMAP_SCALE
        PERSO_Y = TOP_LEFT_Y + self.player.pos[1] / self.map.height * MINIMAP_SCALE
        pg.draw.circle(self.screen, RED, (PERSO_X, PERSO_Y), radius=6, width=0)

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
