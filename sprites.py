import random

import pygame
from pygame.math import Vector2
from pygame.draw import rect

from config import (
    JUMP_HEIGHT,
    GRAVITY,
    MAX_FALL_VELOCITY,
    BLOCK_SIZE,
    SCREEN_BLOCKS,
    SCREEN_SIZE,
)
from utils import resize_image


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, image, *groups):
        super().__init__(*groups)
        self.image = image
        self.initial_pos = pos
        self.rect = self.image.get_rect(center=pos)


class Player(Sprite):
    def __init__(self, pos, image, *groups):
        super().__init__(pos, image, *groups)

        self.particles = []

        self.jump_height = JUMP_HEIGHT
        self.velocity = Vector2(0, 0)

        self.jumping = False
        self.on_ground = False

    def jump(self):
        self.velocity.y = -self.jump_height

    def update(self):
        if self.jumping and self.on_ground:
            self.jump()

        if not self.on_ground:
            self.velocity.y = min(self.velocity.y + GRAVITY, MAX_FALL_VELOCITY)

        self.on_ground = False

        self.rect.top += self.velocity.y
        if self.rect.top > BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4 - 1):
            self.rect.top = BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4 - 1)
            self.velocity.y = 0
            self.jumping = False
            self.on_ground = True

        # print(self.velocity.y)

    def draw_particle_trail(self, pos, alpha_surface, color=(255, 255, 255)):
        """draws a trail of particle-rects in a line at random positions behind the player"""
        x, y = pos
        self.particles.append(
            [
                [x - 5, y - 8],
                [random.randint(0, 25) / 10 - 1, random.choice([0, 0])],
                random.randint(5, 8),
            ]
        )

        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.5
            particle[1][0] -= 0.4
            rect(
                alpha_surface,
                color,
                (
                    [int(particle[0][0]), int(particle[0][1])],
                    [int(particle[2]) for i in range(2)],
                ),
            )
            if particle[2] <= 0:
                self.particles.remove(particle)


class Block(Sprite):
    def __init__(self, pos, image, sprite):
        super().__init__(pos, image, sprite)


class Spike(Sprite):
    def __init__(self, pos, image, sprite):
        super().__init__(pos, image, sprite)


class End(Sprite):
    def __init__(self, pos, image, sprite):
        super().__init__(pos, image, sprite)


# class Orb(Sprite):
#     def __init__(self, pos, image, sprite):
#         super().__init__(pos, image, sprite)
