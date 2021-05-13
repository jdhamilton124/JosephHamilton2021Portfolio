import pygame as pg
import random
from os import path

game_folder = path.dirname(__file__)
image_folder = path.join(game_folder, "images")
image_folder = path.join(game_folder, "sounds")


WIDTH = 480
HEIGHT = 600
FPS = 30
TITLE = "Platformer"
FONT = 'vivaldi'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"


# player properties
PLAYER_ACC = 2.5
PLAYER_FRICTION = -0.2
PLAYER_GRAV = 0.68
JUMP = -20

BOOST_POWER = 60
POW_SPAWN_PCT = 7
MOB_FRQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0


PLATFORM_LIST = [(0, HEIGHT - 70),
                 (30, HEIGHT * 3 / 4),
                 (125, HEIGHT * 4 / 8),
                 (300, 400),
                 (60, 120)]

# colors (r, g, b)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (150, 180, 210)
PURPLE = (165, 0, 255)
YELLOW = (255, 255, 0)
BLOOD_RED = (138, 3, 3)
NICE_COLOR = (255, 142, 90)
GREY = (105, 105, 105)