import pygame as pg
import constants as s
import utils as u
import projectile as p


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
        self.projectile_velocity = s.PROJECTILE_VELOCITY

        # physics attributes
        self.speed = init_speed
        self.heading = 0
        self.engine_force = 2
        self.position = pg.Vector2(init_pos)

        # texture
        self.image = u.load_image('player.png', s.PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = init_pos

    def update(self, delta_time, mouse_pos):
        window_position = pg.Vector2(self.rect.center)
        heading_vector = pg.Vector2(mouse_pos) - window_position
        self.heading = heading_vector.angle_to(pg.Vector2(1, 0))

        self.position = self.position + self.speed * delta_time

    def draw(self, screen: pg.Surface):
        rotated_texture = pg.transform.rotate(self.image, self.heading)
        rotated_rect = rotated_texture.get_rect(center=self.rect.center)
        screen.blit(rotated_texture, rotated_rect)

    def propel(self):
        # add the engine force to the speed based on the heading
        self.speed = self.speed + pg.math.Vector2(0, self.engine_force).rotate(self.heading)

    def shoot(self) -> p.Projectile:
        speed_vector = pg.Vector2(self.projectile_velocity, 0).rotate(self.heading)
        return p.Projectile(self.position, speed_vector, 'player')
