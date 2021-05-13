import pygame as pg
import random
from os import *

game_folder = path.dirname(__file__)
image_folder = path.join(game_folder, "images")
sounds_folder = path.join(game_folder, "sounds")

WIDTH = 600
HEIGHT = 480
FPS = 30
TITLE = "Block Breaker"

# colors (r, g, b)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (165, 0, 255)
YELLOW = (255, 255, 0)
BLOOD_RED = (138, 3, 3)
NICE_COLOR = (255, 142, 90)
GREY = (105, 105, 105)