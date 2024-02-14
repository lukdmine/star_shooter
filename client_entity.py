import pygame as pg
import constants as s
import utils as u
import projectile as p
import enemy_entity as e


class PlayerSpaceShip(pg.sprite.Sprite):
    def __init__(self, init_pos: pg.Vector2 = pg.Vector2(s.WIN_WIDTH // 2, s.WIN_HEIGHT // 2),
                 init_speed: pg.Vector2 = pg.Vector2(0, 0),
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
        # window position (center of the window - remaining the same)
        self.rect.center = pg.Vector2(s.WIN_WIDTH // 2, s.WIN_HEIGHT // 2)

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
        speed_delta = pg.math.Vector2(self.engine_force, 0).rotate(self.heading)
        # pygame y axis is inverted
        speed_delta = pg.Vector2(speed_delta.x, -speed_delta.y)
        new_speed = self.speed + speed_delta
        if new_speed.length() <= s.MAX_SPEED:
            self.speed = new_speed
        else:
            self.speed = new_speed.normalize() * s.MAX_SPEED

    def shoot(self) -> p.Projectile:
        speed_vector = pg.Vector2(self.projectile_velocity, 0).rotate(self.heading)
        # pygame y axis is inverted
        speed_vector = pg.Vector2(speed_vector.x, -speed_vector.y)
        return p.Projectile(self.position, speed_vector, 'player')

    def transform_to_server_player(self):
        return ServerPlayer(self.position, self.hp, self.heading)


class ServerPlayer:
    def __init__(self, init_pos: pg.Vector2, hp: int, heading: int):
        self.hp = hp
        self.heading = heading
        self.position = init_pos
