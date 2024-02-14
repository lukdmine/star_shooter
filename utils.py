import os
import client_entity as p
import projectile as pr
import pygame as pg

import pygame

BASE_IMAGE_PATH = 'data/images/'

def load_image(path: str, size: tuple[int, int] = None) -> pygame.Surface:
    """Load an image from the given path and resize it if needed."""
    image = pygame.image.load(BASE_IMAGE_PATH + path)
    if size:
        image = pygame.transform.scale(image, size)
    image.set_colorkey((0, 0, 0))
    return image


def load_images(path: str, size: tuple[int, int] = None) -> list[pygame.Surface]:
    """Load all images from the given path and resize them if needed."""
    images = []
    for image in os.listdir(BASE_IMAGE_PATH + path):
        images.append(load_image(path + '/' + image, size))
    return images


def pack_player_data(client_entity: 'p.PlayerSpaceShip', projectile: pr.Projectile = None) -> str:
    """Pack the player data into a string."""
    position = f'{int(client_entity.position.x)},{int(client_entity.position.y)}'
    heading = str(client_entity.heading)
    projectile_data = 'f'
    if projectile:
        projectile_data = f't,{int(projectile.position.x)},{int(projectile.position.y)},{int(projectile.speed.x)},{int(projectile.speed.y)}'
    return f'{position}|{heading}|{projectile_data}'


def unpack_player_data(data: str) -> tuple[pg.Vector2, int, tuple[pg.Vector2, pg.Vector2] | None]:
    """Unpack the player data from a string."""
    position, heading, projectile_data = data.split('|')
    position = pg.Vector2(tuple(map(int, position.split(','))))
    heading = int(heading)

    if projectile_data[0] == 'f':
        return position, heading, None

    projectile_data = projectile_data.split(',')
    position = pg.Vector2(tuple(map(int, projectile_data[1:3])))
    heading = int(projectile_data[3])
    return position, heading, projectile_data

