import pygame
from pygame.math import Vector2

from config import JUMP_HEIGHT, GRAVITY, MAX_FALL_VELOCITY
from utils import resize_image

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, image, *groups):
        super().__init__(*groups)
        self.image = image
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
        
        if not self.on_ground:
            self.velocity.y = min(self.velocity.y + GRAVITY, MAX_FALL_VELOCITY)
        
        # Check for collisions
        # self.collide(0, objects) # x-axis collisions
        # self.collide(self.velocity.y, objects) # y-axis collisions
        
        self.rect.top += self.velocity.y


# class Block(Sprite):
#     def __init__(self, pos, image, sprite):
#         super().__init__(pos, image, sprite)


# class Spike(Sprite):
#     def __init__(self, pos, image, sprite):
#         super().__init__(pos, image, sprite)


# class Orb(Sprite):
#     def __init__(self, pos, image, sprite):
#         super().__init__(pos, image, sprite)
