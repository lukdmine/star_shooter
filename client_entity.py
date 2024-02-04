import pygame as pg
import constants as s
import utils as u


class PlayerSpaceShip(pg.sprite.Sprite):
    def __init__(self, init_pos: tuple[int, int] = (s.WIDTH // 2, s.HEIGHT // 2),
                 init_speed: tuple[int, int] = pg.Vector2(0, 0),
                 init_hp: int = s.PLAYER_HP, init_fuel: int = s.PLAYER_FUEL):
        pg.sprite.Sprite.__init__(self)
        # game attributes
        self.max_hp = init_hp
        self.max_fuel = init_fuel
        self.hp = self.max_hp
        self.fuel = self.max_fuel
        self.projectile_damage = s.BASE_PROJECTILE_DAMAGE

        # physics attributes
        self.speed = init_speed
        self.heading = 0
        self.engine_force = 2

        # texture
        self.image = u.load_image('player.png', s.PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = init_pos

    def update(self, delta_time, mouse_pos):
        # TODO: update the player spaceship position and heading based on the speed
        pass

    def draw(self, screen: pg.Surface):
        rotated_texture = pg.transform.rotate(self.image, self.heading)
        rotated_rect = rotated_texture.get_rect(center=self.rect.center)
        screen.blit(rotated_texture, rotated_rect)

    def propel(self):
        # add the engine force to the speed based on the heading
        self.speed = self.speed + pg.math.Vector2(0, self.engine_force).rotate(self.heading)
