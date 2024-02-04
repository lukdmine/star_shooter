import pygame as pg
import constants as s
import utils as u


class EnemySpaceShip(pg.sprite.Sprite):
    def __init__(self, enemy_id, init_pos: tuple[int, int], hp: int, heading: int):
        pg.sprite.Sprite.__init__(self)
        # game attributes
        self.hp = hp
        self.id = enemy_id

        # physics attributes
        self.heading = heading
        self.position = pg.Vector2(init_pos)

        # texture
        self.image = u.load_image('enemy.png', s.PLAYER_SIZE)
        self.rect = self.image.get_rect()
        # pygame window position (has to be updated according to the player position)
        self.rect.center = init_pos

    def update(self, new_pos: pg.Vector2, new_hp: int, new_heading: int):
        self.position = new_pos
        self.hp = new_hp
        self.heading = new_heading
