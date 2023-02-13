import pygame

from components.button import Button
from config import SCREEN_SIZE


def pause(screen: pygame.Surface, clock: pygame.time.Clock, level_id=1, progress=42):
    background = pygame.image.load("assets/background.png")

    menu_button = Button(100, (SCREEN_SIZE[1] - 100) // 2, 100, 100, "Menu")
    play_button = Button(
        SCREEN_SIZE[0] - 200, (SCREEN_SIZE[1] - 100) // 2, 100, 100, "Play"
    )

    go_to_menu, go_to_play = False, False
    while not go_to_menu and not go_to_play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if menu_button.rect.collidepoint(event.pos):
                    go_to_menu = True
                elif play_button.rect.collidepoint(event.pos):
                    go_to_play = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    go_to_menu = True
                if event.key == pygame.K_SPACE:
                    go_to_play = True

        screen.blit(background, (0, 0))

        menu_button.draw(screen)
        play_button.draw(screen)

        # text
        font = pygame.font.Font(None, 36)
        text = font.render("TODO: pause screen", True, (100, 100, 100))
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 4)
        screen.blit(text, text_rect)

        pygame.display.update()

    if go_to_menu:
        from screens.menu import menu

        menu(screen, clock)
    elif go_to_play:
        from screens.play import play

        play(screen, clock, level_id, progress)
