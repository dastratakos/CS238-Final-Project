import pygame

from config import BLOCK_SIZE


def resize_image(image, size=(BLOCK_SIZE, BLOCK_SIZE)):
    return pygame.transform.smoothscale(image, size)
