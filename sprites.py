import pygame
from pygame.math import Vector2

from config import JUMP_HEIGHT, GRAVITY, MAX_FALL_VELOCITY, BLOCK_SIZE
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

        self.jump_height = JUMP_HEIGHT
        self.velocity = Vector2(0, 0)

        self.jumping = False
        self.on_ground = False

    def jump(self):
        self.velocity.y = -self.jump_height

    def update(self):
        if self.jumping and self.on_ground:
            self.jump()

        if not self.on_ground and False:
            self.velocity.y = min(self.velocity.y + GRAVITY, MAX_FALL_VELOCITY)

        self.rect.top += self.velocity.y
        self.rect.top = min(self.rect.top, BLOCK_SIZE * 18.5)

        self.on_ground = False

        # print(self.velocity.y)


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
