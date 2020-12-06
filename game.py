import pygame as pg
import sys
from os import path
from pygame.constants import K_g
from settings.settings import *
from sprites import *
import tilemap
#from fonctions import *
import time, math
from combat import *
from level import *

# Voici le tutorial qui m'inspire, regardez si jamais vous avez du mal a comprendre le code! Tous sont bien expliques et bien ecrits
# https://www.youtube.com/watch?v=3UxnelT9aCo&list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i&ab_channel=KidsCanCode

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
        
        self.map = tilemap.Map(self, path.join(map_folder, 'level1.txt'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        
        # self.map = tilemap.Map(self, path.join(map_folder, 'combat.txt'))
        self.map_combat = tilemap.Map(self, path.join(map_folder, 'combat.txt'))
        self.map_combat_img = self.map_combat.make_map()
        self.map_combat_rect = self.map_combat_img.get_rect()

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
        # Combat settings
        self.combat_mode = False
        self.game_pause = False
        self.walls_combat = pg.sprite.Group()
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.texts = pg.sprite.Group()
        self.spiders = pg.sprite.Group()
        self.player = Player(self)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.level = Level(self)
        self.minimap = Minimap(self)
        # Adding wall
        for x, y in self.map.data_wall:
            Wall(self, x, y)
        
        for x, y in self.map_combat.data_wall:
            Wall(self, x, y, True)
        
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
        if self.game_pause:
            self.texts.update()
            self.camera.update(self.player)
            # self.camera.update(self.player)
            # self.level.update()
            self.player.update()
            
        else:
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
                ###
                Combat(self)
                self.game_pause = True    
                ###
            if hits:
                self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
            # bullets hit mobs
            hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
            for hit in hits:
                hit.health -= BULLET_DAMAGE
                hit.vel = vec(0, 0)
        
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        
        if not self.game_pause:
            # self.screen.fill(BGCOLOR)
            self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
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
            self.minimap.draw_minimap()
            
        else:
            self.screen.blit(self.map_combat_img, self.camera.apply_rect(self.map_combat_rect))
            self.draw_grid()
            for sprite in self.walls_combat:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            self.screen.blit(self.player.image, self.camera.apply(self.player))
        
        for text in self.texts:
            text.print_text()
        self.draw_status()

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
                if event.key == pg.K_c:
                    self.combat_mode = not self.combat_mode
                    self.game_pause = not self.game_pause
                    Combat(self)

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

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            
# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
