import csv
import os
import random

import pygame
from pygame.math import Vector2
from pygame.draw import rect

from config import (
    SCREEN_SIZE,
    BLOCK_SIZE,
    VELOCITY_X,
    BACKGROUND_IMG_FILENAME,
    PLAYER_IMG_FILENAME,
    BLOCK_IMG_FILENAME,
    SPIKE_IMG_FILENAME,
)
from player import Player
from sprites import Sprite
from utils import resize_image


class Camera:
    def __init__(self, pos):
        self.x, self.y = pos


player_img = resize_image(pygame.image.load(PLAYER_IMG_FILENAME))
block_img = resize_image(pygame.image.load(BLOCK_IMG_FILENAME))
spike_img = resize_image(pygame.image.load(SPIKE_IMG_FILENAME))

player_sprite = pygame.sprite.Group()
objects = pygame.sprite.Group()


def load_level(filename):
    with open(filename, "r") as file:
        map = csv.reader(file)

        x, y = 0, 0
        for row in map:
            for cell in row:
                if cell == "block":
                    Sprite((x, y), block_img, objects)
                if cell == "spike":
                    Sprite((x, y), spike_img, objects)
                x += BLOCK_SIZE
            x = 0
            y += BLOCK_SIZE


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Geometry Dash AI")
    pygame.display.set_icon(player)
    clock = pygame.time.Clock()
    # music = pygame.mixer_music.load(os.path.join("music", "bossfight-Vextron.mp3"))
    # pygame.mixer_music.play()
    background = pygame.image.load(BACKGROUND_IMG_FILENAME)
    alpha_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    load_level("./maps/1.csv")

    player = Player((150, 150), player_img, player_sprite)

    started = False
    exit = False
    while not exit:
        keys = pygame.key.get_pressed()

        # TODO: loading screen

        player.velocity.x = VELOCITY_X

        # if keys[pygame.K_SPACE]:
        #     player.jump()

        player_sprite.update()

        # Move map
        for sprite in objects:
            sprite.rect.x -= VELOCITY_X

        # Redraw
        screen.blit(background, (0, 0))
        player_sprite.draw(screen)
        objects.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit = True
    
        # pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
