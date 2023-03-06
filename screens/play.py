import pygame

from components.button import Button
from components.text import Text
from config import BLOCK_SIZE, SCREEN_SIZE, VELOCITY_X
from game import Game
from utils import load_map


def play(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    level_id: int,
):
    map = load_map(level_id)
    game = Game(map, num_manual_players=1)
    attempt_num = 1
    alpha_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

    pause_button = Button(SCREEN_SIZE[0] - 95, 25, 70, 30, "Pause", 20)

    go_to_menu, pause, debug, next_frame = False, False, False, False
    while not go_to_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = Game(map, num_manual_players=1)
                    attempt_num += 1
                elif event.key == pygame.K_p:
                    pause = True
                elif event.key == pygame.K_d:
                    debug = True

        if not debug or next_frame:
            game.update()

        if game.player_sprite_group.sprites()[0].dead:
            attempt_num += 1
            game = Game(map, num_manual_players=1)
        elif game.player_sprite_group.sprites()[0].won:
            pause = True

        # Redraw
        game.tile_sprite_group.draw(screen)

        screen.blit(game.floor.image, game.floor.rect.move(0, -game.camera.y))

        for element in game.element_sprite_group:
            offset_rect = element.rect.move(-game.camera.x, -game.camera.y)
            screen.blit(element.image, offset_rect)

        # player particles
        alpha_surface.fill((255, 255, 255, 1), special_flags=pygame.BLEND_RGBA_MULT)
        for player in game.player_sprite_group:
            for particle in player.particles:
                pygame.draw.rect(
                    alpha_surface,
                    (255, 255, 255),
                    particle.rect.move(-game.camera.x, -game.camera.y),
                )
        screen.blit(alpha_surface, (0, 0))

        for player in game.player_sprite_group:
            screen.blit(
                player.ship_image if player.flying else player.image,
                player.rect.move(-game.camera.x, -game.camera.y),
            )

        game.progress_bar.draw(screen)

        Text(
            f"ATTEMPT {attempt_num}",
            50,
            center=(
                SCREEN_SIZE[0] / 2 - game.camera.x,
                game.map_height - 8 * BLOCK_SIZE - game.camera.y,
            ),
        ).draw(screen)

        if debug:
            Text(
                "Debug mode",
                20,
                color=(255, 0, 0),
                topright=(SCREEN_SIZE[0] - 25, 65),
            ).draw(screen)
            Text(
                "n - next frame",
                20,
                color=(255, 0, 0),
                topright=(SCREEN_SIZE[0] - 25, 85),
            ).draw(screen)
            Text(
                "left arrow - move camera left",
                20,
                color=(255, 0, 0),
                topright=(SCREEN_SIZE[0] - 25, 105),
            ).draw(screen)
            Text(
                "right arrow - move camera right",
                20,
                color=(255, 0, 0),
                topright=(SCREEN_SIZE[0] - 25, 125),
            ).draw(screen)

        pause_button.text = "Pause" if not pause else "Play"
        pause_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

        while debug:
            next_frame = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_n]:
                next_frame = True
            elif keys[pygame.K_LEFT]:
                game.camera.x -= VELOCITY_X * 15
                break
            elif keys[pygame.K_RIGHT]:
                game.camera.x += VELOCITY_X * 15
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game = Game(map, num_manual_players=1)
                        attempt_num += 1
                    elif event.key == pygame.K_p:
                        pause = True
                        debug = False
                    elif event.key == pygame.K_d:
                        debug = False

            pygame.display.update()
            clock.tick(15)

            if next_frame:
                break  # Run the outer while loop once and come back to debug

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False
                    elif event.key == pygame.K_d:
                        pause = False
                        debug = True
                    elif event.key == pygame.K_m:
                        pause = False
                        go_to_menu = True

            pause_button.text = "Pause" if not pause else "Play"
            pause_button.draw(screen)

            pygame.display.update()
            clock.tick(15)

    if go_to_menu:
        from screens.menu import menu

        menu(screen, clock, level_id=level_id)
