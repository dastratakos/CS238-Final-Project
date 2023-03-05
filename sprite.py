import math
import random

import pygame
from pygame.math import Vector2

from utils import load_image, resize_image, rotate_image

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
        is_ai: bool,
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
        self.original_ship_image = self.ship_image

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

        self.dead = False
        self.died_at = 0  # Progress at which the player died

        self.is_ai = is_ai

    def add_particle(self):
        self.particles.append(
            Particle(
                (self.rect.left - 6, self.rect.bottom - 6),
                (random.randint(0, 25) / 10 - 1, random.randint(0, 8) / 10 - 1),
                random.randint(10, 16),
            )
        )

    def apply_gravity(self, gravity):
        if not self.gravity_reversed:
            self.velocity.y = min(self.velocity.y + gravity, VELOCITY_MAX_FALL)
        else:
            self.velocity.y = max(self.velocity.y - gravity, -VELOCITY_MAX_FALL)

    def check_collisions_x(self, objects: dict):
        """Checks for collisions in the x direction.

        Args:
            objects (dict): Dictionary from tile coordinates to pygame Sprites.
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                object = objects.get((self.rect.x + x, self.rect.y + y))
                if not object or not pygame.sprite.collide_mask(self, object):
                    continue

                match object.collision_type:
                    case type if type in [
                        CollisionType.SOLID,
                        CollisionType.SOLID_TOP,
                        CollisionType.SOLID_BOTTOM,
                        CollisionType.SPIKE,
                    ]:
                        self.dead = True
                        self.score = self.rect.x
                        self.velocity = Vector2(0, 0)
                        self.rect.right = object.rect.left
                        return
                    case CollisionType.PORTAL_FLY_START:
                        self.flying = True
                    case CollisionType.PORTAL_FLY_END:
                        self.flying = False
                    case CollisionType.PORTAL_GRAVITY_REVERSE:
                        self.gravity_reversed = True
                    case CollisionType.PORTAL_GRAVITY_NORMAL:
                        self.gravity_reversed = False
                    case CollisionType.JUMP_PAD:
                        self.velocity.y = -self.velocity_jump_pad
                    case CollisionType.END:
                        self.won = True
                        self.velocity = Vector2(0, 0)
                        return

    def check_collisions_y(self, objects: dict):
        """Checks for collisions in the y direction.

        Args:
            objects (dict): Dictionary from tile coordinates to pygame Sprites.
        """
        # If the player is at the floor level, there will be no other collisions
        floor_level = 23 * BLOCK_SIZE
        if self.rect.bottom >= floor_level:  # TODO: change based on level
            self.rect.bottom = floor_level
            self.velocity.y = 0
            self.should_jump = False
            self.on_ground = True
            return

        for x in range(-1, 2):
            for y in range(-1, 2):
                object = objects.get(
                    (self.rect.x // BLOCK_SIZE + x, self.rect.y // BLOCK_SIZE + y)
                )
                if not object or not pygame.sprite.collide_mask(self, object):
                    continue

                match object.collision_type:
                    case type if type in [
                        CollisionType.SOLID,
                        CollisionType.SOLID_TOP,
                        CollisionType.SOLID_BOTTOM,
                    ]:
                        if not self.gravity_reversed:
                            if self.velocity.y > 0:  # player is falling
                                self.rect.bottom = object.rect.top + 1
                                self.velocity.y = 0.001
                                self.should_jump = False
                                self.on_ground = True
                            elif self.velocity.y < 0:  # player is jumping
                                self.rect.top = object.rect.bottom
                        else:
                            if self.velocity.y < 0:  # player is falling
                                self.rect.top = object.rect.bottom
                                self.velocity.y = 0.001
                                self.on_ground = True
                                self.should_jump = False
                            elif self.velocity.y > 0:  # player is jumping
                                self.rect.bottom = object.rect.top - 1
                    case CollisionType.SPIKE:
                        self.dead = True
                        self.score = self.rect.x
                        self.velocity = Vector2(0, 0)
                        return

    def update(self, objects: dict):
        """Updates the player.

        Args:
            objects (dict): Dictionary from tile coordinates to pygame Sprites.
        """
        if self.dead:
            return

        # Move x
        self.rect.x += self.velocity.x

        # Check collisions x
        self.check_collisions_x(objects)

        # TODO: ROTATE IMAGE

        # Update velocity.y (gravity, then jumping)
        if not self.flying:
            self.apply_gravity(GRAVITY)
            if self.on_ground:
                self.add_particle()
        else:
            self.apply_gravity(GRAVITY / 2)
            self.add_particle()
        
        if self.jump_controller.should_jump():
            object = objects.get((self.rect.x // BLOCK_SIZE, self.rect.y // BLOCK_SIZE))
            if object and object.collision_type == CollisionType.JUMP_ORB:
                self.velocity.y = self.velocity_jump_orb * (
                    1 if self.gravity_reversed else -1
                )
            elif not self.flying:
                if self.on_ground and not self.gravity_reversed:
                    self.velocity_y = -self.velocity_jump
                elif self.on_ceiling and self.gravity_reversed:
                    self.velocity.y = self.velocity_jump
            else:
                if not self.gravity_reversed:
                    self.velocity.y = max(self.velocity.y + -GRAVITY * 5, -GRAVITY * 5)
                else:
                    self.velocity.y = min(self.velocity.y + GRAVITY * 5, GRAVITY * 5)

        # Move y
        self.rect.y += self.velocity.y
        self.on_ground = False

        # Check collisions y
        self.check_collisions_y(objects)

        # Remove old particles
        for particle in self.particles:
            particle.update()
            if particle.ttl <= 0:
                self.particles.remove(particle)

    def update_old(self):
        # Remove old particles
        for particle in self.particles:
            particle.update()
            if particle.ttl <= 0:
                self.particles.remove(particle)

        if self.dead:
            return

        inputs = [
            # distance to nearest obstacle
            1
            if self.flying
            else 0,
        ]
        if self.jump_controller.should_jump():
            self.should_jump = True

        if self.flying:
            self.apply_gravity(GRAVITY / 2)
            if self.should_jump:
                self.should_jump = False
                self.velocity.y = max(self.velocity.y + -GRAVITY * 5, -GRAVITY * 5)
            self.angle = max(min(self.velocity.y * -2, 20), -20)
            if self.on_ground:
                self.angle = 0

            rotated_image, rotated_image_rect = rotate_image(
                self.original_ship_image,
                self.rect.midleft,
                Vector2(0, BLOCK_SIZE / 2),
                self.angle,
            )
            self.ship_image = rotated_image
            bottom = self.rect.bottom
            self.rect.size = rotated_image_rect.size
            self.rect.bottom = bottom

            self.add_particle()
        else:
            self.apply_gravity(GRAVITY)
            if self.on_ground:
                if self.should_jump:
                    self.should_jump = False
                    self.velocity.y = self.velocity_jump * (
                        1 if self.gravity_reversed else -1
                    )

                self.add_particle()

                # Round the angle to the nearest 90 deg
                angle_radians = math.radians(135 - ((self.angle - 1) % 90 + 1))

                off_x = (BLOCK_SIZE * math.sqrt(2) / 2) * math.cos(angle_radians)
                off_y = (BLOCK_SIZE * math.sqrt(2) / 2) * math.sin(angle_radians)

                curr_angle = self.angle % 360
                next_flat_angle = 90 * round(curr_angle / 90)
                if not math.isclose(curr_angle, next_flat_angle):
                    if curr_angle < next_flat_angle:  # Rotate counter-clockwise
                        self.angle = min(curr_angle + 7.2, next_flat_angle)
                        rotated_image, rotated_image_rect = rotate_image(
                            self.original_image,
                            self.rect.move(off_x, off_y).center,
                            Vector2(BLOCK_SIZE, BLOCK_SIZE),
                            self.angle,
                        )
                    else:  # Rotate clockwise
                        self.angle = max(curr_angle - 7.2, next_flat_angle)
                        rotated_image, rotated_image_rect = rotate_image(
                            self.original_image,
                            self.rect.move(off_x, off_y).center,
                            Vector2(0, BLOCK_SIZE),
                            self.angle,
                        )
                    self.image = rotated_image
                    bottom = self.rect.bottom
                    self.rect.size = rotated_image_rect.size
                    self.rect.bottom = bottom
            else:
                # Rotate the player
                # self.angle -= (180 * GRAVITY) / (2 * self.velocity_jump)
                # self.angle -= 8.1712
                self.angle -= 7.2
                rotated_image, rotated_image_rect = rotate_image(
                    self.original_image,
                    self.rect.center,
                    Vector2(BLOCK_SIZE / 2, BLOCK_SIZE / 2),
                    self.angle,
                )
                self.image = rotated_image
                bottom = self.rect.bottom
                self.rect.size = rotated_image_rect.size
                self.rect.bottom = bottom

        # Move the player
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Reset the on_ground flag. It will be set again in play.check_collisions()
        self.on_ground = False
