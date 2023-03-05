import random

import pygame
from pygame.math import Vector2

from components.progress_bar import ProgressBar
from config import (
    BLOCK_SIZE,
    SCREEN_BLOCKS,
    SCREEN_SIZE,
    VELOCITY_X,
    ELEMENTS,
    CollisionType,
)
from jump_controller import JumpControllerManual, JumpControllerAI
from sprite import ElementSprite, Player, TiledSprite
from utils import get_sprite_image, load_image


class Camera:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y


class Game:
    """
    A class that represents a game of Geometry Dash.
    """

    def __init__(
        self,
        map,
        num_manual_players=0,
        num_ai_players=0,
        best_ai_player=None,
    ):
        """Creates a new game.

        Args:
            map (2D list): 2D list where each element is a tile id.
            num_manual_players (int, optional): The number of manual players.
                Defaults to 1.
            num_ai_players (int, optional): The number of AI players. Defaults
                to 20.
            best_ai_player (Player, optional): The best AI player from the
                previous round to model this round's AI players off of. Defaults
                to None.
        """
        self.map_height = len(map) * BLOCK_SIZE
        self.map_width = len(map[0]) * BLOCK_SIZE

        # The camera will determine the upper-left corner of the screen
        self.camera = Camera(0, self.map_height + (4 - SCREEN_BLOCKS[1]) * BLOCK_SIZE)

        # sprite group for all the players
        self.player_sprite_group = self.init_players(
            num_manual_players, num_ai_players, best_ai_player
        )

        # sprite group for all the elements in the map
        self.element_sprite_group = self.init_elements(map)

        # dict from tile coord to sprite element
        self.element_map = {}
        for element_sprite in self.element_sprite_group:
            tile_coord = (
                element_sprite.rect.x // BLOCK_SIZE,
                element_sprite.rect.y // BLOCK_SIZE,
            )
            self.element_map[tile_coord] = element_sprite

        # sprite group for all the background tiles
        self.tile_sprite_group = self.init_tiles()

        self.floor = ElementSprite(
            (0, self.map_height),
            load_image("assets/highlight.png", (SCREEN_SIZE[0], 2.5)),
            CollisionType.SOLID,
        )

        self.progress_bar = ProgressBar(SCREEN_SIZE[0] / 4, 30, SCREEN_SIZE[0] / 2, 20)

    def init_players(self, num_manual_players, num_ai_players, best_ai_player):
        player_sprite_group = pygame.sprite.Group()
        for i in range(num_ai_players):
            if best_ai_player:
                # Make the first player the same as the best player from the
                # previous generation so that the NN does not devolve
                if i == 0:
                    jump_controller = best_ai_player.jump_controller
                else:
                    jump_controller = JumpControllerAI(
                        best_ai_player.jump_controller.net
                    )
            else:
                jump_controller = JumpControllerAI()
            Player(
                (
                    BLOCK_SIZE * -5 - (BLOCK_SIZE * 3 * i / num_ai_players),
                    self.map_height - BLOCK_SIZE,
                ),
                Vector2(VELOCITY_X, 0),
                load_image(f"assets/players/player-{random.randint(1, 20)}.png"),
                load_image(f"assets/ships/ship-1.png"),
                jump_controller,
                True,
                player_sprite_group,
            )
        for _ in range(num_manual_players):
            Player(
                (BLOCK_SIZE * -5, self.map_height - BLOCK_SIZE),
                Vector2(VELOCITY_X, 0),
                load_image("assets/players/player-0.png"),
                load_image(f"assets/ships/ship-1.png"),
                JumpControllerManual(),
                False,
                player_sprite_group,
            )
        return player_sprite_group

    def init_elements(self, map):
        element_sprite_group = pygame.sprite.Group()
        x, y = 0, 0
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
                    ElementSprite(
                        (
                            x - (BLOCK_SIZE if is_portal else 0),
                            y - (BLOCK_SIZE if is_portal else 0),
                        ),
                        image,
                        ELEMENTS[id]["collision_type"],
                        element_sprite_group,
                    )
                x += BLOCK_SIZE
            x = 0
            y += BLOCK_SIZE
        return element_sprite_group

    def init_tiles(self):
        tile_sprite_group = pygame.sprite.Group()
        # Background tiles
        for i in range(2):
            TiledSprite(
                (i * 800, 0),
                Vector2(VELOCITY_X / 5, 0),
                pygame.image.load("assets/background.png"),
                2,
                tile_sprite_group,
            )
        # Floor tiles
        for i in range(8):
            TiledSprite(
                (i * BLOCK_SIZE * 4, BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4)),
                Vector2(VELOCITY_X, 0),
                load_image("assets/ground.png", (BLOCK_SIZE * 4, BLOCK_SIZE * 4)),
                8,
                tile_sprite_group,
            )
        return tile_sprite_group

    def update(self):
        for player in self.player_sprite_group:
            player.should_jump = player.jump_controller.should_jump(
                player.rect, self.element_map
            )
            player.update(self.element_map, self.map_height)
        
        # Starting animation: don't move the camera until the player is past the
        # first third of the screen
        if self.player_sprite_group.sprites()[0].rect.x > SCREEN_SIZE[0] / 3:
            self.tile_sprite_group.update()
            self.camera.x += VELOCITY_X
        # self.camera.y += 0 # TODO: camera should follow player

        self.progress_bar.progress = self.camera.x / self.map_width
