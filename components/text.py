from typing import Tuple

import pygame

pygame.Rect


class Text:
    def __init__(
        self,
        text: str,
        font_size: int = 20,
        color: Tuple[int, int, int] = (255, 255, 255),
        x: int = None,
        y: int = None,
        top: int = None,
        left: int = None,
        bottom: int = None,
        right: int = None,
        topleft: Tuple[int, int] = None,
        bottomleft: Tuple[int, int] = None,
        topright: Tuple[int, int] = None,
        bottomright: Tuple[int, int] = None,
        midtop: Tuple[int, int] = None,
        midleft: Tuple[int, int] = None,
        midbottom: Tuple[int, int] = None,
        midright: Tuple[int, int] = None,
        center: Tuple[int, int] = None,
        centerx: int = None,
        centery: int = None,
        size: Tuple[int, int] = None,
        width: int = None,
        height: int = None,
        w: int = None,
        h: int = None,
    ):
        self.text = text
        self.font_size = font_size
        self.color = color

        self.x = x
        self.y = y
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.topleft = topleft
        self.bottomleft = bottomleft
        self.topright = topright
        self.bottomright = bottomright
        self.midtop = midtop
        self.midleft = midleft
        self.midbottom = midbottom
        self.midright = midright
        self.center = center
        self.centerx = centerx
        self.centery = centery
        self.size = size
        self.width = width
        self.height = height
        self.w = w
        self.h = h

    def draw(self, screen):
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.text, True, self.color)

        rect = text.get_rect()
        if self.x:
            rect.x = self.x
        if self.y:
            rect.y = self.y
        if self.top:
            rect.top = self.top
        if self.left:
            rect.left = self.left
        if self.bottom:
            rect.bottom = self.bottom
        if self.right:
            rect.right = self.right
        if self.topleft:
            rect.topleft = self.topleft
        if self.bottomleft:
            rect.bottomleft = self.bottomleft
        if self.topright:
            rect.topright = self.topright
        if self.bottomright:
            rect.bottomright = self.bottomright
        if self.midtop:
            rect.midtop = self.midtop
        if self.midleft:
            rect.midleft = self.midleft
        if self.midbottom:
            rect.midbottom = self.midbottom
        if self.midright:
            rect.midright = self.midright
        if self.center:
            rect.center = self.center
        if self.centerx:
            rect.centerx = self.centerx
        if self.centery:
            rect.centery = self.centery
        if self.size:
            rect.size = self.size
        if self.width:
            rect.width = self.width
        if self.height:
            rect.height = self.height
        if self.w:
            rect.w = self.w
        if self.h:
            rect.h = self.h

        screen.blit(text, rect)
