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
