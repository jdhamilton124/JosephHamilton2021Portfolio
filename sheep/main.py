import sys

import pygame as pg
import random
from os import *
from settings import *
from map import *
from sprites import *


class Game(object):

    def __init__(self):
        self.running = True
        self.playing = True
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screenf = pg.Surface((WIDTH, HEIGHT))
        self.rectf = self.screenf.get_rect()
        self.mouse_down = False
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.tile_timer = 0
        self.hud_font = path.join(image_folder, 'VIVALDII.TTF')
        self.wolf_image = pg.image.load(path.join(image_folder, "sheep_wolf.png")).convert()
        self.sheep_image = pg.image.load(path.join(image_folder, "sheep_sheep.png")).convert()
        self.true_sheep_image = pg.image.load(path.join(image_folder, "sheep_ttrue_sheep.png")).convert()
        self.ground_images = []
        self.ground_images.append(pg.image.load(path.join(image_folder, "dirt.png")).convert())
        self.ground_images.append(pg.image.load(path.join(image_folder, "dirt+.png")).convert())
        self.ground_images.append(pg.image.load(path.join(image_folder, "dirt++.png")).convert())
        self.ground_images.append(pg.image.load(path.join(image_folder, "grass.png")).convert())
        for i in self.ground_images:
            i.set_colorkey(BLACK)
        self.blood_image = pg.image.load(path.join(image_folder, "blood.png")).convert()
        self.blood_image.set_colorkey(BLACK)

        self.screams = [pg.mixer.Sound(path.join(sounds_folder, "Scream.wav")),
                        pg.mixer.Sound(path.join(sounds_folder, "Scream2.mp3")),
                        pg.mixer.Sound(path.join(sounds_folder, "Scream3.mp3")),
                        pg.mixer.Sound(path.join(sounds_folder, "Scream4.mp3")),
                        pg.mixer.Sound(path.join(sounds_folder, "Scream5.mp3"))]
        self.bleats = [pg.mixer.Sound(path.join(sounds_folder, "Bleat.wav")),
                       pg.mixer.Sound(path.join(sounds_folder, "Bleat2.mp3")),
                       pg.mixer.Sound(path.join(sounds_folder, "Bleat3.mp3")),
                       pg.mixer.Sound(path.join(sounds_folder, "Bleat4.mp3"))]
        self.crunches = []
        for i in range(7):
            self.crunches.append(pg.mixer.Sound(path.join(sounds_folder, "crunch.{}.ogg".format(i + 1))))
            self.crunches[i].set_volume(0.04)
        self.splat = pg.mixer.Sound(path.join(sounds_folder, "Splat.wav"))
        pg.mixer.music.load(path.join(sounds_folder, "Morning Mood.mp3"))
        pg.mixer.music.play(loops=-1)

        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((160, 82, 45, 34))
        self.death_timer = 0

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.sheep = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.wolves = pg.sprite.Group()
        self.blood = pg.sprite.Group()
        self.true_sheep = pg.sprite.Group()

        self.speed = 40
        self.bloody = 0
        self.total_sheep = -1
        self.mouse_down = False

        self.map = Map()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'd':
                    Ground(self, col, row)

        self.first_sheep = Sheep(self, WIDTH / 2, HEIGHT / 2)
        self.first_sheep.is_true_sheep = True
        self.first_sheep.add(self.true_sheep)
        for i in range(8):
            Wolf(self, random.randint(50, 80), random.randint(50, 80))
        # start running game loop
        self.run()

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if self.running:
                if event.type == pg.QUIT:
                    self.quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_down = True

            if event.type == pg.MOUSEBUTTONUP:
                self.mouse_down = False

    def update(self):
        if self.mouse_down:
            self.speed = 180

        self.sheep.update()
        self.wolves.update()
        self.blood.update()
        now = pg.time.get_ticks()
        if now - self.tile_timer > 150:
            self.tile_timer = now
            self.tiles.update()
            if self.true_sheep:
                if random.random() > (0.98 - min((.001 * len(self.sheep)), 0.03)):
                    for sheep in self.sheep:
                        sheep.crunch.stop()
                    bleat = random.choice(self.bleats)
                    bleat.play()

        if not self.true_sheep:
            self.death_timer -= 1
            if self.death_timer < 0:
                self.playing = False

        self.speed = 40

    def draw(self):
        self.screenf.fill(DARK_GREEN)
        self.tiles.draw(self.screenf)
        self.sheep.draw(self.screenf)
        self.true_sheep.draw(self.screenf)
        self.wolves.draw(self.screenf)
        self.blood.draw(self.screenf)
        self.screenf = pg.transform.smoothscale(self.screenf, (WIDTH - 40, HEIGHT - 40))
        self.screenf = pg.transform.smoothscale(self.screenf, (WIDTH, HEIGHT))
        self.screen.blit(self.screenf, self.rectf)
        self.screen.blit(self.dim_screen, (0, 0))

        self.draw_text("Total # of Sheep Spawned: {}".format(self.total_sheep), self.hud_font, 40, OFF_WHITE, WIDTH / 2,
                       30)

        pg.display.flip()

    def show_start_screen(self):
        self.screen.fill(BLOOD_RED)
        self.draw_text("Super Fun Sheep", self.hud_font, 120, WHITE, WIDTH / 2, HEIGHT * (2 / 5))
        self.draw_text("Game", self.hud_font, 120, WHITE, WIDTH / 2, HEIGHT * (2.8 / 5))
        self.draw_text("Use the mouse to direct the sheep. Don't let them get eaten by wolves.", self.hud_font, 35,
                       WHITE, WIDTH / 2, HEIGHT * (2 / 3))
        self.draw_text("Click and hold to make them go faster. Get them to eat grass so they have babies.",
                       self.hud_font, 35, WHITE, WIDTH / 2, HEIGHT * (2.1 / 3))
        self.draw_text("Get lots of sheep babies but not too many sheep babies or the game will be glitchy.",
                       self.hud_font, 35, WHITE, WIDTH / 2, HEIGHT * (2.2 / 3))
        self.draw_text("If the lead sheep dies, the rest will get really sad and explode.", self.hud_font, 35, WHITE,
                       WIDTH / 2, HEIGHT * (2.3 / 3))

        self.draw_text("Press Any Key To Begin", self.hud_font, 30, WHITE, WIDTH / 2, HEIGHT * (5 / 6))

        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):

        self.screen.fill(BLOOD_RED)
        self.draw_text("Game Over", self.hud_font, 120, WHITE, WIDTH / 2, HEIGHT * (2 / 5))
        self.draw_text("Press Any Key To Try Again", self.hud_font, 35, WHITE, WIDTH / 2, HEIGHT * (2 / 3))
        self.draw_text("Score: {}".format(self.total_sheep), self.hud_font, 35, WHITE, WIDTH / 2, HEIGHT * (5 / 6))

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

    def quit(self):
        pg.quit()
        sys.exit()


g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
