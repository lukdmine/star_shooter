import pygame as pg
import settings as s
import player as p
import utils as u

ASSETS = {
    'player': u.load_image('player.png', s.PLAYER_SIZE),
    'p_projectile': u.load_image('player_projectile.png', s.PROJECTILE_SIZE),
    'e_projectile': u.load_image('enemy_projectile.png', s.PROJECTILE_SIZE),
    'enemy': u.load_image('enemy.png', s.PLAYER_SIZE)
}


class Entity(pg.sprite.Sprite):
    def __init__(self, init_pos: tuple[int, int], init_speed: tuple[int, int],
                 init_size: tuple[int, int], texture: pg.Surface):
        pg.sprite.Sprite.__init__(self)
        self.image = texture
        self.speed = init_speed
        self.rect = self.image.get_rect()
        # pygame window position
        self.rect.center = init_pos
        self.heading = 0

    def update(self, player: 'p.Player'):
        self.rect.move_ip(self.speed[0] - player.spaceship.speed[0],
                          self.speed[1] - player.spaceship.speed[1])

    def draw(self, screen: pg.Surface):
        rotated_texture = pg.transform.rotate(self.image, self.heading)
        rotated_rect = rotated_texture.get_rect(center=self.rect.center)
        screen.blit(rotated_texture, rotated_rect)

    def set_angle(self, angle: float):
        self.heading = angle


class Spaceship(Entity):
    def __init__(self, init_pos: tuple[int, int], init_speed: tuple[int, int],
                 init_hp: int, init_fuel: int, init_size: tuple[int, int], texture: pg.Surface,
                 projectile_damage: int = s.BASE_PROJECTILE_DAMAGE):
        super().__init__(init_pos, init_speed, init_size, texture)
        self.max_hp = init_hp
        self.max_fuel = init_fuel
        self.hp = self.max_hp
        self.fuel = self.max_fuel
        self.projectile_damage = projectile_damage


class PlayerSpaceShip(Spaceship):
    def __init__(self, init_pos: tuple[int, int] = (s.WIDTH // 2, s.HEIGHT // 2),
                 init_speed: tuple[int, int] = (0, 0),
                 init_hp: int = s.PLAYER_HP, init_fuel: int = s.PLAYER_FUEL,
                 init_size: tuple[int, int] = s.PLAYER_SIZE, texture: pg.Surface = ASSETS['player']):
        super().__init__(init_pos, init_speed, init_hp, init_fuel, init_size, texture)
        self.engine_force = 2

    def update(self, player: 'p.Player'):
        # player spaceship does not move on its own
        pass

    def propel(self):
        # add the engine force to the speed based on the heading
        self.speed = pg.math.Vector2(self.speed[0], self.speed[1]) + pg.math.Vector2(0, self.engine_force).rotate(self.heading)
        print(self.speed)


class Enemy(Spaceship):
    def __init__(self, init_pos: tuple[int, int], init_speed: tuple[int, int],
                 init_hp: int = s.PLAYER_HP, init_fuel: int = s.PLAYER_FUEL, init_size: tuple[int, int] = s.PLAYER_SIZE,
                 texture=ASSETS['enemy']):
        super().__init__(init_pos, init_speed, init_hp, init_fuel, init_size, texture)


class Projectile(Entity):
    def __init__(self, init_pos: tuple[int, int], init_angle: int,
                 init_damage: int, init_size, texture: pg.Surface):
        init_speed = pg.math.Vector2(0, s.PROJECTILE_VELOCITY).rotate(init_angle)
        init_speed = (int(init_speed[0]), int(-init_speed[1]))
        super().__init__(init_pos, init_speed, init_size, texture)
        self.damage = init_damage


class PlayerProjectile(Projectile):
    def __init__(self, init_pos: tuple[int, int], init_damage: int, init_angle,
                 init_size: tuple[int, int] = s.PROJECTILE_SIZE):
        super().__init__(init_pos, init_angle, init_damage, init_size, ASSETS['p_projectile'])
