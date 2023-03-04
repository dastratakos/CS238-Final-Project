import csv
import os

import pygame
from pygame.math import Vector2

from config import BLOCK_SIZE, LEVELS


def resize_image(image, size=(BLOCK_SIZE, BLOCK_SIZE)):
    return pygame.transform.smoothscale(image, size)


def load_image(filename, size=(BLOCK_SIZE, BLOCK_SIZE)):
    return resize_image(pygame.image.load(filename), size)


def load_map(level_id):
    filename = LEVELS[level_id]["filename"]
    with open(filename) as f:
        reader = csv.reader(f)
        map = []
        for row in reader:
            r = []
            for cell in row:
                r.append(cell)
            map.append(r)
    return map


def get_sprite_image(filename, size=(BLOCK_SIZE, BLOCK_SIZE)):
    if os.path.exists(filename):
        return load_image(filename, size=size)
    return None

def rotate_image(original_image, surf_pivot, image_pivot, angle):
    """Sets self.image and self.rect to the rotate position for self.original_image.

    See https://stackoverflow.com/a/59909946 for details.

    Args:
        original_image (pygame.image): The image to rotate
        surf_pivot (Vector2): The position of the pivot point relative to the surface
        image_pivot (Vector2): The position of the pivot point relative to the image
        angle (float): The angle to rotate the image by
    """
    image_rect = original_image.get_rect(
        topleft=(surf_pivot[0] - image_pivot[0], surf_pivot[1] - image_pivot[1])
    )
    offset_center_to_pivot = Vector2(surf_pivot) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (
        surf_pivot[0] - rotated_offset.x,
        surf_pivot[1] - rotated_offset.y,
    )
    rotated_image = pygame.transform.rotate(original_image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    return rotated_image, rotated_image_rect
