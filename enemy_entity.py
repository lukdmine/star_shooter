import pygame as pg
import constants as s
import utils as u
import uuid


class EnemySpaceShip(pg.sprite.Sprite):
    def __init__(self, enemy_id: uuid.UUID, init_pos: pg.Vector2, hp: int, heading: int):
        pg.sprite.Sprite.__init__(self)
        # game attributes
        self.hp = hp
        self.id = enemy_id

        # physics attributes
        self.heading = heading
        self.position = pg.Vector2(init_pos)

        # texture
        self.image = u.load_image('enemy.png', s.PLAYER_SIZE)
        self.original_image = self.image
        self.rect = self.image.get_rect()
        # pygame window position (has to be updated according to the player position)
        self.rect.center = init_pos

    def update(self, new_pos: pg.Vector2, new_hp: int, new_heading: int, player_pos: pg.Vector2):
        self.position = new_pos
        # window position updated based on player position
        self.rect.center = self.position - player_pos + pg.Vector2(s.WIN_WIDTH // 2, s.WIN_HEIGHT // 2)
        self.hp = new_hp
        self.heading = new_heading
        self.image = pg.transform.rotate(self.original_image, self.heading)
        self.rect = self.image.get_rect(center=self.rect.center)


class ServerSpaceShip:
    def __init__(self, enemy_id: uuid.UUID, init_pos: pg.Vector2, hp: int, heading: int):
        self.hp = hp
        self.id = enemy_id
        self.heading = heading
        self.position = init_pos

    def update(self, new_pos: pg.Vector2, new_hp: int, new_heading: int):
        self.position = new_pos
        self.hp = new_hp
        self.heading = new_heading

    def transform_to_client_enemy(self):
        return EnemySpaceShip(self.id, self.position, self.hp, self.heading)
