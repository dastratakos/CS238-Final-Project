import pygame

from components.text import Text


class RoundedRect:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        color=(79, 175, 7),
        border_radius=10,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = pygame.Color(color)
        self.rect = pygame.Rect(x, y, width, height)
        self.border_radius = border_radius

    def draw(self, screen):
        # top left corner
        pygame.draw.circle(
            screen,
            self.color,
            (self.x + self.border_radius, self.y + self.border_radius),
            self.border_radius,
        )
        # top right corner
        pygame.draw.circle(
            screen,
            self.color,
            (self.x + self.width - self.border_radius, self.y + self.border_radius),
            self.border_radius,
        )
        # bottom left corner
        pygame.draw.circle(
            screen,
            self.color,
            (self.x + self.border_radius, self.y + self.height - self.border_radius),
            self.border_radius,
        )
        # bottom right corner
        pygame.draw.circle(
            screen,
            self.color,
            (
                self.x + self.width - self.border_radius,
                self.y + self.height - self.border_radius,
            ),
            self.border_radius,
        )

        pygame.draw.rect(
            screen,
            self.color,
            (
                self.x + self.border_radius,
                self.y,
                self.width - 2 * self.border_radius,
                self.height,
            ),
            0,
        )
        pygame.draw.rect(
            screen,
            self.color,
            (
                self.x,
                self.y + self.border_radius,
                self.width,
                self.height - 2 * self.border_radius,
            ),
            0,
        )
