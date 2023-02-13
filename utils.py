import csv
import os

import pygame

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
