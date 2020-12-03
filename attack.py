import pygame as pg
from settings import *
from sprites import *


class ATTACK():
    def __init__(self, game, pos, dir):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        """
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
        """

    def surprise_atk(self):
        if not FIN_COMBAT:
            global n, resultat
            self.diceevt.load_dice()
            if self.diceevt.start:
                self.msg = "Surprise Attack"
            self.diceevt.start = False
            # cet attribut est pour afficher Surprise Attack uniquement a la premiere entree a la fonction
            # vu que la fonction s'execute plusieurs fois
            done = False
            for dice in self.diceevt.all_dices:
                if not self.pause:
                    dice.rotate(dice.image, self.angle, self.screen)
                    self.diceevt.compter()
                    self.diceevt.check()
                    n = dice.numero

                else:
                    self.diceevt.pause()
                    self.diceevt.all_dices.draw(self.screen)
                    done = True  # pour signaler que le de a termine de tourner
            if STOP:  # pour generer un entier aleatoire quand le de finit de tourner
                self.diceevt.resultat = generate_randint(1, n)
                print("::"+str(self.diceevt.resultat))
                STOP = False

            if ((self.diceevt.resultat + self.spider.stealth < self.player.ac) and
                    done and not self.diceevt.actdamage and self.tourm):
                self.msg = "Miss. What will be your next step?"
                self.diceevt.damage = 0

            elif ((self.diceevt.resultat + self.spider.stealth >= self.player.ac) and done
                  and self.tourm):
                self.msg = "Hit. Generating damage..."
                self.diceevt.damage = 0
                for i in range(100):
                    # pour laisser un temps entre l'affichage du premier resultat du de et le second
                    self.diceevt.pause()
                self.diceevt.resume(1, 6)
                self.diceevt.check()
            elif ACT_DAMAGE and self.tourm:  # a changer
                self.diceevt.damage = self.diceevt.resultat
                self.player.hp = self.player.hp - self.diceevt.damage  # 100
                ACT_DAMAGE = False
                self.msg = "Your next step?"
                #print("self.player.hp: "+str(self.player.hp))

            # tour du joueur
            if((self.diceevt.resultat + self.player.dex < self.spider.ac) and done
                    and self.tourj and not self.diceevt.actdamage):
                self.msg = "You missed."
                self.diceevt.damage = 0
                for i in range(200):
                    # pour laisser un temps entre l'affichage du premier resultat du de et le second
                    self.diceevt.pause()
                self.tourm, self.tourj = True, False
                self.diceevt.resume(0, 20)
                self.diceevt.check()

            elif((self.diceevt.resultat + self.player.dex >= self.spider.ac) and done
                 and self.tourj and not self.diceevt.actdamage):  # modifier la condition
                self.msg = "You hitted the monster.Generating damage..."
                for i in range(100):
                    # pour laisser un temps entre l'affichage du premier resultat du de et le second
                    self.diceevt.pause()
                self.diceevt.resume(1, 6)
                self.diceevt.check()

            elif ACT_DAMAGE and self.tourj:  # a changer
                self.diceevt.damage = self.diceevt.resultat
                self.spider.hp = self.spider.hp - self.diceevt.damage  # 100
                ACT_DAMAGE = False
                self.diceevt.actdamage = False
                if self.spider.hp <= 0:
                    self.objects.remove(self.spider)
                    self.msg = "Monster beaten"
                    FIN_COMBAT = True
                else:
                    self.tourm, self.tourj = True, False
                    self.msg = "-"
                    for i in range(100):
                        # pour laisser un temps entre l'affichage du premier resultat du de et le second
                        self.diceevt.pause()
                    self.diceevt.resume(0, 20)
                    self.diceevt.check()
                print("Spider hp: "+str(self.spider.hp))
