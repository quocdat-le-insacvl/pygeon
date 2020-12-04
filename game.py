import pygame as pg
import sys
from os import path
from pygame.constants import K_g
from settings.settings import *
from sprites import *
from tilemap import *
from fonctions import *
import time, math
from combat import *
# HUD functions


def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        # Je veux bien de reformuler
        self.first = True
        self.angle = 0  # pour la rotation
        self.score = 0  # pour le dice
        self.dice_evt = DiceEvent(self)
        self.msg = "-"
        self.pause = False
        self.tour_monster = True  # cette valeur est a True si c'est le tour du monstre de jouer
        self.tour_jouer = False  # cette valeur est a True si c'est le tour du joueur de jouer
        self.LANCER = False
        self.STOP = False
        self.MODIFY_HP = False
        self.ACT_DAMAGE = False
        self.FIN_COMBAT = False
        self.time = time.time()


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
        self.spiders = pg.sprite.Group()
        self.texts = pg.sprite.Group()
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
        self.camera.update(self.player)
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            """
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            """
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)
        hits = pg.sprite.spritecollide(self.player, self.spiders, False)
        for hit in hits:
            Combat(self, hit)
            self.surprise_atk()
        self.angle += 10

    def draw_log(self):
        #Christine :
        affichage_box(self.screen,"Hitpoints: " + str(self.player.hp), (0,0,0),0,0,30)
        affichage_box(self.screen,"Resultat du de: " + str(self.dice_evt.resultat), (0,0,0),0,30,30)
        affichage_box(self.screen,"Damage: " + str(self.dice_evt.damage), (0,0,0),0,60,30)
        affichage_box(self.screen,"Message: " + str(self.msg), (0,0,0),0,90,30)

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
                pg.draw.rect(self.screen, CYAN,
                             self.camera.apply_rect(wall.rect), 1)

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_log()
        for text in self.texts:
            text.print_text()
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
                if event.key == K_g:
                    self.dice_evt.resume(0,20)
                    self.dice_evt.actdamage = False
                    self.dice_evt.reset_all()
                    self.tour_jouer = True
                    self.tour_monster = False

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def surprise_atk(self):
        if not self.FIN_COMBAT:
            global n, resultat
            self.dice_evt.load_dice()
            if self.dice_evt.start:
                self.msg = "Surprise Attack"
            self.dice_evt.start = False
            # cet attribut est pour afficher Surprise Attack uniquement a la premiere entree a la fonction
            # vu que la fonction s'execute plusieurs fois
            done = False
            for dice in self.dice_evt.all_dices:
                if not self.pause:
                    dice.rotate(dice.image, self.angle, self.screen)
                    self.dice_evt.compter()
                    self.dice_evt.check()
                    n = dice.numero
                else:
                    self.dice_evt.pause()
                    self.dice_evt.all_dices.draw(self.screen)
                    done = True  # pour signaler que le de a termine de tourner
            if self.STOP:  # pour generer un entier aleatoire quand le de finit de tourner
                self.dice_evt.resultat = generate_randint(1, n)
                print("::"+str(self.dice_evt.resultat))
                self.STOP = False

            if ((self.dice_evt.resultat + self.spider.stealth < self.player.ac) and
                    done and not self.dice_evt.actdamage and self.tour_monster):
                self.msg = "Miss. What will be your next step?"
                self.dice_evt.damage = 0

            elif ((self.dice_evt.resultat + self.spider.stealth >= self.player.ac) and done
                  and self.tour_monster):
                self.msg = "Hit. Generating damage..."
                self.dice_evt.damage = 0
                for i in range(100):
                    # pour laisser un temps entre l'affichage du premier resultat du de et le second
                    self.dice_evt.pause()
                self.dice_evt.resume(1, 6)
                self.dice_evt.check()
            elif self.ACT_DAMAGE and self.tour_monster:  # a changer
                self.dice_evt.damage = self.dice_evt.resultat
                self.player.hp = self.player.hp - self.dice_evt.damage  # 100
                self.ACT_DAMAGE = False
                self.msg = "Your next step?"
                #print("self.player.hp: "+str(self.player.hp))

            # tour du joueur
            if((self.dice_evt.resultat + self.player.dex < self.spider.ac) and done
                    and self.tour_jouer and not self.dice_evt.actdamage):
                self.msg = "You missed."
                self.dice_evt.damage = 0
                for i in range(200):
                    # pour laisser un temps entre l'affichage du premier resultat du de et le second
                    self.dice_evt.pause()
                self.tour_monster, self.tour_jouer = True, False
                self.dice_evt.resume(0, 20)
                self.dice_evt.check()

            elif((self.dice_evt.resultat + self.player.dex >= self.spider.ac) and done
                 and self.tour_jouer and not self.dice_evt.actdamage):  # modifier la condition
                self.msg = "You hitted the monster.Generating damage..."
                for i in range(100):
                    # pour laisser un temps entre l'affichage du premier resultat du de et le second
                    self.dice_evt.pause()
                self.dice_evt.resume(1, 6)
                self.dice_evt.check()

            elif self.ACT_DAMAGE and self.tour_jouer:  # a changer
                self.dice_evt.damage = self.dice_evt.resultat
                self.spider.hp = self.spider.hp - self.dice_evt.damage  # 100
                self.ACT_DAMAGE = False
                self.dice_evt.actdamage = False
                if self.spider.hp <= 0:
                    self.objects.remove(self.spider)
                    self.msg = "Monster beaten"
                    self.FIN_COMBAT = True
                else:
                    self.tour_monster, self.tour_jouer = True, False
                    self.msg = "-"
                    for i in range(100):
                        # pour laisser un temps entre l'affichage du premier resultat du de et le second
                        self.dice_evt.pause()
                    self.dice_evt.resume(0, 20)
                    self.dice_evt.check()
                print("Spider hp: "+str(self.spider.hp))

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
