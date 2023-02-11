import pygame

from config import PLAYER_IMG_FILENAME, BLOCK_IMG_FILENAME, SPIKE_IMG_FILENAME
from utils import resize_image

player_img = resize_image(pygame.image.load(PLAYER_IMG_FILENAME))
block_img = resize_image(pygame.image.load(BLOCK_IMG_FILENAME))
spike_img = resize_image(pygame.image.load(SPIKE_IMG_FILENAME))

