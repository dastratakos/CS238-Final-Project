from __future__ import annotations

import pygame
from pygame.math import Vector2


from config import CollisionType


class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, *groups):
        super().__init__(*groups)
        self.position = position


class ImageSprite(Sprite):
    def __init__(self, position: tuple, image: pygame.Surface, *groups):
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
        image: pygame.Surface,
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
        image: pygame.Surface,
        collision_type: CollisionType = CollisionType.NONE,
        *groups,
    ):
        super().__init__(position, image, *groups)
        self.collision_type = collision_type
