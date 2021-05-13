import pygame as pg
import random
from os import *

game_folder = path.dirname(__file__)
image_folder = path.join(game_folder, "images")
sounds_folder = path.join(game_folder, "sounds")


WIDTH = 900
HEIGHT = 900
FPS = 30
TITLE = "Super Fun Sheep Gamed"

TILESIZE = 15

# colors (r, g, b)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
DARK_GREEN = (0, 80, 0)
MID_GREEN = (70, 125, 40)
LIGHT_GREEN = (100, 125, 60)
BLUE = (0, 0, 255)
PURPLE = (165, 0, 255)
YELLOW = (255, 255, 0)
BLOOD_RED = (138, 3, 3)
NICE_COLOR = (255, 142, 90)
GREY = (105, 105, 105)
WOLF_GREY = (90, 90, 90)
BROWN = (166, 123, 91)
OFF_WHITE = (208, 200, 187)
