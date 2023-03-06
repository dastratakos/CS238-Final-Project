import pygame

from components.rounded_rect import RoundedRect
from components.text import Text


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        font_size=36,
        text_color=(255, 255, 255),
        color=(98, 0, 238),  # (79, 175, 7),
        hover_color=(173, 122, 246),  # (239, 243, 247),
        border_radius=10,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color
        self.rect = pygame.Rect(x, y, width, height)
        self.border_radius = border_radius

    def draw(self, screen):
        # Check if the mouse is hovering over the button
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        RoundedRect(
            self.x, self.y, self.width, self.height, color, self.border_radius
        ).draw(screen)

        Text(
            self.text,
            self.font_size,
            self.text_color,
            center=(self.x + self.width // 2, self.y + self.height // 2),
        ).draw(screen)
