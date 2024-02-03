import os

import pygame

BASE_IMAGE_PATH = 'data/images/'

def load_image(path: str, size: tuple[int, int] = None) -> pygame.Surface:
    """Load an image from the given path and resize it if needed."""
    image = pygame.image.load(BASE_IMAGE_PATH + path)
    image.set_colorkey((0, 0, 0))
    return image


def load_images(path: str, size: tuple[int, int] = None) -> list[pygame.Surface]:
    """Load all images from the given path and resize them if needed."""
    images = []
    for image in os.listdir(BASE_IMAGE_PATH + path):
        images.append(load_image(path + '/' + image, size))
    return images


def pack_player_data(pos: tuple[int, int]) -> str:
    return f'{pos[0]},{pos[1]}'


def unpack_player_data(data: str) -> tuple[int, int]:
    return tuple(map(int, data.split(',')))
