import math
import random

import pygame
from pygame.math import Vector2  # TODO: remove Vector2

from config import (
    JUMP_VELOCITY,
    GRAVITY,
    MAX_FALL_VELOCITY,
    BLOCK_SIZE,
    SCREEN_BLOCKS,
)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, image, *groups):
        super().__init__(*groups)
        self.image = image
        self.initial_pos = pos
        self.rect = self.image.get_rect(center=pos)


class Object(Sprite):
    def __init__(self, pos, image, id, *groups):
        super().__init__(pos, image, *groups)
        self.id = id


class Particle:
    def __init__(self, pos, velocity, ttl):
        self.pos = pos
        self.velocity = velocity
        self.ttl = ttl

    def update(self):
        self.pos = tuple(p + v for p, v in zip(self.pos, self.velocity))
        self.velocity = (self.velocity[0] - 0.4, self.velocity[1])
        self.ttl -= 1

    def get_rect(self):
        pos = [int(self.pos[0]), int(self.pos[1])]
        size = [int(self.ttl / 2), int(self.ttl / 2)]
        return (pos, size)


class Player(Sprite):
    def __init__(self, pos, image, *groups):
        super().__init__(pos, image, *groups)

        self.particles = []

        self.velocity_jump = JUMP_VELOCITY
        self.last_velocity_jump = JUMP_VELOCITY
        self.velocity = Vector2(0, 0)

        self.jumping = False
        self.on_ground = False

        self.original_image = image
        self.angle = 0
        self.pos = pos

    def rotate(self):
        rotated_box = [
            Vector2((0, 0)).rotate(self.angle),
            Vector2((BLOCK_SIZE, 0)).rotate(self.angle),
            Vector2((BLOCK_SIZE, -BLOCK_SIZE)).rotate(self.angle),
            Vector2((0, -BLOCK_SIZE)).rotate(self.angle),
        ]
        x_offset = min([point.x for point in rotated_box])
        y_offset = max([point.y for point in rotated_box])

        # Calculate the translation of the pivot
        pivot = Vector2(BLOCK_SIZE / 2, -BLOCK_SIZE / 2)
        pivot_rotate = pivot.rotate(self.angle)
        pivot_move = pivot_rotate - pivot

        # Calculate the upper-left pos of the rotated image
        self.pos = (
            self.rect.center[0] - BLOCK_SIZE / 2 + x_offset - pivot_move[0],
            self.rect.center[1] - BLOCK_SIZE / 2 - y_offset + pivot_move[1],
        )

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)

    def update(self):
        if self.jumping and self.on_ground:
            self.velocity.y = -self.velocity_jump
            self.last_velocity_jump = self.velocity_jump

        if not self.on_ground:
            self.velocity.y = min(self.velocity.y + GRAVITY, MAX_FALL_VELOCITY)

        # If jumping, compute the rotated image
        if self.jumping:
            # the angle to do a 180 deg turn in one jump
            self.angle -= (180 * GRAVITY) / (2 * self.last_velocity_jump)
            self.rotate()

        # Update particle trail
        if self.on_ground:
            self.particles.append(
                Particle(
                    (self.rect.left - 6, self.rect.bottom - 6),
                    (random.randint(0, 25) / 10 - 1, 0),
                    random.randint(10, 16),
                )
            )
            # If on the ground, round the angle to the nearest 90 deg
            self.angle = 90 * math.ceil(self.angle / 90) % 360
            self.rotate()

        for particle in self.particles:
            particle.update()
            if particle.ttl <= 0:
                self.particles.remove(particle)

        self.on_ground = False

        self.rect.top += self.velocity.y
        if self.rect.top > BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4 - 1):
            self.rect.top = BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4 - 1)
            self.velocity.y = 0
            self.jumping = False
            self.on_ground = True
