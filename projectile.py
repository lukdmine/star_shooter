import pygame as pg
import constants as s
import utils as u


class Projectile(pg.sprite.Sprite):
    def __init__(self, init_pos: pg.Vector2, init_speed: pg.Vector2, origin: str):  # origin can be 'player' or 'enemy'
        pg.sprite.Sprite.__init__(self)
        # physics attributes
        self.speed = init_speed
        self.position = init_pos

        # texture
        self.image = self.load_image(origin)
        self.rect = self.image.get_rect()
        self.rect.center = init_pos

    def update(self, delta_time: float, player_pos: pg.Vector2):
        #TODO: update the projectile position based on the speed
        #TODO: update the window position based on the player position
        self.position = self.position + self.speed * delta_time

    def draw(self, screen: pg.Surface):
        rotated_texture = pg.transform.rotate(self.image, self.heading)
        rotated_rect = rotated_texture.get_rect(center=self.rect.center)
        screen.blit(rotated_texture, rotated_rect)

    def load_image(self, origin):
        if origin == 'player':
            return u.load_image('player_projectile.png', s.PROJECTILE_SIZE)
        else:
            return u.load_image('enemy_projectile.png', s.PROJECTILE_SIZE)
