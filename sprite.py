import math
import random

import pygame
from pygame.math import Vector2

from config import (
    BLOCK_SIZE,
    SCREEN_BLOCKS,
    GRAVITY,
    VELOCITY_MAX_FALL,
    VELOCITY_JUMP,
    VELOCITY_JUMP_ORB,
)
from elements import CollisionType, ActionType
from jump_controller import JumpController


class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, *groups):
        super().__init__(*groups)
        self.position = position


class ImageSprite(Sprite):
    def __init__(self, position: tuple, image: pygame.image, *groups):
        super().__init__(position, *groups)
        self.image = image
        self.rect = self.image.get_rect(center=position)


class TiledSprite(ImageSprite):
    """An image sprite that repeats itself to fill the screen. The caller can
    specify a velocity for the image to move to the left.
    """

    def __init__(
        self,
        position: tuple,
        velocity: Vector2,
        image: pygame.image,
        num_siblings: int,
        *groups,
    ):
        super().__init__(position, image, *groups)
        self.velocity = velocity
        self.num_siblings = num_siblings
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def update(self):
        self.position = (self.position[0] - self.velocity.x, self.position[1])
        if self.position[0] <= -self.image.get_width():
            self.position = (
                self.position[0] + self.image.get_width() * self.num_siblings,
                self.position[1],
            )
        self.rect.x = self.position[0]


class ElementSprite(ImageSprite):
    def __init__(
        self,
        position: tuple,
        image: pygame.image,
        collision_type: CollisionType = CollisionType.NONE,
        action_type: ActionType = ActionType.NONE,
        *groups,
    ):
        super().__init__(position, image, *groups)
        self.collision_type = collision_type
        self.action_type = action_type


class Particle(Sprite):
    def __init__(self, position: tuple, velocity: Vector2, ttl: int, *groups):
        super().__init__(position, *groups)
        self.velocity = velocity
        self.ttl = ttl
        self.rect = pygame.Rect(
            self.position[0], self.position[1], self.ttl / 2, self.ttl / 2
        )

    def update(self):
        self.position = tuple(p + v for p, v in zip(self.position, self.velocity))
        self.velocity = (self.velocity[0] - 0.4, self.velocity[1])
        self.ttl -= 1
        self.rect = pygame.Rect(
            self.position[0], self.position[1], self.ttl / 2, self.ttl / 2
        )


class Player(ImageSprite):
    def __init__(
        self,
        position: tuple,
        velocity: Vector2,
        image: pygame.image,
        jump_controller: JumpController,
        *groups,
    ):
        super().__init__(position, image, *groups)

        self.particles = []

        self.velocity = velocity
        self.velocity_jump = VELOCITY_JUMP
        self.velocity_jump_orb = VELOCITY_JUMP_ORB

        self.reverse_gravity = False  # TODO
        self.flying = False  # TODO

        self.should_jump = False
        self.on_ground = False

        self.original_image = image
        self.angle = 0

        self.jump_controller = jump_controller

    def rotate(self):
        if self.angle == 0:
            self.image = self.original_image
            return

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

        # Calculate the upper-left position of the rotated image
        self.position = (
            self.rect.center[0] - BLOCK_SIZE / 2 + x_offset - pivot_move[0],
            self.rect.center[1] - BLOCK_SIZE / 2 - y_offset + pivot_move[1],
        )

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)

    def update_new(self):
        # 1. Update positionition, velocity, and angle
        # 2. Check for collisions
        # 3. Render
        if self.jump_controller.should_jump:
            self.should_jump = True

        if self.should_jump and self.on_ground:
            # perform the jump
            self.should_jump = False
            self.on_ground = False
            self.velocity.y = -self.velocity_jump

        if self.on_ground:
            # Add a particle
            self.particles.append(
                Particle(
                    (self.rect.left - 6, self.rect.bottom - 6),
                    (random.randint(0, 25) / 10 - 1, 0),
                    random.randint(10, 16),
                )
            )
            # Round the angle to the nearest 90 deg
            # print("Old angle: ", self.angle)
            self.angle = 90 * round(self.angle / 90) % 360
            # self.angle = 90 * math.ceil(self.angle / 90) % 360
            # print("New angle: ", self.angle)
            self.rotate()
        else:
            self.velocity.y = min(self.velocity.y + GRAVITY, VELOCITY_MAX_FALL)
            self.angle -= (180 * GRAVITY) / (2 * self.velocity_jump)
            self.rotate()

        self.on_ground = False

        self.rect.top += self.velocity.y
        # if self.rect.top > BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4) - BLOCK_SIZE:
        #     self.rect.top = BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4) - BLOCK_SIZE
        #     self.velocity.y = 0
        #     self.should_jump = False
        #     self.on_ground = True

        # Remove old particles
        for particle in self.particles:
            particle.update()
            if particle.ttl <= 0:
                self.particles.remove(particle)

    def update(self):
        if self.should_jump:
            if self.on_ground:
                self.velocity.y = -self.velocity_jump
            else:  # Don't rotate on the first frame
                # the angle to do a 180 deg turn in one jump
                self.angle -= (180 * GRAVITY) / (2 * self.velocity_jump)
                self.rotate()

        if not self.on_ground:
            self.velocity.y = min(self.velocity.y + GRAVITY, VELOCITY_MAX_FALL)

        # # If jumping, compute the rotated image
        # if self.should_jump:
        #     # the angle to do a 180 deg turn in one jump
        #     self.angle -= (180 * GRAVITY) / (2 * self.velocity_jump)
        #     self.rotate()

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
            # print("Old angle: ", self.angle)
            self.angle = 90 * round(self.angle / 90) % 360
            # self.angle = 90 * math.ceil(self.angle / 90) % 360
            # print("New angle: ", self.angle)
            self.rotate()

        for particle in self.particles:
            particle.update()
            if particle.ttl <= 0:
                self.particles.remove(particle)

        self.on_ground = False

        self.rect.top += self.velocity.y
        if self.rect.top > BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4) - BLOCK_SIZE:
            self.rect.top = BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4) - BLOCK_SIZE
            self.velocity.y = 0
            self.should_jump = False
            self.on_ground = True
