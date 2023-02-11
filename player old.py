import pygame
from pygame.math import Vector2

from config import JUMP_HEIGHT
from utils import resize_image


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, image, *groups):
        super().__init__(*groups)

        self.image = image
        self.rect = resize_image(self.image).get_rect(center=pos)
        self.jump_height = JUMP_HEIGHT
        self.velocity = Vector2(0, 0)
    
    def jump(self):
        self.velocity.y = -self.jump_height
    
    def tick(self, objects):
        # self.collide(0, objects) # x-axis collisions
        # self.collide(self.velocity.y, objects) # y-axis collisions
        
        # TODO: return if won or died
        pass
