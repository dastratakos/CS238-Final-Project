import pygame

from config import SCREEN_SIZE, LEVELS
from components.button import Button


def menu(screen: pygame.Surface, clock: pygame.time.Clock):
    level_id = 1

    background = pygame.image.load("assets/background.png")

    level_button = Button(
        SCREEN_SIZE[0] // 4,
        3 * SCREEN_SIZE[1] // 8,
        SCREEN_SIZE[0] // 2,
        SCREEN_SIZE[1] // 4,
        f"Level {level_id}: {LEVELS[level_id]['name']}",
    )
    prev_button = Button(50, (SCREEN_SIZE[1] - 100) // 2, 100, 100, "<")
    next_button = Button(
        SCREEN_SIZE[0] - 150, (SCREEN_SIZE[1] - 100) // 2, 100, 100, ">"
    )

    go_to_play = False
    while not go_to_play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if level_button.rect.collidepoint(event.pos):
                    go_to_play = True
                elif prev_button.rect.collidepoint(event.pos):
                    level_id = (level_id - 2) % len(LEVELS) + 1
                    level_button.text = f"Level {level_id}: {LEVELS[level_id]['name']}"
                elif next_button.rect.collidepoint(event.pos):
                    level_id = level_id % len(LEVELS) + 1
                    level_button.text = f"Level {level_id}: {LEVELS[level_id]['name']}"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    go_to_play = True
                elif event.key == pygame.K_LEFT:
                    level_id = (level_id - 2) % len(LEVELS) + 1
                    level_button.text = f"Level {level_id}: {LEVELS[level_id]['name']}"
                elif event.key == pygame.K_RIGHT:
                    level_id = level_id % len(LEVELS) + 1
                    level_button.text = f"Level {level_id}: {LEVELS[level_id]['name']}"

        # Redraw
        screen.blit(background, (0, 0))

        level_button.draw(screen)
        prev_button.draw(screen)
        next_button.draw(screen)

        # TODO: add explainer text

        pygame.display.update()

    if go_to_play:
        from screens.play import play

        play(screen, clock, level_id)
