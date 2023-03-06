import pygame

from config import SCREEN_SIZE, LEVELS
from components.button import Button
from components.text import Text


def menu(screen: pygame.Surface, clock: pygame.time.Clock, level_id: int = 0):
    background = pygame.image.load("assets/background.png")

    title = Text(
        f"Level {level_id + 1}: {LEVELS[level_id]['name']}",
        50,
        midbottom=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 4 - 40),
    )
    play_button = Button(
        SCREEN_SIZE[0] / 4,
        SCREEN_SIZE[1] / 4 + 40,
        SCREEN_SIZE[0] / 4 - 20,
        100,
        "Play",
    )
    simulate_button = Button(
        SCREEN_SIZE[0] / 2 + 20,
        SCREEN_SIZE[1] / 4 + 40,
        SCREEN_SIZE[0] / 4 - 20,
        100,
        "Simulate",
    )
    prev_button = Button(50, SCREEN_SIZE[1] / 4 - 50, 100, 100, "<")
    next_button = Button(SCREEN_SIZE[0] - 150, SCREEN_SIZE[1] / 4 - 50, 100, 100, ">")

    explainer_text = """Welcome to Geometry Dash AI!
        
        Press "p" to click the Play button to play the level.
        
        Press "s" or click the Simulate button to run an AI on the level.
        The AI is trained using a genetic algorithm.
        
        Controls:
        - space: jump
        - p: pause
        - r: restart
        """
    lines = [x.strip() for x in explainer_text.splitlines()]
    explainer_text = []
    for i, line in enumerate(reversed(lines)):
        explainer_text.append(
            Text(line, midleft=(SCREEN_SIZE[0] / 4, SCREEN_SIZE[1] - 10 - i * 20))
        )

    go_to_play, go_to_simulate = False, False
    while not go_to_play and not go_to_simulate:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if play_button.rect.collidepoint(event.pos):
                    go_to_play = True
                elif simulate_button.rect.collidepoint(event.pos):
                    go_to_simulate = True
                elif prev_button.rect.collidepoint(event.pos):
                    level_id = (level_id - 1) % len(LEVELS)
                    title.text = f"Level {level_id + 1}: {LEVELS[level_id]['name']}"
                elif next_button.rect.collidepoint(event.pos):
                    level_id = (level_id + 1) % len(LEVELS)
                    title.text = f"Level {level_id + 1}: {LEVELS[level_id]['name']}"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    go_to_play = True
                elif event.key == pygame.K_s:
                    go_to_simulate = True
                elif event.key == pygame.K_LEFT:
                    level_id = (level_id - 1) % len(LEVELS)
                    title.text = f"Level {level_id + 1}: {LEVELS[level_id]['name']}"
                elif event.key == pygame.K_RIGHT:
                    level_id = (level_id + 1) % len(LEVELS)
                    title.text = f"Level {level_id + 1}: {LEVELS[level_id]['name']}"

        # Redraw
        screen.blit(background, (0, 0))

        title.draw(screen)
        play_button.draw(screen)
        simulate_button.draw(screen)
        prev_button.draw(screen)
        next_button.draw(screen)
        for text in explainer_text:
            text.draw(screen)

        # TODO: add explainer text

        pygame.display.update()

    if go_to_play:
        from screens.play import play

        play(screen, clock, level_id)
    elif go_to_simulate:
        from screens.play import play

        play(screen, clock, level_id, simulate=True)
