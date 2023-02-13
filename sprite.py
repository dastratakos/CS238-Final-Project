import math
import random

import pygame
from pygame.math import Vector2

from utils import load_image, resize_image

from config import (
    BLOCK_SIZE,
    GRAVITY,
    VELOCITY_MAX_FALL,
    VELOCITY_JUMP,
    VELOCITY_JUMP_PAD,
    VELOCITY_JUMP_ORB,
    CollisionType,
)
from jump_controller import JumpController


class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, *groups):
        super().__init__(*groups)
        self.position = position


class ImageSprite(Sprite):
    def __init__(self, position: tuple, image: pygame.image, *groups):
        super().__init__(position, *groups)
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        centered_position = (
            position[0] + image.get_width() / 2,
            position[1] + image.get_height() / 2,
        )
        self.rect = self.image.get_rect(center=centered_position)


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
        velocity: Vector2,
        image: pygame.image,
        collision_type: CollisionType = CollisionType.NONE,
        *groups,
    ):
        super().__init__(position, image, *groups)
        self.velocity = velocity

        self.collision_type = collision_type

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y


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
        ship_image: pygame.image,
        jump_controller: JumpController,
        *groups,
    ):
        super().__init__(position, image, *groups)

        # Build ship image
        self.ship_image = load_image("assets/ships/blank.png")
        self.ship_image.blit(
            resize_image(image, (BLOCK_SIZE / 2, BLOCK_SIZE / 2)),
            (BLOCK_SIZE / 4, BLOCK_SIZE / 4),
        )
        self.ship_image.blit(ship_image, (0, 0))

        self.particles = []

        self.velocity = velocity
        self.velocity_jump = VELOCITY_JUMP
        self.velocity_jump_pad = VELOCITY_JUMP_PAD
        self.velocity_jump_orb = VELOCITY_JUMP_ORB

        self.gravity_reversed = False
        self.flying = False

        self.should_jump = False
        self.on_ground = False

        self.original_image = image
        self.angle = 0

        self.jump_controller = jump_controller

    def rotate_image(self, pivot: Vector2):
        return
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
        pivot_rotate = pivot.rotate(self.angle)
        pivot_move = pivot_rotate - pivot

        # Calculate the upper-left position of the rotated image
        self.position = (
            self.rect.center[0] - BLOCK_SIZE / 2 + x_offset - pivot_move[0],
            self.rect.center[1] - BLOCK_SIZE / 2 - y_offset + pivot_move[1],
        )

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)

    def add_particle(self):
        self.particles.append(
            Particle(
                (self.rect.left - 6, self.rect.bottom - 6),
                (random.randint(0, 25) / 10 - 1, random.randint(0, 8) / 10 - 1),
                random.randint(10, 16),
            )
        )

    def apply_gravity(self):
        if not self.gravity_reversed:
            self.velocity.y = min(self.velocity.y + GRAVITY, VELOCITY_MAX_FALL)
        else:
            self.velocity.y = max(self.velocity.y - GRAVITY, -VELOCITY_MAX_FALL)

    def update(self):
        if self.jump_controller.should_jump():
            self.should_jump = True

        if self.flying:
            if self.should_jump:
                self.should_jump = False
                self.velocity.y = -GRAVITY * 7

            self.add_particle()
            self.apply_gravity()
        else:
            if self.on_ground:
                if self.should_jump:
                    # Perform the jump
                    self.should_jump = False
                    self.velocity.y = self.velocity_jump * (
                        1 if self.gravity_reversed else -1
                    )

                self.add_particle()

                # Round the angle to the nearest 90 deg
                # TODO: fix glitch where cube goes below ground
                # TODO: rotate instead of jumping to that angle
                old_angle = self.angle % 360
                self.angle = 90 * round(self.angle / 90) % 360

                pivot = Vector2(BLOCK_SIZE / 2, -BLOCK_SIZE / 2)
                self.rotate_image(pivot)

                # top_left = Vector2(0, 0)
                # top_right = Vector2(0, BLOCK_SIZE)
                # center = Vector2(BLOCK_SIZE / 2, BLOCK_SIZE / 2)
                # bottom_left = Vector2(0, BLOCK_SIZE)
                # bottom_right = Vector2(BLOCK_SIZE, BLOCK_SIZE)
                # self.rotate_image(bottom_right if old_angle < self.angle else bottom_left)
            else:
                self.apply_gravity()

                # Rotate the player
                # self.angle -= (180 * GRAVITY) / (2 * self.velocity_jump)
                # self.angle -= 8.1712
                self.angle -= 7.2
                pivot = Vector2(BLOCK_SIZE / 2, -BLOCK_SIZE / 2)
                self.rotate_image(pivot)

        # Remove old particles
        for particle in self.particles:
            particle.update()
            if particle.ttl <= 0:
                self.particles.remove(particle)

        # Move the player
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Reset the on_ground flag. It will be set again in play.check_collisions()
        self.on_ground = False
