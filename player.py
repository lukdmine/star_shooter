import pygame as pg
import settings as s
import entity as e

# a class which stores player information
class Player:
    def __init__(self):
        self.spaceship = e.PlayerSpaceShip()
        self.actual_pos: tuple[int, int] = (s.W_WIDTH // 2, s.W_HEIGHT // 2)
        self.score = 0

    def update(self, mouse_pos: tuple[int, int]):
        angle = pg.math.Vector2(mouse_pos[0] - s.WIDTH // 2, mouse_pos[1] - s.HEIGHT // 2).angle_to(pg.math.Vector2(0, -1))
        self.spaceship.set_angle(angle)
        # update the actual position of the player by adding the speed to it
        self.actual_pos = (round(self.actual_pos[0] + self.spaceship.speed[0]), round(self.actual_pos[1] + self.spaceship.speed[1]))


    def draw(self, screen: pg.Surface):
        self.spaceship.draw(screen)


