from typing import TYPE_CHECKING

import pygame

from components.text import Text
from config import SCREEN_SIZE, VELOCITY_X
from game import Game
from utils import load_map

if TYPE_CHECKING:
    from sprite import Player


def simulate(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    level_id: int,
    num_manual_players: int = 0,
    num_ai_players: int = 20,
):
    generation = 0
    best_ai_player: Player = None
    while not best_ai_player or not best_ai_player.won:

        map = load_map(level_id)
        game = Game(
            map, num_manual_players, num_ai_players, best_ai_player=best_ai_player
        )
        alpha_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

        go_to_menu, pause, debug, next_frame = False, False, False, False
        while not go_to_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game = Game(
                            map,
                            num_manual_players,
                            num_ai_players,
                            best_ai_player=best_ai_player,
                        )
                    elif event.key == pygame.K_p:
                        pause = True
                    elif event.key == pygame.K_d:
                        debug = True

            while debug:
                next_frame = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_n]:
                    next_frame = True
                elif keys[pygame.K_LEFT]:
                    game.camera.x -= VELOCITY_X * 5
                    next_frame = True
                elif keys[pygame.K_RIGHT]:
                    game.camera.x += VELOCITY_X * 5
                    next_frame = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game = Game(
                                map,
                                num_manual_players,
                                num_ai_players,
                                best_ai_player=best_ai_player,
                            )
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

            if not debug or next_frame:
                game.update()

            # Check if all players are dead
            for player in game.player_sprite_group:
                if not player.dead:
                    break
            else:
                # Determine the winner and start a new generation
                winner = max(game.player_sprite_group.sprites(), key=lambda p: p.score)
                if not best_ai_player or winner.score > best_ai_player.score:
                    best_ai_player = winner
                generation += 1
                game = Game(
                    map,
                    num_manual_players,
                    num_ai_players,
                    best_ai_player=best_ai_player,
                )

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

            generation_text = Text(f"Generation {generation}", 30, topleft=(20, 20))
            generation_text.draw(screen)

            best_score = best_ai_player.score if best_ai_player else 0
            best_score_text = Text(
                f"Best score: {(100 * best_score / game.map_width):.2f}%",
                30,
                topleft=(20, 50),
            )
            best_score_text.draw(screen)

            pygame.display.flip()
            clock.tick(60)

        if go_to_menu:
            from screens.menu import menu

            menu(screen, clock)
