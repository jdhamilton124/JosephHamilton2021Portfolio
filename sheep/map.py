import pygame as pg
from settings import *

class Map:
    def __init__(self):
        self.data = []
        for i in range(int(HEIGHT / TILESIZE)):
            line = []
            for s in range(int(WIDTH / TILESIZE)):
                line.append("d")
            self.data.append(line)

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
