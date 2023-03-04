import math
import random
import time

import pygame
from pygame.math import Vector2

from config import (
    BLOCK_SIZE,
    SCREEN_BLOCKS,
    SCREEN_SIZE,
    VELOCITY_X,
    ELEMENTS,
    CollisionType,
)
from components.progress_bar import ProgressBar
from jump_controller import JumpControllerManual, JumpControllerAI
from sprite import TiledSprite, Player, ElementSprite
from utils import load_map, get_sprite_image, load_image


class Camera:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y


def load_level(map, progress=0, num_manual_players=1, num_ai_players=19):
    # Create the players
    player_sprite_group = pygame.sprite.Group()
    players = []
    for _ in range(num_ai_players):
        players.append(
            Player(
                (
                    BLOCK_SIZE * 5
                    - random.randint(0, BLOCK_SIZE * 3)
                    + progress * len(map[0]) * BLOCK_SIZE,
                    BLOCK_SIZE * 5,
                ),
                Vector2(VELOCITY_X, 0),
                load_image(f"assets/players/player-{random.randint(1, 20)}.png"),
                load_image(f"assets/ships/ship-1.png"),
                JumpControllerAI(),
                True,
                player_sprite_group,
            )
        )
    for _ in range(num_manual_players):
        players.append(
            Player(
                (BLOCK_SIZE * 5 + progress * len(map[0]) * BLOCK_SIZE, BLOCK_SIZE * 5),
                Vector2(VELOCITY_X, 0),
                load_image("assets/players/player-0.png"),
                load_image(f"assets/ships/ship-1.png"),
                JumpControllerManual(),
                False,
                player_sprite_group,
            )
        )

    # Create the elements
    element_sprite_group = pygame.sprite.Group()
    elements = []
    x, y = 0, -(len(map) - SCREEN_BLOCKS[1] + 4) * BLOCK_SIZE
    for row in map:
        for id in row:
            is_portal = ELEMENTS[id]["collision_type"] in [
                CollisionType.PORTAL_FLY_START,
                CollisionType.PORTAL_FLY_END,
                CollisionType.PORTAL_GRAVITY_REVERSE,
                CollisionType.PORTAL_GRAVITY_NORMAL,
            ]
            image = get_sprite_image(
                ELEMENTS[id]["filename"],
                (
                    BLOCK_SIZE * (2 if is_portal else 1),
                    BLOCK_SIZE * (2 if is_portal else 1),
                ),
            )
            if image:
                elements.append(
                    ElementSprite(
                        (
                            x - (BLOCK_SIZE if is_portal else 0),
                            y - (BLOCK_SIZE if is_portal else 0),
                        ),
                        Vector2(0, 0),
                        image,
                        ELEMENTS[id]["collision_type"],
                        element_sprite_group,
                    )
                )
            x += BLOCK_SIZE
        x = 0
        y += BLOCK_SIZE

    # Create the floor
    floor_sprite_group = pygame.sprite.Group()
    floor = ElementSprite(
        (progress * len(map[0]) * BLOCK_SIZE, BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4)),
        Vector2(VELOCITY_X, 0),
        load_image("assets/highlight.png", (SCREEN_SIZE[0], 2.5)),
        CollisionType.SOLID,
        floor_sprite_group,
    )

    # Create the camera
    camera = Camera(progress * len(map[0]) * BLOCK_SIZE, 0)

    return (
        player_sprite_group,
        players,
        element_sprite_group,
        elements,
        floor_sprite_group,
        floor,
        camera,
    )


def check_collisions(
    players: list[Player],
    elements: list[ElementSprite],
    floor: ElementSprite,
    map_width: int,
    stop_when_die=True,
):
    for player in players:
        if player.dead:
            continue
        if pygame.sprite.collide_rect(player, floor):
            player.rect.bottom = floor.rect.top + 1
            player.velocity.y = 0.001
            player.should_jump = False
            player.on_ground = True
        collide_elements = pygame.sprite.spritecollide(
            player, elements, False, pygame.sprite.collide_mask
        )
        for element in collide_elements:
            if element.collision_type in [
                CollisionType.SOLID,
                CollisionType.SOLID_TOP,
                CollisionType.SOLID_BOTTOM,
            ]:
                if not player.gravity_reversed:
                    if player.velocity.y > 0:  # player is falling
                        player.rect.bottom = element.rect.top + 1
                        player.velocity.y = 0.001
                        player.should_jump = False
                        player.on_ground = True
                    elif player.velocity.y < 0:  # player is jumping
                        player.rect.top = element.rect.bottom
                    else:  # player is going forward
                        if stop_when_die:
                            player.dead = True
                            player.died_at = player.rect.x / map_width
                            player.velocity = Vector2(0, 0)
                            player.rect.right = element.rect.left
                else:
                    if player.velocity.y < 0:  # player is falling
                        player.rect.top = element.rect.bottom
                        player.velocity.y = 0.001
                        player.on_ground = True
                        player.should_jump = False
                    elif player.velocity.y > 0:  # player is jumping
                        player.rect.bottom = element.rect.top - 1
                    else:  # player is going forward
                        if stop_when_die:
                            player.dead = True
                            player.died_at = player.rect.x / map_width
                            player.velocity = Vector2(0, 0)
                            player.rect.right = element.rect.left
            elif element.collision_type == CollisionType.SPIKE:
                if stop_when_die:
                    player.dead = True
                    player.died_at = player.rect.x / map_width
                    player.velocity = Vector2(0, 0)
            elif element.collision_type == CollisionType.PORTAL_FLY_START:
                player.flying = True
            elif element.collision_type == CollisionType.PORTAL_FLY_END:
                player.flying = False
            elif element.collision_type == CollisionType.PORTAL_GRAVITY_REVERSE:
                player.gravity_reversed = True
            elif element.collision_type == CollisionType.PORTAL_GRAVITY_NORMAL:
                player.gravity_reversed = False
            elif element.collision_type == CollisionType.JUMP_PAD:
                player.velocity.y = -player.velocity_jump_pad
            elif element.collision_type == CollisionType.JUMP_ORB:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    player.velocity.y = -player.velocity_jump_orb
            elif element.collision_type == CollisionType.END:
                player.velocity = Vector2(0, 0)
                # print(time.time(), "You win!")
        if not collide_elements:
            for element in pygame.sprite.spritecollide(player, elements, False):
                if element.collision_type in [
                    CollisionType.SOLID,
                    # CollisionType.SOLID_TOP,
                    # CollisionType.SOLID_BOTTOM,
                ]:
                    if not player.gravity_reversed:
                        if player.velocity.y > 0:  # player is falling
                            player.rect.bottom = element.rect.top + 1
                            player.velocity.y = 0.001
                            player.should_jump = False
                            player.on_ground = True
                        elif player.velocity.y < 0:  # player is jumping
                            player.rect.top = element.rect.bottom
                    else:
                        if player.velocity.y < 0:  # player is falling
                            player.rect.top = element.rect.bottom
                            player.velocity.y = 0.001
                            player.on_ground = True
                            player.should_jump = False
                        elif player.velocity.y > 0:  # player is jumping
                            player.rect.bottom = element.rect.top - 1


def play(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    level_id,
    progress=0,
    draw_debug=False,
    # num_generations=100,
    # population_size=100,
    # mutation_rate=0.01,
    # crossover_rate=0.7,
    # elitism_rate=0.2,
    # screen=None,
    # clock=None,
    # debug=False,
):
    map = load_map(level_id)
    (
        player_sprite_group,
        players,
        element_sprite_group,
        elements,
        floor_sprite_group,
        floor,
        camera,
    ) = load_level(map, progress)

    alpha_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

    tile_sprite_group = pygame.sprite.Group()
    tiles = []
    # Background tiles
    for i in range(2):
        tiles.append(
            TiledSprite(
                (i * 800, 0),
                Vector2(VELOCITY_X / 5, 0),
                pygame.image.load("assets/background.png"),
                2,
                tile_sprite_group,
            )
        )
    # Floor tiles
    for i in range(8):
        tiles.append(
            TiledSprite(
                (i * BLOCK_SIZE * 4, BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4)),
                Vector2(VELOCITY_X, 0),
                load_image("assets/ground.png", (BLOCK_SIZE * 4, BLOCK_SIZE * 4)),
                8,
                tile_sprite_group,
            )
        )

    progress_bar = ProgressBar(SCREEN_SIZE[0] / 4, 30, SCREEN_SIZE[0] / 2, 20, progress)

    go_to_pause = False
    while not go_to_pause or True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    (
                        player_sprite_group,
                        players,
                        element_sprite_group,
                        elements,
                        floor_sprite_group,
                        floor,
                        camera,
                    ) = load_level(map, 0)
                elif event.key == pygame.K_p:
                    go_to_pause = not go_to_pause
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            camera.x -= VELOCITY_X * 5
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            camera.x += VELOCITY_X * 5

        still_alive = False
        for player in players:
            if not player.dead:
                still_alive = True

        if still_alive:
            # 1. Update tiles, players, and camera
            tile_sprite_group.update()
            player_sprite_group.update()
            floor_sprite_group.update()

        if still_alive:
            camera.x += VELOCITY_X
            # camera.y += player.velocity.y

        progress_bar.progress = camera.x / (len(map[0]) * BLOCK_SIZE)

        # 2. Check for collisions and update players as necessary
        check_collisions(players, elements, floor, len(map[0]) * BLOCK_SIZE)

        # 3. Redraw
        tile_sprite_group.draw(screen)
        for floor in floor_sprite_group:
            screen.blit(floor.image, floor.rect.move(-camera.x, -camera.y))

        alpha_surface.fill((255, 255, 255, 1), special_flags=pygame.BLEND_RGBA_MULT)
        for player in players:
            for particle in player.particles:
                pygame.draw.rect(
                    alpha_surface,
                    (255, 255, 255),
                    particle.rect.move(-camera.x, -camera.y),
                )
        screen.blit(alpha_surface, (0, 0))

        for element in element_sprite_group:
            screen.blit(element.image, element.rect.move(-camera.x, -camera.y))
        for player in player_sprite_group:
            screen.blit(
                player.ship_image if player.flying else player.image,
                player.rect.move(-camera.x, -camera.y),
            )
            if draw_debug:
                # draw a red rectangle around the player's rotated image
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    (
                        *player.rect.move(-camera.x, -camera.y).topleft,
                        *player.image.get_size(),
                    ),
                    2,
                )
                # draw a white rectangle around the player's original image
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (
                        *player.rect.move(-camera.x, -camera.y).topleft,
                        *player.original_image.get_size(),
                    ),
                    2,
                )
                # draw a yellow rectangle around the player's rect
                pygame.draw.rect(
                    screen,
                    (0, 255, 255),
                    (
                        *player.rect.move(-camera.x, -camera.y).topleft,
                        *player.rect.size,
                    ),
                    2,
                )
                # draw a green dot at the bottom left corner
                pygame.draw.circle(
                    screen,
                    (0, 255, 0),
                    player.rect.move(-camera.x, -camera.y).bottomleft,
                    3,
                    0,
                )
                # draw a blue dot at the bottom right corner
                pygame.draw.circle(
                    screen,
                    (0, 0, 255),
                    player.rect.move(-camera.x, -camera.y).bottomright,
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
                        -camera.x + (off_x),
                        -camera.y + off_y,
                    ).center,
                    3,
                    0,
                )

        progress_bar.draw(screen)

        pygame.display.flip()
        clock.tick(60)
        while go_to_pause:
            next_frame = False
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        go_to_pause = not go_to_pause
                    elif event.key == pygame.K_n:
                        next_frame = True

            pygame.display.update()
            clock.tick(15)

            if next_frame:
                break

    # if go_to_pause:
    #     from screens.pause import pause

    #     pause(screen, clock, level_id, progress_bar.progress)
