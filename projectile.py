import pygame as pg
import constants as s
import utils as u
import uuid


class Projectile(pg.sprite.Sprite):
    def __init__(self, init_pos: pg.Vector2, init_speed: pg.Vector2, origin: str, damage: int = s.BASE_PROJECTILE_DAMAGE):  # origin can be 'player' or 'enemy'
        pg.sprite.Sprite.__init__(self)
        # physics attributes
        self.speed = init_speed
        self.position = init_pos
        self.damage = damage
        self.id = uuid.uuid4()

        # texture
        self.image = self.load_image(origin)
        self.rect = self.image.get_rect()
        self.rect.center = init_pos

    def update(self, delta_time: float, player_pos: pg.Vector2):
        #TODO: update the projectile position based on the speed
        #TODO: update the window position based on the player position
        self.position = self.position + self.speed * delta_time
        self.rect.center = self.position - player_pos + pg.Vector2(s.WIN_WIDTH // 2, s.WIN_HEIGHT // 2)

    def transform_to_server_projectile(self):
        return ServerProjectile(self.position, self.speed, self.damage, self.id)

    def draw(self, screen: pg.Surface):
        # TODO: draw only if the projectile is in the window
        if self.rect.colliderect(screen.get_rect()):
            screen.blit(self.image, self.rect)

    def load_image(self, origin):
        if origin == 'player':
            return u.load_image('player_projectile.png', s.PROJECTILE_SIZE)
        else:
            return u.load_image('enemy_projectile.png', s.PROJECTILE_SIZE)


class ServerProjectile:
    def __init__(self, init_pos: pg.Vector2, init_speed: pg.Vector2, damage: int, pro_id: uuid.UUID):
        self.speed = init_speed
        self.position = init_pos
        self.damage = damage
        self.id = pro_id

    def update(self, dt):
        self.position = self.position + self.speed * dt

    def transform_to_client_projectile(self):
        return Projectile(self.position, self.speed, 'enemy')
