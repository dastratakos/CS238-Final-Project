import pygame

from components.text import Text


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        color=(100, 100, 100),
        hover_color=(200, 200, 200),
        border_radius=10,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.rect = pygame.Rect(x, y, width, height)
        self.border_radius = border_radius

    def draw(self, screen):
        # Check if the mouse is hovering over the button
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        text_color = (
            self.color if self.rect.collidepoint(mouse_pos) else self.hover_color
        )

        # top left corner
        pygame.draw.circle(
            screen,
            color,
            (self.x + self.border_radius, self.y + self.border_radius),
            self.border_radius,
        )
        # top right corner
        pygame.draw.circle(
            screen,
            color,
            (self.x + self.width - self.border_radius, self.y + self.border_radius),
            self.border_radius,
        )
        # bottom left corner
        pygame.draw.circle(
            screen,
            color,
            (self.x + self.border_radius, self.y + self.height - self.border_radius),
            self.border_radius,
        )
        # bottom right corner
        pygame.draw.circle(
            screen,
            color,
            (
                self.x + self.width - self.border_radius,
                self.y + self.height - self.border_radius,
            ),
            self.border_radius,
        )

        pygame.draw.rect(
            screen,
            color,
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
            color,
            (
                self.x,
                self.y + self.border_radius,
                self.width,
                self.height - 2 * self.border_radius,
            ),
            0,
        )

        # text
        text = Text(
            self.text,
            36,
            text_color,
            center=(self.x + self.width // 2, self.y + self.height // 2),
        )
        text.draw(screen)
