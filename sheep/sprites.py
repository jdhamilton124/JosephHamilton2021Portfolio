from math import *

import pygame as pg
import random
from os import *
from settings import *

vec = pg.math.Vector2


class Sheep(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.sheep
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_original = game.sheep_image
        self.true_image_original = game.true_sheep_image
        self.image_original.set_colorkey(BLACK)
        self.true_image_original.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image_original, (39, 39))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.wool = 0
        self.dewool = False
        self.spawn_timer = 0
        self.game.total_sheep += 1
        self.is_true_sheep = False
        self.radius = int(self.rect.width) * .5 / 2
        self.crunch = self.game.crunches[1]

    def avoid_sheep(self):
        for sheep in self.game.sheep:
            if sheep != self:
                dist = self.pos - sheep.pos
                if 0 < dist.length() < 17:
                    self.acc += dist.normalize()

    def update(self):
        if self.is_true_sheep:
            target = vec(pg.mouse.get_pos())
            self.game.head = self.pos
        else:
            target = self.game.head
        target_dist = target - self.pos
        if (10 > target_dist.x > -10) and (10 > target_dist.y > -10):
            close_to_mouse = True
        else:
            close_to_mouse = False

        if not close_to_mouse:
            self.rot = target_dist.angle_to(vec(1, 0))
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            if not self.is_true_sheep:
                self.avoid_sheep()
            try:
                self.acc.scale_to_length(self.game.speed)
            except:
                self.acc = (5, 5)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt

        # Eat
        if self.game.speed > 40:
            if self.wool > 30:
                self.wool -= 10
        else:
            hits = pg.sprite.spritecollide(self, self.game.tiles, False)
            for hit in hits:
                if hit.grassed > 0:
                    if not self.dewool:
                        self.wool += hit.grassed
                        self.crunch = random.choice(self.game.crunches)
                        self.crunch.play()
                        if self.wool > 100:
                            if self.game.death_timer <= 0:
                                self.spawn_sheep()
                                self.dewool = True
                                self.wool = 100
                    hit.grassed = 0
                    hit.update_grass()

        if self.dewool:
            self.wool -= 10
            if self.wool <= 40:
                self.wool = 41
                self.dewool = False

        if 0 < self.game.death_timer:
            if self.wool <= 1:
                self.wool = 2
            self.wool *= 1.1
            self.rot += self.wool
            if self.wool > 200:
                self.crunch.stop()
                self.game.splat.play()
                scream = random.choice(self.game.screams)
                scream.play()
                for i in range(75):
                    BloodDrop(self.game, self.rect.center, 35)
                self.kill()

        if self.is_true_sheep:
            self.image = pg.transform.scale(self.true_image_original, (int(19 + self.wool / 5), int(19 + self.wool / 5)))
        else:
            self.image = pg.transform.scale(self.image_original, (int(19 + self.wool / 5), int(19 + self.wool / 5)))
        self.image = pg.transform.rotate(self.image, self.rot + 270)

    def spawn_sheep(self):
        now = pg.time.get_ticks()
        if now - self.spawn_timer > 1000:
            self.spawn_timer = now
            Sheep(self.game, self.pos.x + 1, self.pos.y + 1)


class Ground(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.grassed = 3
        self.ske = random.randint(2, 6)
        self.rot = random.choice((0, 90, 180, 270))
        self.image = self.game.ground_images[self.grassed]
        self.image = pg.transform.scale(self.image, (TILESIZE + self.ske, TILESIZE + self.ske))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.is_bloody = False

    def update(self):
        if self.grassed < 3:
            if random.random() > 0.99:
                if self.is_bloody:
                    self.is_bloody = False
                else:
                    self.grassed += 1
                    self.update_grass()



    def update_grass(self):
        if self.is_bloody:
            self.image = self.game.blood_image
            self.image = pg.transform.smoothscale(self.image, (TILESIZE + self.ske, TILESIZE + self.ske))
            self.image = pg.transform.rotate(self.image, self.rot)
        else:
            self.image = self.game.ground_images[self.grassed]
            self.image = pg.transform.smoothscale(self.image, (TILESIZE + self.ske, TILESIZE + self.ske))
            self.image = pg.transform.rotate(self.image, self.rot)



class Wolf(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.wolves
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_original = game.wolf_image
        self.image = pg.transform.smoothscale(self.image_original, (55, 55))
        self.image_original.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(random.randint(10, 200), random.randint(10, 200))
        self.rot = atan2(-self.vel.x, -self.vel.y) * 57.29578
        self.rect.center = self.pos
        self.wool = 0
        self.dewool = False
        self.spawn_timer = 0
        self.radius = int(self.rect.width) * .75 / 2
        self.not_bouncy = 0

    def update(self):

        if self.not_bouncy < 0:
            if self.rect.right > WIDTH:
                self.vel.x = -self.vel.x
                self.not_bouncy = 10
            if self.rect.left < 0:
                self.vel.x = -self.vel.x
                self.not_bouncy = 10
            if self.rect.bottom > HEIGHT:
                self.vel.y = -self.vel.y
                self.not_bouncy = 10
            if self.rect.top < 0:
                self.vel.y = -self.vel.y
                self.not_bouncy = 10

        self.not_bouncy -= 1


        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos



        # Eat
        hits = pg.sprite.spritecollide(self, self.game.sheep, False, pg.sprite.collide_circle)
        for hit in hits:
            self.wool += hit.wool
            if hit.is_true_sheep:
                self.game.death_timer = 80
                for i in range(75):
                    BloodDrop(self.game, self.rect.center, 10)
            hit.kill()
            for i in range(15):
                BloodDrop(self.game, self.rect.center, 0)
            hit.crunch.stop()
            self.game.splat.play()
            scream = random.choice(self.game.screams)
            scream.play()


        if self.wool > 100:
            self.spawn_wolf()
            self.dewool = True
            self.wool = 99

        if self.dewool:
            self.wool -= 10
            if self.wool <= 40:
                self.wool = 41
                self.dewool = False

        self.rot = (3 * self.rot + atan2(-self.vel.x, -self.vel.y) * 57.29578) / 4

        self.image = pg.transform.smoothscale(self.image_original, (int(53 + self.wool / 10), int(53 + self.wool / 10)))
        self.image = pg.transform.rotate(self.image, self.rot)


    def spawn_wolf(self):
        now = pg.time.get_ticks()
        if now - self.spawn_timer > 1000:
            self.spawn_timer = now
            Wolf(self.game, self.pos.x + 1, self.pos.y + 1)

class BloodDrop(pg.sprite.Sprite):
    def __init__(self, game, center, range):
        self.groups = game.all_sprites, game.blood
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.speedy = random.randint(-2 - range, 2 + range)
        self.speedx = random.randint(min(-2 - range + abs(self.speedy), -1), max(2 - abs(self.speedy) + range, 1))
        self.image = pg.Surface((35, 35))
        self.image.fill(BLOOD_RED)
        self.rect = self.image.get_rect()
        self.num = 6
        self.image = pg.transform.scale(self.image, (self.num, self.num))
        self.rect.center = center

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if random.random() > 0.60:
            self.num -= 1
            if self.num <= 5:
                hits = pg.sprite.spritecollide(self, self.game.tiles, False)
                if hits:
                    hits[0].is_bloody = True
                    hits[0].update_grass()
                self.kill()
            self.image = pg.transform.scale(self.image, (self.num, self.num))
        if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT:
            self.kill()
