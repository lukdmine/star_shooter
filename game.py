import pygame as pg
import settings as s
import world as w


class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((s.WIDTH, s.HEIGHT))
        self.world = w.World(self.window)
        self.playing = False

    def run(self):
        self.playing = True
        while self.playing:
            self.world.tick()
