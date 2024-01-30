import pygame as pg
import settings as s
import entity as e

# a class which stores player information
class Player:
    def __init__(self):
        self.spaceship = e.Spaceship((s.WIDTH // 2, s.HEIGHT // 2),
                                     (0, 0), s.PLAYER_HP, s.PLAYER_FUEL, s.PLAYER_SIZE)
        self.score = 0

    def update(self):
        pass

    def draw(self, screen: pg.Surface):
        pass


