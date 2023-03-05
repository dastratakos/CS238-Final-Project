import math

import pygame

from config import (
    BLOCK_SIZE,
    SCREEN_SIZE,
    VELOCITY_X,
)
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

    go_to_menu, pause, debug = False, False, False
    draw_debug = False
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

        while debug:
            next_frame = False
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
                    elif event.key == pygame.K_n:
                        next_frame = True
                    elif event.key == pygame.K_LEFT:
                        game.camera.x -= VELOCITY_X * 5
                        next_frame = True  # TODO: this is not quite right
                    elif event.key == pygame.K_RIGHT:
                        game.camera.x += VELOCITY_X * 5
                        next_frame = True  # TODO: this is not quite right

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

        game.update()

        if game.player_sprite_group.sprites()[0].dead:
            attempt_num += 1
            game = Game(map, num_manual_players=1)

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
            if draw_debug:
                # draw a red rectangle around the player's rotated image
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    (
                        *player.rect.move(-game.camera.x, -game.camera.y).topleft,
                        *player.image.get_size(),
                    ),
                    2,
                )
                # draw a white rectangle around the player's original image
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (
                        *player.rect.move(-game.camera.x, -game.camera.y).topleft,
                        *player.original_image.get_size(),
                    ),
                    2,
                )
                # draw a yellow rectangle around the player's rect
                pygame.draw.rect(
                    screen,
                    (0, 255, 255),
                    (
                        *player.rect.move(-game.camera.x, -game.camera.y).topleft,
                        *player.rect.size,
                    ),
                    2,
                )
                # draw a green dot at the bottom left corner
                pygame.draw.circle(
                    screen,
                    (0, 255, 0),
                    player.rect.move(-game.camera.x, -game.camera.y).bottomleft,
                    3,
                    0,
                )
                # draw a blue dot at the bottom right corner
                pygame.draw.circle(
                    screen,
                    (0, 0, 255),
                    player.rect.move(-game.camera.x, -game.camera.y).bottomright,
                    3,
                    0,
                )
                # draw a purple dot at the bottom right corner of image
                y = (player.angle - 1) % 90 + 1
                off_x = (BLOCK_SIZE * math.sqrt(2) / 2) * math.cos(
                    math.radians(135 - y)
                )
                off_y = (BLOCK_SIZE * math.sqrt(2) / 2) * math.sin(
                    math.radians(135 - y)
                )
                pygame.draw.circle(
                    screen,
                    (255, 0, 255),
                    player.rect.move(
                        -game.camera.x + (off_x),
                        -game.camera.y + off_y,
                    ).center,
                    3,
                    0,
                )

        game.progress_bar.draw(screen)

        font = pygame.font.Font(None, 50)

        text = font.render(f"ATTEMPT {attempt_num}", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_SIZE[0] / 2, game.map_height - 8 * BLOCK_SIZE)
        screen.blit(text, text_rect.move(-game.camera.x, -game.camera.y))

        pygame.display.flip()
        clock.tick(60)

    if go_to_menu:
        from screens.menu import menu

        menu(screen, clock)
