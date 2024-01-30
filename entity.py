import pygame as pg
import settings as s
import player as p


class Entity:
    def __init__(self, init_pos: tuple[int, int], init_speed: tuple[int, int],
                 init_size: tuple[int, int]):
        self.position = init_pos
        self.speed = init_speed
        self.rect = pg.Rect(self.position, init_size)

    def update(self, player: 'p.Player'):
        self.position = (self.position[0] + self.speed[0]
                         - player.spaceship.speed[0],
                         self.position[1] + self.speed[1]
                         - player.spaceship.speed[1])

    def draw(self, screen: pg.Surface):
        pass


class Spaceship(Entity):
    def __init__(self, init_pos: tuple[int, int], init_speed: tuple[int, int],
                 init_hp: int, init_fuel: int, init_size: tuple[int, int]):
        super().__init__(init_pos, init_speed, init_size)
        self.max_hp = init_hp
        self.max_fuel = init_fuel
        self.hp = self.max_hp
        self.fuel = self.max_fuel


class Projectile(Entity):
    def __init__(self, init_pos: tuple[int, int], init_speed: tuple[int, int],
                 init_damage: int):
        super().__init__(init_pos, init_speed)
        self.damage = init_damage
