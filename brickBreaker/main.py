import pygame as pg
import random
from os import *
from settings import *
from sprites import *


class Game(object):

    def __init__(self):
        self.running = True
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.paddles = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.balls = pg.sprite.Group()

        self.hud_font = path.join(image_folder, 'VIVALDII.TTF')

        self.lives = 3

        # self.npc = NPC()
        self.player = Player(self)
        self.ball = Ball(self)
        y = 70
        for i in range(4):
            x = 37
            for i in range(14):
                Block(self, x, y)
                x += 40
            y += 40

        # start running game loop
        self.run()

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        if len(self.blocks) == 0:
            self.playing = False
        if self.lives < 0:
            self.playing = False

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text("Balls Left: {}".format(self.lives), self.hud_font, 40, WHITE, 100, 400)

        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.screen.fill(BLACK)
        if len(self.blocks) == 0:
            self.draw_text("You Won!", self.hud_font, 120, WHITE, WIDTH / 2, HEIGHT / 2)
            self.draw_text("Press Any Key To Play Again", self.hud_font, 35, WHITE, WIDTH / 2, HEIGHT * (3 / 4))

        else:
            self.draw_text("You Lost!", self.hud_font, 120, WHITE, WIDTH / 2, HEIGHT / 2)
            self.draw_text("Press Any Key To Try Again", self.hud_font, 35, WHITE, WIDTH / 2, HEIGHT * (3 / 4))

        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, font_name, size, color, x, y):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
