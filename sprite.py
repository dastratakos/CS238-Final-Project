from __future__ import annotations
import math
import random
from typing import TYPE_CHECKING

import pygame
from pygame.math import Vector2


from config import (
    BLOCK_SIZE,
    GRAVITY,
    VELOCITY_MAX_FALL,
    VELOCITY_JUMP,
    VELOCITY_JUMP_PAD,
    VELOCITY_JUMP_ORB,
    CollisionType,
)
from utils import load_image, resize_image, rotate_image

if TYPE_CHECKING:
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
        image: pygame.image,
        collision_type: CollisionType = CollisionType.NONE,
        *groups,
    ):
        super().__init__(position, image, *groups)
        self.collision_type = collision_type


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
        jump_controller: JumpController = None,
        render_particles: bool = True,
        angle: int = 0,
        gravity_reversed: bool = False,
        flying: bool = False,
        on_ground: bool = False,
        on_ceiling: bool = False,
        sprite_groups: list[pygame.sprite.Group] = [],
    ):
        super().__init__(position, image, *sprite_groups)

        self.original_image = image

        self.ship_image = self.build_ship_image(image, ship_image)
        self.original_ship_image = self.ship_image

        self.particles = []
        self.render_particles = render_particles

        self.velocity = velocity
        self.angle = angle

        self.gravity_reversed = gravity_reversed
        self.flying = flying
        self.on_ground = on_ground
        self.on_ceiling = on_ceiling  # TODO: do something with this (e.g. when flying)

        self.jump_controller = jump_controller
        self.should_jump = False

        self.dead = False
        self.score = 0  # x position when the player died

    def clone(self):
        return Player(
            self.rect,
            self.velocity,
            self.original_image,
            self.original_ship_image,
            render_particles=False,
            angle=self.angle,
            gravity_reversed=self.gravity_reversed,
            flying=self.flying,
            on_ground=self.on_ground,
            on_ceiling=self.on_ceiling,
        )

    def build_ship_image(self, image: pygame.image, ship_image: pygame.image):
        """Returns a new pygame.image with the player sitting inside the ship.

        Args:
            image (pygame.image): The player image.
            ship_image (pygame.image): The ship image.

        Returns:
            pygame.image: The new image.
        """
        new_image = load_image("assets/ships/blank.png")
        new_image.blit(
            resize_image(image, (BLOCK_SIZE / 2, BLOCK_SIZE / 2)),
            (BLOCK_SIZE / 4, BLOCK_SIZE / 4),
        )
        new_image.blit(ship_image, (0, 0))
        return new_image

    def add_particle(self):
        if not self.render_particles:
            return
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

    def check_collisions_x(self, element_map: dict):
        """Checks for collisions in the x direction.

        Args:
            element_map (dict): Dictionary from tile coordinates to pygame Sprites.
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                tile_coord = (
                    self.rect.center[0] // BLOCK_SIZE + x,
                    self.rect.center[1] // BLOCK_SIZE + y,
                )
                element = element_map.get(tile_coord)
                if not element or not pygame.sprite.collide_mask(self, element):
                    continue

                match element.collision_type:
                    case type if type in [
                        CollisionType.SOLID,
                        CollisionType.SOLID_TOP,
                        CollisionType.SOLID_BOTTOM,
                        CollisionType.SPIKE,
                    ]:
                        self.dead = True
                        self.score = self.rect.x
                        self.velocity = Vector2(0, 0)
                        self.rect.right = element.rect.left
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
                        self.velocity.y = -VELOCITY_JUMP_PAD
                    case CollisionType.END:
                        self.won = True
                        self.velocity = Vector2(0, 0)
                        return

    def check_collisions_y(self, element_map: dict, floor_level: int):
        """Checks for collisions in the y direction.

        Args:
            element_map (dict): Dictionary from tile coordinates to pygame Sprites.
            floor_level (int): The y coordinate of the floor.
        """
        # If on the floor level, there will be no other y collisions
        if self.rect.bottom >= floor_level:
            self.rect.bottom = floor_level
            self.velocity.y = 0
            self.on_ground = True
            return

        for x in range(-1, 2):
            for y in range(-1, 2):
                tile_coord = (
                    self.rect.center[0] // BLOCK_SIZE + x,
                    self.rect.center[1] // BLOCK_SIZE + y,
                )
                element = element_map.get(tile_coord)
                if not element or not pygame.sprite.collide_mask(self, element):
                    continue

                match element.collision_type:
                    case type if type in [
                        CollisionType.SOLID,
                        CollisionType.SOLID_TOP,
                        CollisionType.SOLID_BOTTOM,
                    ]:
                        if not self.gravity_reversed:
                            if self.velocity.y > 0:  # player is falling
                                self.rect.bottom = element.rect.top
                                self.velocity.y = 0
                                self.on_ground = True
                            elif self.velocity.y < 0:  # player is jumping
                                self.rect.top = element.rect.bottom
                        else:
                            if self.velocity.y < 0:  # player is falling
                                self.rect.top = element.rect.bottom
                                self.velocity.y = 0
                                self.on_ground = True
                            elif self.velocity.y > 0:  # player is jumping
                                self.rect.bottom = element.rect.top
                    case CollisionType.SPIKE:
                        self.dead = True
                        self.score = self.rect.x
                        self.velocity = Vector2(0, 0)
                        return

    def update(self, element_map: dict, floor_level: int):
        """Updates the player.

        Args:
            element_map (dict): Dictionary from tile coordinates to pygame Sprites.
            floor_level (int): The y coordinate of the floor.
        """
        if self.render_particles:
            # Remove old particles
            for particle in self.particles:
                particle.update()
                if particle.ttl <= 0:
                    self.particles.remove(particle)

        if self.dead:
            return

        # Move x
        self.rect.x += self.velocity.x

        # Check collisions x
        self.check_collisions_x(element_map)

        # Update velocity.y with gravity
        if not self.flying:
            self.apply_gravity(GRAVITY)
            if self.on_ground:
                self.add_particle()
        else:
            self.apply_gravity(GRAVITY / 2)
            self.add_particle()

        # Update velocity.y with jump
        if self.should_jump:
            tile_coord = (self.rect.x // BLOCK_SIZE, self.rect.y // BLOCK_SIZE)
            element = element_map.get(tile_coord)
            if element and element.collision_type == CollisionType.JUMP_ORB:
                self.velocity.y = VELOCITY_JUMP_ORB * (
                    1 if self.gravity_reversed else -1
                )
            elif not self.flying:
                if self.on_ground and not self.gravity_reversed:
                    self.velocity.y = -VELOCITY_JUMP
                elif self.on_ceiling and self.gravity_reversed:
                    self.velocity.y = VELOCITY_JUMP
            else:
                if not self.gravity_reversed:
                    self.velocity.y = max(self.velocity.y + -GRAVITY * 5, -GRAVITY * 5)
                else:
                    self.velocity.y = min(self.velocity.y + GRAVITY * 5, GRAVITY * 5)

        # Update angle, surf_pivot, and image_pivot
        surf_pivot, image_pivot = None, None
        if self.on_ground:
            # Rotate the player to the nearest 90 degrees
            angle_radians = math.radians(135 - ((self.angle - 1) % 90 + 1))

            off_x = (BLOCK_SIZE * math.sqrt(2) / 2) * math.cos(angle_radians)
            off_y = (BLOCK_SIZE * math.sqrt(2) / 2) * math.sin(angle_radians)

            curr_angle = self.angle % 360
            next_flat_angle = 90 * round(curr_angle / 90)
            if not math.isclose(curr_angle, next_flat_angle):
                if curr_angle < next_flat_angle:  # Rotate counter-clockwise
                    self.angle = min(curr_angle + 7.2, next_flat_angle)
                    surf_pivot = self.rect.move(off_x, off_y).center
                    image_pivot = Vector2(BLOCK_SIZE, BLOCK_SIZE)
                else:  # Rotate clockwise
                    self.angle = max(curr_angle - 7.2, next_flat_angle)
                    surf_pivot = self.rect.move(off_x, off_y).center
                    image_pivot = Vector2(0, BLOCK_SIZE)
        elif self.flying:
            self.angle = max(min(self.velocity.y * -2, 20), -20)
            surf_pivot = self.rect.midleft
            image_pivot = Vector2(0, BLOCK_SIZE / 2)
        else:  # not on the ground and not flying (i.e., spinning in air)
            self.angle -= 7.2
            surf_pivot = self.rect.center
            image_pivot = Vector2(BLOCK_SIZE / 2, BLOCK_SIZE / 2)

        # Rotate image
        if surf_pivot and image_pivot:
            rotated_image, rotated_image_rect = rotate_image(
                self.original_ship_image if self.flying else self.original_image,
                surf_pivot,
                Vector2(BLOCK_SIZE / 2, BLOCK_SIZE / 2),
                self.angle,
            )
            if self.flying:
                self.ship_image = rotate_image
                self.mask = pygame.mask.from_surface(self.ship_image)
            else:
                self.image = rotated_image
                self.mask = pygame.mask.from_surface(self.image)
            bottom = self.rect.bottom
            self.rect.size = rotated_image_rect.size
            self.rect.bottom = bottom

        # Move y. We are using round() to avoid floating point errors when
        # self.velocity.y = GRAVITY = 0.86 because on_ground would not be True.
        self.rect.y += round(self.velocity.y)
        self.on_ground = False

        # Check collisions y
        self.check_collisions_y(element_map, floor_level)

        # Reset should_jump
        self.should_jump = False
