import pygame as pg
import settings as s
import world as w
import network as n


class Game:
    def __init__(self):
        self.window = pg.display.set_mode((s.WIDTH, s.HEIGHT))
        self.network = n.Network()
        self.world = w.World(self.window, self.network)
        self.playing = False

    def run(self):
        self.network.connect()
        self.playing = True
        while self.playing:
            self.world.tick()
