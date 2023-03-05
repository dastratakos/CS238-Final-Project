import csv
from enum import Enum
import os
from typing import Tuple

import pygame
from pygame.math import Vector2

from config import BLOCK_SIZE, LEVELS


def resize_image(image: pygame.image, size: Tuple[int, int] = (BLOCK_SIZE, BLOCK_SIZE)):
    """Resizes the given image out of place.

    Args:
        image (pygame.image): The image to resize.
        size (Tuple[int, int], optional): The new size. Defaults to
            (BLOCK_SIZE, BLOCK_SIZE).

    Returns:
        pygame.image: The resized image.
    """
    return pygame.transform.smoothscale(image, size)


def close_to_black(color: Tuple[int, int, int]) -> bool:
    r, g, b = color
    return r == g and r == b and r < 50 and g < 50 and b < 50


def fill_player(
    image: pygame.image,
    color1: Tuple[int, int, int],
    color2: Tuple[int, int, int],
):
    """Fills the player image with the given colors. The first color is used for
    the player's body (white pixels) and the second color is used to fill in the
    gaps (transparent pixels).

    Args:
        image (pygame.image): The player image.
        color1 (Tuple[int, int, int]): The primary color.
        color2 (Tuple[int, int, int]): The secondary color.
    """
    w, h = image.get_size()
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    border_width = 3
    for x in range(border_width, w - border_width):
        for y in range(border_width, h - border_width):
            r, g, b, a = image.get_at((x, y))
            if close_to_black((r, g, b)) and a > 60:
                image.set_at((x, y), pygame.Color(0, 0, 0, 255))
            elif (r, g, b) == (0, 0, 0):
                image.set_at((x, y), pygame.Color(r2, g2, b2, a))
            elif a == 0:
                image.set_at((x, y), pygame.Color(r2, g2, b2, 255))
            else:
                image.set_at((x, y), pygame.Color(r1, g1, b1, 255))


def fill_ship(
    image: pygame.image,
    color1: Tuple[int, int, int],
    color2: Tuple[int, int, int],
):
    """Fills the ship image with the given colors. The first color is used for
    the ships's body (white pixels). The second color is unused for now.

    Args:
        image (pygame.image): The player image.
        color1 (Tuple[int, int, int]): The primary color.
        color2 (Tuple[int, int, int]): The secondary color.
    """
    w, h = image.get_size()
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    for x in range(w):
        for y in range(h):
            r, g, b, a = image.get_at((x, y))
            if (r, g, b) == (255, 255, 255):
                image.set_at((x, y), pygame.Color(r1, g1, b1, a))


class FillType(Enum):
    NONE = 1
    PLAYER = 2
    SHIP = 3


def load_image(
    filename: str,
    size: Tuple[int, int] = (BLOCK_SIZE, BLOCK_SIZE),
    fill_type: FillType = FillType.NONE,
    color1: Tuple[int, int, int] = (2, 255, 0),
    color2: Tuple[int, int, int] = (2, 255, 255),
):
    """Loads an image from the given filename, resizes it, and adds color if
    fill_tyep is not FillType.NONE.

    Args:
        filename (str): The image filename.
        size (Tuple[int, int], optional): The size of the output image. Defaults
            to (BLOCK_SIZE, BLOCK_SIZE).
        fill_type (FillType, optional): The type of fill to use, if any.
            Defaults to FillType.NONE.
        color1 (Tuple[int, int, int], optional): The primary color. Defaults to
            (2, 255, 0).
        color2 (Tuple[int, int, int], optional): The secondary color. Defaults
            to (2, 255, 255).

    Returns:
        pygame.image: The loaded image.
    """
    if os.path.exists(filename):
        image = resize_image(pygame.image.load(filename), size)
        match fill_type:
            case FillType.PLAYER:
                fill_player(image, color1, color2)
            case FillType.SHIP:
                fill_ship(image, color1, color2)
        return image
    return None


def load_map(level_id: int):
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


def rotate_image(
    original_image: pygame.image,
    surf_pivot: Vector2,
    image_pivot: Vector2,
    angle: float,
):
    """Sets self.image and self.rect to the rotate position for self.original_image.

    See https://stackoverflow.com/a/59909946 for details.

    Args:
        original_image (pygame.image): The image to rotate.
        surf_pivot (Vector2): The position of the pivot point relative to the surface.
        image_pivot (Vector2): The position of the pivot point relative to the image.
        angle (float): The angle to rotate the image by.
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
