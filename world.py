import pygame as pg
import settings as s
import entity as e
import player as p

# a class which stores the game world
class World:
    def __init__(self, window: pg.Surface):
        self.player = p.Player()
        self.projectiles = []
        self.enemies = []
        self.window = window
        self.clock = pg.time.Clock()

    def tick(self):
        self.clock.tick(s.FPS)
        self.update()
        self.draw()

    def update(self):
        self.player.update()
        for projectile in self.projectiles:
            projectile.update(self.player)
        for enemy in self.enemies:
            enemy.update(self.player)

    def draw(self):
        self.player.draw(self.window)
        for projectile in self.projectiles:
            projectile.draw(self.window)
        for enemy in self.enemies:
            enemy.draw(self.window)
        pg.display.update()