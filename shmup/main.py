import pygame as pg
import random as r
import math
from os import *


# Game Credits
####################################################################
# Programmed by Joe Hamilton
# Ship and explosions from "Kenney.nl" or "www.kenney.nl"
# Other images from Google
####################################################################

# Game object classes
####################################################################

class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = player_img
        self.image = pg.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(WHITE)
        # self.image = pg.Surface((50,40))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIDTH / 2)
        self.rect.bottom = (HEIGHT - (HEIGHT * .05))
        self.speedx = 0
        self.shield = 100
        self.fuel = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.shoot_delay = 200
        self.last_shot = pg.time.get_ticks()
        self.powerlevel = 1
        self.power_timer = pg.time.get_ticks()

    def update(self):
        # time out for powerups
        if self.powerlevel >= 2 and pg.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.powerlevel -= 2
            self.power_timer = pg.time.get_ticks()
            if self.powerlevel < 1:
                self.powerlevel = 1

        if self.hidden and pg.time.get_ticks() - self.hide_timer > 4000:
            self.hidden = False
            self.rect.centerx = (WIDTH / 2)
            self.rect.bottom = (HEIGHT - (HEIGHT * .05))
            self.shield = 100
            self.fuel = 100

        self.speedx = 0
        keystate = pg.key.get_pressed()
        if (keystate[pg.K_LEFT] or keystate[pg.K_a]) and not self.hidden:
            self.speedx = -12
            self.fuel -= .4
        if (keystate[pg.K_RIGHT] or keystate[pg.K_d]) and not self.hidden:
            self.fuel -= .4
            self.speedx = 12

        if self.fuel < 0:
            self.speedx = 0
            self.fuel = 0

        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

        if keystate[pg.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay and not self.hidden:
            self.last_shot = now
            if self.powerlevel == 1:
                b = Bullet(self.rect.centerx, self.rect.top - 1)
                bullet_group.add(b)
                all_sprites.add(b)
                shoot_sound.play()
            if self.powerlevel == 2:
                b = Bullet(self.rect.left, self.rect.centery)
                bullet_group.add(b)
                all_sprites.add(b)
                b = Bullet(self.rect.right, self.rect.centery)
                bullet_group.add(b)
                all_sprites.add(b)
                shoot_sound.play()
            if self.powerlevel == 3:
                b = Bullet(self.rect.centerx, self.rect.top - 1)
                bullet_group.add(b)
                all_sprites.add(b)
                b = Bullet(self.rect.left, self.rect.centery)
                bullet_group.add(b)
                all_sprites.add(b)
                b = Bullet(self.rect.right, self.rect.centery)
                bullet_group.add(b)
                all_sprites.add(b)
                shoot_sound.play()
            if self.powerlevel >= 4:
                b = Bullet(self.rect.centerx, self.rect.top - 1)
                b.spread = -0
                bullet_group.add(b)
                all_sprites.add(b)
                b = Bullet(self.rect.centerx, self.rect.top - 1)
                b.spread = -1
                bullet_group.add(b)
                all_sprites.add(b)
                b = Bullet(self.rect.centerx, self.rect.top - 1)
                b.spread = 1
                bullet_group.add(b)
                all_sprites.add(b)
                b = Bullet(self.rect.left, self.rect.centery)
                b.spread = -2
                bullet_group.add(b)
                all_sprites.add(b)
                b = Bullet(self.rect.right, self.rect.centery)
                b.spread = 2
                bullet_group.add(b)
                all_sprites.add(b)
                shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.lives -= 1
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 1500)

    def get_hit(self, radius):
        self.change_shield(-radius)

    def change_shield(self, amount):
        self.shield += amount
        if self.shield >= 100:
            self.shield = 100

    def change_fuel(self, amount):
        self.fuel += amount
        if self.fuel >= 100:
            self.fuel = 100

    def gun_pow(self):
        self.powerlevel += 1
        if self.powerlevel > 4:
            self.powerlevel = 4
        self.power_timer = pg.time.get_ticks()


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.image = bullet_img
        self.image = pg.transform.scale(self.image, (140, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width) * .75 / 7
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        self.spread = 0

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.spread
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size, rot):
        super(Explosion, self).__init__()
        self.size = size
        self.image = exp_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50
        self.image.set_alpha(256)
        self.rotate = rot
        all_sprites.add(self)

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(exp_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = exp_anim[self.size][self.frame]
                self.image = pg.transform.rotate(self.image, self.rotate * self.frame)
                self.image.set_alpha(256 * (4 / self.frame))
                self.rect = self.image.get_rect()
                self.rect.center = center


class NPC(pg.sprite.Sprite):
    def __init__(self):
        super(NPC, self).__init__()
        # self.image = pg.Surface((25,25))
        # self.image.fill(RED)
        self.image_orig = enemy_img
        # self.image_orig = r.choice(enemy_images)
        num = r.randint(20, 100)
        self.image_orig = pg.transform.scale(self.image_orig, (num, num))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width) * .75 / 2
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect = self.image.get_rect()
        self.rect.centerx = (r.randint(0, WIDTH))
        self.rect.bottom = 0
        self.speedx = r.randint(-10 + level, 10 + level)
        self.speedy = r.randint(1 + level, r.randint(2, r.randint(3, 5)) + level) - self.speedx
        if self.speedy <= 0:
            self.speedy = 1
        self.rot = 0
        self.rot_speed = r.randint(-8, 8)
        self.last_update = pg.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT:
            self.reset()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 20:
            self.last_update = now
            # rotate sprite
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def reset(self):
        self.rect.centerx = (r.randint(0, WIDTH))
        self.rect.bottom = 0
        self.speedx = r.randint(-5, 5)
        self.speedy = r.randint(5, r.randint(8, 25)) - self.speedx


class Star(pg.sprite.Sprite):
    def __init__(self):
        super(Star, self).__init__()
        self.speedy = r.randint(10, 15)
        self.image = pg.Surface(((35 / self.speedy), ((35 / self.speedy) * 3)))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.centerx = (r.randint(0, WIDTH))
        self.rect.bottom = 0

    def update(self):
        self.rect.y += self.speedy

        if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        self.rect.centerx = (r.randint(0, WIDTH))
        self.rect.bottom = 0
        self.speedy = r.randint(7, 15)
        self.image = pg.Surface(((25 / self.speedy), ((35 / self.speedy) * 3)))
        self.image.fill(WHITE)
        self.image.set_colorkey(BLACK)


class BloodDrop(pg.sprite.Sprite):
    def __init__(self, center, x, y):
        super(BloodDrop, self).__init__()
        self.speedy = r.randint(-5, 5)
        self.speedx = r.randint(min(-5 + abs(self.speedy), -1), max(5 - abs(self.speedy), 1))
        self.speedy += y
        self.speedx += x
        self.image = blood_drop_img.copy()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.num = 35
        self.image = pg.transform.scale(self.image, (self.num, self.num))
        self.num2 = 5
        self.rect.center = center
        self.alpha = 255

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx


        if r.random() > 0.60:
            self.num -= self.num2
            self.num2 += 1
            if self.num <= 6:
                self.kill()
            self.image = pg.transform.scale(self.image, (self.num, self.num))

        if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT:
            self.kill()


class Collectables(pg.sprite.Sprite):
    def __init__(self, center, x, y):
        super(Collectables, self).__init__()
        self.type = r.choice(powTypes)
        self.image = powerup_imgs[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = y
        self.speedx = x

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT:
            self.kill()


####################################################################


# Game Constants
####################################################################
HEIGHT = 900
WIDTH = 600
FPS = 60

# Colors (R,G,B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

POWERUP_TIME = 6000

creator = "Joe Hamilton Programing 2 4/5 2021"

font_name = pg.font.match_font('arial')

title = "Shmup"

powTypes = ["gun", "shield", "fuel"]
powChance = ["shield", "shield", "fuel", "fuel", "fuel", "fuel", "fuel", "gun", "shield", "gun"]

game_folder = path.dirname(__file__)
imgs_folder = path.join(game_folder, "imgs")
player_imgs = path.join(imgs_folder, "player_imgs")
enemy_imgs = path.join(imgs_folder, "enemy_imgs")
background_imgs = path.join(imgs_folder, "background_imgs")
bullet_imgs = path.join(imgs_folder, "bullet_imgs")
animation_folder = path.join(imgs_folder, "animations")
pows_folder = path.join(imgs_folder, "pows")

scores_folder = path.join(game_folder, "scores")
snds_folder = path.join(game_folder, "snds")


####################################################################

# Game Functions
####################################################################
def spawn_npc():
    npc = NPC()
    npc_group.add(npc)
    all_sprites.add(npc)


def draw_text(surf, text, size, x, y, color):
    font = pg.font.Font(font_name, size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surf, text_rect)


def draw_bar(surf, x, y, pct, color):
    if pct < 0:
        pct = 0
    bar_len = 250
    bar_height = 20
    fill = (pct / 100) * bar_len
    outline = pg.Rect(x, y, bar_len, bar_height)
    fillrect = pg.Rect(x, y, fill, bar_height)
    pg.draw.rect(surf, color, fillrect)
    pg.draw.rect(surf, WHITE, outline, 3)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, title, 64, WIDTH/2, HEIGHT/4, WHITE)
    draw_text(screen, "Created by " + creator, 22, WIDTH/2, HEIGHT/2, WHITE)
    draw_text(screen, "Arrow keys to move, Space to fire", 18, WIDTH/2, HEIGHT*3/4, WHITE)
    draw_text(screen, "Press a key to begin", 18, WIDTH/2, HEIGHT*7/8, WHITE)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False



####################################################################

# initialize pygame and create window
####################################################################
pg.init()
pg.mixer.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(title)
clock = pg.time.Clock()
####################################################################

# load imgs
####################################################################
# background image
background = pg.image.load(path.join(background_imgs, "stars.jpg")).convert()
background = pg.transform.scale(background, (int(WIDTH * 1.9), HEIGHT))
background_rect = background.get_rect()
# player image
player_img = pg.image.load(path.join(player_imgs, "ship.png")).convert()
# health image
player_mini_img = pg.transform.scale(player_img, (28, 21))
player_mini_img.set_colorkey(WHITE)
# npc image
enemy_img = pg.image.load(path.join(enemy_imgs, "kitten-removebg-preview.png")).convert()
# bullet image
bullet_img = pg.image.load(path.join(bullet_imgs, "weasel-removebg-preview.png")).convert()
# blood drop image
blood_drop_img = pg.image.load(path.join(background_imgs, "BloodDrop.png")).convert()
# explosion images
exp_anim = {}
exp_anim["lg"] = []
exp_anim["sm"] = []
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    img = pg.image.load(path.join(animation_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pg.transform.scale(img, (130, 130))
    exp_anim["lg"].append(img_lg)
    img_sm = pg.transform.scale(img, (75, 75))
    exp_anim["sm"].append(img_sm)

# powerups
powerup_imgs = {}
for i in range(len(powTypes)):
    fn = "img_{}.png".format(i)
    powerup_imgs[powTypes[i]] = pg.image.load(path.join(pows_folder, fn)).convert()
    if i == 2:
        powerup_imgs[powTypes[i]].set_colorkey(WHITE)
        powerup_imgs[powTypes[i]] = pg.transform.scale(powerup_imgs[powTypes[i]], (88, 33))
    else:
        powerup_imgs[powTypes[i]].set_colorkey(BLACK)
        powerup_imgs[powTypes[i]] = pg.transform.scale(powerup_imgs[powTypes[i]], (33, 33))





# enemy_images = []
# enemy_list = ["fluffy.png", "small.png", "other.png"]
# for img in enemy_list:
#     enemy_images.append(pg.image.load(path.join(enemy_imgs, img)).convert())

####################################################################

# load snds
####################################################################
shoot_sound = pg.mixer.Sound(path.join(snds_folder, "TubularBell3.wav"))
expl_snds = []
for snd in ["Explosion 5.wav", "Explosion 1.wav", "Explosion 2.wav"]:
    expl_snds.append(pg.mixer.Sound(path.join(snds_folder, snd)))

shield_snd = pg.mixer.Sound(path.join(snds_folder, "SquareMotif2.wav"))
gun_snd = pg.mixer.Sound(path.join(snds_folder, "SquareMotif3.wav"))
fuel_snd = pg.mixer.Sound(path.join(snds_folder, "SquareMotif5.wav"))


pg.mixer.music.load(path.join(snds_folder, "WeirdSynth.ogg"))
pg.mixer.music.set_volume(0.4)

####################################################################



# Game Loop
###################
# game update Variables
########################################
playing = True
game_over = True
score = 0
level = 1
diff = 0
pg.mixer.music.play(loops=-1)

########################################
################################################################
while playing:
    if game_over:
        show_go_screen()
        game_over = False
        # create Sprite groups
        ####################################################################
        all_sprites = pg.sprite.Group()
        players_group = pg.sprite.Group()
        npc_group = pg.sprite.Group()
        bullet_group = pg.sprite.Group()
        star_group = pg.sprite.Group()
        collectable_group = pg.sprite.Group()
        ####################################################################
        # create Game Objects
        ####################################################################
        score = 0
        level = 1
        level_counter = 0
        player = Player()
        for i in range(13):
            npc = NPC()
            npc_group.add(npc)
        for i in range(119):
            star = Star()
            star_group.add(star)
        ####################################################################
        # add objects to sprite groups
        ####################################################################
        players_group.add(player)
        for i in star_group:
            all_sprites.add(i)
        for i in players_group:
            all_sprites.add(i)
        for i in npc_group:
            all_sprites.add(i)
        ####################################################################

    # timing
    ##################################################
    clock.tick(FPS)
    ##################################################

    # collecting Input
    ##################################################

    # Quiting the game when we hit the x
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                playing = False
        if event.type == pg.QUIT:
            playing = False
        # if event.type == pg.KEYDOWN:
        #     if event.key == pg.K_SPACE:
        #         player.shoot()

    ##################################################
    # Updates
    ##################################################
    level_counter += 1
    if level_counter > 500:
        level += 1
        spawn_npc()
        level_counter = 0

    # checking for hit between player and NPC
    hits = pg.sprite.spritecollide(player, npc_group, True, pg.sprite.collide_circle)
    if hits:
        exp = Explosion(hits[0].rect.center, "sm",  hits[0].rot_speed)
        r.choice(expl_snds).play()
        spawn_npc()
        player.get_hit(hits[0].radius)
        if player.shield <= 0:
            exp = Explosion(player.rect.center, "lg", 0)
            player.hide()
            if player.lives <= 0:  # and (not exp.alive()):
                game_over = True

    # checking if bullet hits NPC
    hits = pg.sprite.groupcollide(npc_group, bullet_group, True, True, pg.sprite.collide_circle)
    for hit in hits:
        # exp = Explosion(hit.rect.center, size, hit.rot_speed)
        for i in range(int(hit.radius * 10)):
            blood = BloodDrop(hit.rect.center, hit.speedx, hit.speedy)
            all_sprites.add(blood)
        r.choice(expl_snds).play()
        score += 50 - int(hit.radius)
        if r.random() > 0.85:
            pow = Collectables(hit.rect.center, hit.speedx, hit.speedy)
            collectable_group.add(pow)
            all_sprites.add(pow)
        spawn_npc()

    hits = pg.sprite.spritecollide(player, collectable_group, True)
    for hit in hits:
        if hit.type == "shield":
            num = r.random() * 4
            player.change_shield((100 - player.shield) / num)
            shield_snd.play()
        if hit.type == "gun":
            player.gun_pow()
            gun_snd.play()
        if hit.type == "fuel":
            player.change_fuel(50)
            fuel_snd.play()


    all_sprites.update()
    ##################################################
    # Render
    ##################################################

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    # draw HUD
    draw_bar(screen, 5, 15, player.shield, RED)
    draw_bar(screen, 5, 35, player.fuel, GREEN)
    draw_text(screen, "Score: " + str(score), 40, WIDTH * (3 / 4), 15, WHITE)
    draw_text(screen, "Difficulty: " + str(level), 40, WIDTH * (3 / 4), 55, WHITE)
    draw_lives(screen, WIDTH - 100, 100, player.lives, player_mini_img)

    pg.display.flip()
    ##################################################

pg.quit()
################################################################
#####################
