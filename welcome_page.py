import pygame
import os
from pygame import mixer #la librairie responsable de la gestion des sons
from settings.screen import LARGEUR, LONGUEUR, screen
from settings.load_img import D,DD,DK

class Welcome():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.START_KEY, self.QUIT_KEY = False, False
        self.width, self.height = 1000, 600
        self.window = pygame.display.set_mode((self.width,self.height))
        self.display = pygame.Surface((self.width, self.height))
        self.BLACK, self.WHITE, self.BURGUNDY = (0,0,0), (255,255,255), (30,0,0)
        self.D = D
        self.DD = DD
        self.DK = pygame.image.load(os.getcwd()+'/f11.png')

    def game_loop(self):
        Xdd, Ydd, Xdragon, Ydragon = -150, -150, 800, -400
        while self.playing:
            Xdd, Ydd, Xdragon, Ydragon = Xdd + 1, Ydd + 1, Xdragon - 1.5, Ydragon + 1.5
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BURGUNDY)
            self.draw_text('Press ESC to QUIT or SPACE to continue', 18, self.width / 4.5, self.height / 11)
            if Xdd >= -50: Xdd = -50
            if Ydd >= -50: Ydd = -50
            if Xdragon <= 450: Xdragon = 450
            if Ydragon >= -self.width / 14: Ydragon = -self.width / 14
            self.dd(Xdd, Ydd)
            self.dragon(Xdragon, Ydragon)
            self.window.blit(self.display, (0, 0))
            pygame.display.update()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running, self.playing = False, False
                if event.key == pygame.K_SPACE:
                    #self.menu = MenuInitial()
                    #self.menu.display_menu()
                    print("next")

    def draw_text(self, text, size, x, y):
        font = pygame.font.SysFont('comicsansms', size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def dd(self, x, y):
        self.display.blit(self.DD, (x, y))
        self.display.blit(self.DK, (-240, 100))

    def dragon(self, x, y):
        self.display.blit(self.D, (x, y))

print(os.getcwd())
w= Welcome()
while w.running:
    w.playing = True
    mixer.music.load('background.wav')
    mixer.music.play(-1) 
    #l argument -1 est pour designer qu'on veut que la musique reste tout au long de l ouverture du jeu 
    w.game_loop()