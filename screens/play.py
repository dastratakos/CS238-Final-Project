import random
import time

import pygame
from pygame.math import Vector2

from config import BLOCK_SIZE, SCREEN_BLOCKS, SCREEN_SIZE, VELOCITY_X
from elements import ELEMENTS, CollisionType, ActionType
from jump_controller import JumpControllerManual, JumpControllerAI
from sprite import TiledSprite, Player, ElementSprite
from utils import load_map, get_sprite_image, load_image


class Camera:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y


def load_level(level_id, num_manual_players=1, num_ai_players=0):
    # Create the players
    player_sprite_group = pygame.sprite.Group()
    players = []
    for _ in range(num_ai_players):
        players.append(
            Player(
                (BLOCK_SIZE * 5 - random.randint(0, BLOCK_SIZE * 3), BLOCK_SIZE * 5),
                Vector2(VELOCITY_X, 0),
                load_image(f"assets/players/player-{random.randint(1, 20)}.png"),
                JumpControllerAI(),
                player_sprite_group,
            )
        )
    for _ in range(num_manual_players):
        players.append(
            Player(
                (BLOCK_SIZE * 5, BLOCK_SIZE * 5),
                Vector2(VELOCITY_X, 0),
                load_image("assets/players/player-0.png"),
                JumpControllerManual(),
                player_sprite_group,
            )
        )

    # Create the elements
    element_sprite_group = pygame.sprite.Group()
    elements = []
    map = load_map(level_id)
    x, y = 0, -(len(map) - SCREEN_BLOCKS[1] + 4) * BLOCK_SIZE
    for row in map:
        for id in row:
            image = get_sprite_image(ELEMENTS[id]["filename"])
            if image:
                elements.append(
                    ElementSprite(
                        (x, y),
                        Vector2(0, 0),
                        image,
                        ELEMENTS[id]["collision_type"],
                        ELEMENTS[id]["action_type"],
                        element_sprite_group,
                    )
                )
            x += BLOCK_SIZE
        x = 0
        y += BLOCK_SIZE

    # Create the floor
    floor_sprite_group = pygame.sprite.Group()
    floor = ElementSprite(
        (0, BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4)),
        Vector2(VELOCITY_X, 0),
        load_image("assets/highlight.png", (SCREEN_SIZE[0], 2.5)),
        CollisionType.SOLID,
        ActionType.NONE,
        floor_sprite_group,
    )

    # Create the camera
    camera = Camera()

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
    players: list[Player], elements: list[ElementSprite], floor: ElementSprite
):
    for player in players:
        if pygame.sprite.collide_rect(player, floor):
            player.rect.bottom = floor.rect.top + 1
            player.velocity.y = 0
            player.should_jump = False
            player.on_ground = True
        for element in elements:
            if pygame.sprite.collide_rect(player, element):
                if element.collision_type in [
                    CollisionType.SOLID,
                    CollisionType.SOLID_TOP,
                    CollisionType.SOLID_BOTTOM,
                ]:
                    if not player.gravity_reversed:
                        if player.velocity.y > 0:  # player is falling
                            print("Collision and player falling")
                            player.rect.bottom = element.rect.top + 1
                            player.velocity.y = 0
                            player.on_ground = True
                            player.should_jump = False
                        elif player.velocity.y < 0:  # player is jumping
                            print("Collision and player jumping")
                            player.rect.top = element.rect.bottom
                        else:  # player is going forward
                            # player.velocity = Vector2(0, 0)
                            # player.rect.right = element.rect.left
                            print("You lose (solid)!")
                            breakpoint()
                    else:
                        if player.velocity.y < 0:  # player is falling
                            print("Collision and player falling")
                            player.rect.top = element.rect.bottom
                            player.velocity.y = 0
                            player.on_ground = True
                            player.should_jump = False
                        elif player.velocity.y > 0:  # player is jumping
                            print("Collision and player jumping")
                            player.rect.bottom = element.rect.top + 1
                        else:  # player is going forward
                            # player.velocity = Vector2(0, 0)
                            # player.rect.right = element.rect.left
                            print("You lose (solid - reverse gravity)!")
                elif element.collision_type == CollisionType.SPIKE:
                    # player.velocity = Vector2(0, 0)
                    print("You lose (spike)!")
                    breakpoint()
                elif element.collision_type == CollisionType.PORTAL:
                    # TODO: Don't run this multiple times for same portal
                    if element.action_type == ActionType.FLY:
                        player.flying = not player.flying
                    elif element.action_type == ActionType.GRAVITY:
                        player.gravity_reversed = not player.gravity_reversed
                elif element.collision_type == CollisionType.JUMP_PAD:
                    player.velocity.y = -player.velocity_jump
                    # player.position.y += player.velocity.y
                elif element.collision_type == CollisionType.JUMP_ORB:
                    if pygame.key.get_pressed()[pygame.K_SPACE]:
                        player.velocity.y = -player.velocity_jump_orb
                        # player.position.y += player.velocity.y
                elif element.collision_type == CollisionType.END:
                    print("You win!")


def play(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    level_id=1,
    progress=0,
    # num_generations=100,
    # population_size=100,
    # mutation_rate=0.01,
    # crossover_rate=0.7,
    # elitism_rate=0.2,
    # screen=None,
    # clock=None,
    # debug=False,
):
    (
        player_sprite_group,
        players,
        element_sprite_group,
        elements,
        floor_sprite_group,
        floor,
        camera,
    ) = load_level(level_id)

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

    go_to_pause = False
    while not go_to_pause:
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
                    ) = load_level(level_id)
                elif event.key == pygame.K_p:
                    go_to_pause = True

        # 1. Update tiles, players, and camera
        tile_sprite_group.update()
        player_sprite_group.update()
        floor_sprite_group.update()

        camera.x += VELOCITY_X
        # camera.y += player.velocity.y

        # 2. Check for collisions and update players as necessary
        check_collisions(players, elements, floor)

        # 3. Redraw
        tile_sprite_group.draw(screen)
        floor_sprite_group.draw(screen)
        # for floor in floor_sprite_group:
        #     screen.blit(floor.image, floor.rect.move(-camera.x, -camera.y))

        alpha_surface.fill((255, 255, 255, 1), special_flags=pygame.BLEND_RGBA_MULT)
        for player in players:
            for particle in player.particles:
                pygame.draw.rect(
                    alpha_surface,
                    (255, 255, 255),
                    particle.rect.move(-camera.x, -camera.y),
                )
        screen.blit(alpha_surface, (0, 0))

        # element_sprite_group.draw(screen)
        for element in element_sprite_group:
            screen.blit(element.image, element.rect.move(-camera.x, -camera.y))
        for player in player_sprite_group:
            screen.blit(player.image, player.rect.move(-camera.x, -camera.y))
        # if player.should_jump:
        #     screen.blit(player.image, player.position)
        # else:
        #     # screen.blit(player.image, player.position)
        #     player_sprite_group.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    if go_to_pause:
        from screens.pause import pause

        # TODO: add progress = full width / camera.x
        pause(screen, clock, level_id)
