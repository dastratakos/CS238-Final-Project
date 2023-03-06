import pygame

from components.button import Button
from components.rounded_rect import RoundedRect
from components.text import Text
from config import BLOCK_SIZE, SCREEN_SIZE, VELOCITY_X
from game import Game
from utils import load_map


def get_events(pause_button: Button = None):
    r, p, d, m, n, left, right = False, False, False, False, False, False, False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if pause_button and event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button.rect.collidepoint(event.pos):
                p = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                r = True
            elif event.key == pygame.K_p:
                p = True
            elif event.key == pygame.K_d:
                d = True
            elif event.key == pygame.K_m:
                m = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            n = True
        elif keys[pygame.K_LEFT]:
            left = True
        elif keys[pygame.K_RIGHT]:
            right = True
    return r, p, d, m, n, left, right


def debug_loop(screen, clock, game, pause, pause_button):
    restart, debug, next_frame = False, True, False
    while debug:
        restart, p, d, _, next_frame, left, right = get_events(pause_button)

        if p:
            pause = not pause
        if restart or d:
            debug = False
        if left:
            game.camera.x -= VELOCITY_X * 15
        if right:
            game.camera.x += VELOCITY_X * 15

        draw_debug(screen)
        if not pause:
            pause_button.draw(screen)

        pygame.display.update()
        clock.tick(15)

        if p or next_frame or left or right:
            # Run the main loop once and come back (debug will still be True)
            break
    return restart, pause, debug, next_frame


def draw_debug(screen):
    red = (255, 0, 0)
    x = SCREEN_SIZE[0] - 25
    Text("Debug mode", color=red, topright=(x, 65)).draw(screen)
    Text("n - next frame", color=red, topright=(x, 85)).draw(screen)
    Text("left/right arrows - move camera", color=red, topright=(x, 105)).draw(screen)


def draw_pause(screen):
    alpha_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    alpha_surface.fill((255, 255, 255, 1), special_flags=pygame.BLEND_RGBA_MULT)
    RoundedRect(
        50, 75, SCREEN_SIZE[0] - 100, SCREEN_SIZE[1] - 150, (0, 0, 0, 150), 20
    ).draw(alpha_surface)
    screen.blit(alpha_surface, (0, 0))

    mid_x, mid_y = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2
    Text("Paused", 50, center=(mid_x, mid_y)).draw(screen)
    Text("p - play", center=(mid_x, mid_y - 50)).draw(screen)
    Text("r - restart level", center=(mid_x, mid_y - 70)).draw(screen)
    Text("m - main menu", center=(mid_x, mid_y - 90)).draw(screen)


def play(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    level_id: int,
    simulate: bool = False,
):
    """This function is the main loop for one level of the game. It creates a
    Game object and handles all of the controls and drawing for pausing,
    debugging, and restarting separately from the Game.

    Args:
        screen (pygame.Surface): _description_
        clock (pygame.time.Clock): _description_
        level_id (int): _description_
        simulate (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    map = load_map(level_id)
    num_manual_players = 0 if simulate else 1
    num_ai_players = 20 if simulate else 0
    best_ai_player = None

    def new_game():
        return Game(map, num_manual_players, num_ai_players, best_ai_player)

    game = new_game()
    attempt_num = 1

    pause_button = Button(SCREEN_SIZE[0] - 95, 25, 70, 30, "Pause", 20)

    go_to_menu, pause, debug, next_frame = False, False, False, False
    while not go_to_menu:
        restart, p, debug, m, *_ = get_events(pause_button)
        if restart:
            attempt_num += 1
            game = new_game()
        if p:
            pause = not pause
        if pause and m:
            go_to_menu = True
        if debug:
            restart, pause, debug, next_frame = debug_loop(
                screen, clock, game, pause, pause_button
            )

        if not pause and (not debug or next_frame):
            # Update the game
            game.update()

            # Check game status
            if game.all_dead():
                if simulate:
                    furthest_player = max(
                        game.player_sprite_group.sprites(), key=lambda p: p.score
                    )
                    if (
                        not best_ai_player
                        or furthest_player.score > best_ai_player.score
                    ):
                        best_ai_player = furthest_player
                attempt_num += 1
                game = new_game()
            elif simulate and (winner := game.get_winner()):
                best_ai_player = winner
                pause = True

        # Redraw
        game.draw(screen, attempt_num, simulate)

        if debug:
            draw_debug(screen)
        if pause:
            draw_pause(screen)
        else:
            pause_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    if go_to_menu:
        from screens.menu import menu

        menu(screen, clock, level_id=level_id)
