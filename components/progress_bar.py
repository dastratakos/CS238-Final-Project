import pygame


class ProgressBar:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        progress: int = 0,  # float from 0 to 1
        color: tuple = (79, 175, 7),
        highlight_color: tuple = (121, 214, 52),
        background_color: tuple = (175, 175, 175),
        text_color: tuple = (255, 255, 255),
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.progress = progress
        self.color = color
        self.highlight_color = highlight_color
        self.background_color = background_color
        self.text_color = text_color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        # background
        pygame.draw.circle(
            screen,
            self.background_color,
            (self.x + self.height / 2, self.y + self.height / 2),
            self.height / 2,
        )
        pygame.draw.circle(
            screen,
            self.background_color,
            (
                self.x + self.width - self.height / 2,
                self.y + self.height / 2,
            ),
            self.height / 2,
        )
        pygame.draw.rect(
            screen,
            self.background_color,
            (
                self.x + self.height / 2,
                self.y,
                self.width - self.height,
                self.height,
            ),
            0,
        )

        # progress
        pygame.draw.circle(
            screen,
            self.color,
            (self.x + self.height / 2, self.y + self.height / 2),
            self.height / 2,
        )
        pygame.draw.circle(
            screen,
            self.color,
            (
                self.x + (self.width - self.height) * self.progress + self.height / 2,
                self.y + self.height / 2,
            ),
            self.height / 2,
        )
        pygame.draw.rect(
            screen,
            self.color,
            (
                self.x + self.height / 2,
                self.y,
                (self.width - self.height) * self.progress,
                self.height,
            ),
            0,
        )

        # highlight
        pygame.draw.circle(
            screen,
            self.highlight_color,
            (self.x + self.height / 2, self.y + self.height / 4 + self.height / 8),
            self.height / 8,
        )
        pygame.draw.circle(
            screen,
            self.highlight_color,
            (
                self.x + (self.width - self.height) * self.progress + self.height / 2,
                self.y + self.height / 4 + self.height / 8,
            ),
            self.height / 8,
        )
        pygame.draw.rect(
            screen,
            self.highlight_color,
            (
                self.x + self.height / 2,
                self.y + self.height / 4,
                (self.width - self.height) * self.progress,
                self.height / 4,
            ),
            0,
        )

        # text
        font = pygame.font.Font(None, 36)
        text = font.render(f"{(100 * self.progress):.2f}%", True, self.text_color)
        text_rect = text.get_rect()
        text_rect.midleft = (self.x + self.width + 10, self.y + self.height / 2)
        screen.blit(text, text_rect)
