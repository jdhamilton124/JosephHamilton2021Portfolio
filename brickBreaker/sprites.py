import pygame as pg
import random
from os import *
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, game):
        self.groups = game.all_sprites, game.paddles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((80, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT * (7 / 8))
        self.vel = vec(0, 0)
        self.rect.center = self.pos


    def update(self):

        self.vel.x = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT] or keystate[pg.K_a]:
            self.vel.x = -13
        if keystate[pg.K_RIGHT] or keystate[pg.K_d]:
            self.vel.x = 13

        self.pos.x += self.vel.x
        self.rect.center = self.pos

        # bind to the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


class Block(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((34, 34))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health = 3
        self.timer = 0
        self.game = game

    def update(self):
        if self.health >= 3:
            self.image.fill(GREEN)
        elif self.health >= 2:
            self.image.fill(YELLOW)
        elif self.health >= 1:
            self.image.fill(RED)
        else:
            bla = random.choice(self.game.crunches)
            bla.play()
            for i in range(185):
                BloodDrop(self.game, self.rect.center, 5)
            self.kill()

    def take_damage(self):
        now = pg.time.get_ticks()
        if now - self.timer > 100:
            self.timer = now
            self.health -= 1

class BloodDrop(pg.sprite.Sprite):
    def __init__(self, game, center, range):
        self.groups = game.all_sprites, game.blood
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.speedy = random.randint(-2 - range, 2 + range)
        self.speedx = random.randint(min(-1 - range + abs(self.speedy), -1), max(1 - abs(self.speedy) + range, 1))
        self.speedy += 5
        self.image = pg.Surface((35, 35))
        self.image.fill(BLOOD_RED)
        self.rect = self.image.get_rect()
        self.num = 15
        self.image = pg.transform.scale(self.image, (self.num, self.num))
        self.rect.center = center

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if random.random() > 0.60:
            self.num -= 2
            if self.num <= 5:
                self.kill()
            self.image = pg.transform.scale(self.image, (self.num, self.num))
        if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT:
            self.kill()


class Ball(pg.sprite.Sprite):

    def __init__(self, game):
        self.groups = game.all_sprites, game.balls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((15, 15))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT * (2 / 3))
        self.vel = vec(random.uniform(-2, 2), 8)
        self.rect.center = self.pos
        self.alive = True
        self.respawn_timer = 0
        self.bounce_timer = 0

    def update(self):

        if self.alive == False:
            self.respawn()
        else:
            self.pos.x += self.vel.x
            self.pos.y += self.vel.y

            self.rect.center = self.pos

            if self.rect.right > WIDTH:
                self.vel.x = -self.vel.x
            if self.rect.left < 0:
                self.vel.x = -self.vel.x
            if self.rect.top > HEIGHT:
                self.respawn_timer = pg.time.get_ticks()
                self.alive = False
            if self.rect.top < 0:
                self.vel.y = -self.vel.y

            hits = pg.sprite.spritecollide(self, self.game.paddles, False)
            for hit in hits:
                self.vel.y = -self.vel.y
                self.vel.x = ((hit.vel.x / 4) + self.vel.x + ((self.pos.x - hit.pos.x) / 2)) / 2

            hits = pg.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                adjusted = False
                if self.rect.centery + 4 < hits[0].rect.centery - 13:
                    adjusted = True
                    self.vel.y = -self.vel.y
                if self.rect.centery - 4 > hits[0].rect.centery + 13:
                    adjusted = True
                    self.vel.y = -self.vel.y
                if self.rect.centerx + 4 < hits[0].rect.centerx - 13:
                    adjusted = True
                    self.vel.x = -self.vel.x
                if self.rect.centerx - 4 > hits[0].rect.centerx + 13:
                    adjusted = True
                    self.vel.x = -self.vel.x
                if not adjusted:
                    self.vel = -self.vel
                for hit in hits:
                    hit.take_damage()

    def respawn(self):
        now = pg.time.get_ticks()
        if now - self.respawn_timer > 1500:
            self.pos = vec(WIDTH / 2, HEIGHT * (2 / 3))
            self.vel = vec(random.uniform(-2, 2), 8)
            self.rect.center = self.pos
            self.game.lives -= 1
            self.alive = True
