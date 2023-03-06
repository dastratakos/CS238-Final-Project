import random

import pygame
from pygame.math import Vector2

from components.progress_bar import ProgressBar
from components.text import Text
from config import (
    BLOCK_SIZE,
    ELEMENTS,
    PALETTE,
    SCREEN_BLOCKS,
    SCREEN_SIZE,
    VELOCITY_X,
    CollisionType,
)
from jump_controller import JumpControllerManual, JumpControllerAI
from sprites.basic import ElementSprite, ImageSprite, TiledSprite
from sprites.player import Player
from utils import FillType, load_image


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

        self.num_ai_players = num_ai_players
        self.best_ai_player = best_ai_player

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

        self.floor = ImageSprite(
            (0, self.map_height),
            load_image("assets/highlight.png", (SCREEN_SIZE[0], 2.5)),
        )

        self.progress_bar = ProgressBar(SCREEN_SIZE[0] / 4, 30, SCREEN_SIZE[0] / 2, 20)

    def init_players(self, num_manual_players, num_ai_players, best_ai_player):
        # How much space the line of AI players should take up
        AI_PLAYERS_SPREAD = SCREEN_SIZE[0] / 3

        player_sprite_group = pygame.sprite.Group()
        for i in range(num_ai_players):
            color1, color2 = random.choice(PALETTE), random.choice(PALETTE)
            if i == num_ai_players - 1:
                # Make the first player the same as the best player from the
                # previous generation so that the NN does not devolve
                if best_ai_player:
                    jump_controller = best_ai_player.jump_controller
                # If there is no best player, make a random player
                else:
                    jump_controller = JumpControllerAI()
                # The first player gets the player-0 skin
                image = load_image(f"assets/players/player-0.png")
            else:
                # Make the rest of the players a child of the best player
                if best_ai_player:
                    jump_controller = JumpControllerAI(
                        best_ai_player.jump_controller.net
                    )
                # If there is no best player, make a random player
                else:
                    jump_controller = JumpControllerAI()
                image = load_image(
                    f"assets/players/player-{random.randint(1, 20)}.png",
                    fill_type=FillType.PLAYER,
                    color1=color1,
                    color2=color2,
                )

            Player(
                (
                    BLOCK_SIZE * -5
                    - (AI_PLAYERS_SPREAD * (num_ai_players - i - 1) / num_ai_players),
                    self.map_height - BLOCK_SIZE,
                ),
                Vector2(VELOCITY_X, 0),
                image,
                load_image(
                    f"assets/ships/ship-1.png",
                    fill_type=FillType.SHIP,
                    color1=color1,
                    color2=color2,
                ),
                jump_controller=jump_controller,
                sprite_groups=[player_sprite_group],
            )
        for _ in range(num_manual_players):
            Player(
                (BLOCK_SIZE * -5, self.map_height - BLOCK_SIZE),
                Vector2(VELOCITY_X, 0),
                load_image("assets/players/player-0.png"),
                load_image(f"assets/ships/ship-1.png", fill_type=FillType.SHIP),
                jump_controller=JumpControllerManual(),
                sprite_groups=[player_sprite_group],
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
                image = load_image(
                    ELEMENTS[id]["filename"],
                    (
                        BLOCK_SIZE * (3 if is_portal else 1),
                        BLOCK_SIZE * (3 if is_portal else 1),
                    ),
                )
                if image:
                    ElementSprite(
                        (
                            x - BLOCK_SIZE * (2 if is_portal else 0),
                            y - BLOCK_SIZE * (2 if is_portal else 0),
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
            if not player.dead:
                # print("on_ground", player.on_ground)
                player.should_jump = player.jump_controller.should_jump(
                    player, self.element_map, self.map_height
                )
            player.update(self.element_map, self.map_height)

        player_x = self.player_sprite_group.sprites()[-1].rect.x

        # Starting animation: don't move the camera until the player is past the
        # first third of the screen
        if player_x > SCREEN_SIZE[0] / 3:
            self.tile_sprite_group.update()
            self.camera.x += VELOCITY_X
        # self.camera.y += 0 # TODO: camera should follow player

        if player_x < SCREEN_SIZE[0] / 3:
            self.progress_bar.progress = (
                max(0, player_x + BLOCK_SIZE * 2) / self.map_width
            )
        else:
            self.progress_bar.progress = (
                self.camera.x + SCREEN_SIZE[0] / 3 + BLOCK_SIZE * 2
            ) / self.map_width

    def all_dead(self):
        for player in self.player_sprite_group:
            if not player.dead:
                return False
        return True

    def count_alive(self):
        count = 0
        for player in self.player_sprite_group:
            if not player.dead:
                count += 1
        return count

    def get_winner(self):
        for player in self.player_sprite_group:
            if player.won:
                return player
        return None

    def draw(
        self,
        screen: pygame.Surface,
        attempt_num: int,
        game_time: float,
        total_time: float,
        simulate: bool,
    ):
        self.tile_sprite_group.draw(screen)

        screen.blit(self.floor.image, self.floor.rect.move(0, -self.camera.y))

        for element in self.element_sprite_group:
            offset_rect = element.rect.move(-self.camera.x, -self.camera.y)
            screen.blit(element.image, offset_rect)

        # player particles
        alpha_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        alpha_surface.fill((255, 255, 255, 1), special_flags=pygame.BLEND_RGBA_MULT)
        for player in self.player_sprite_group:
            for particle in player.particles:
                pygame.draw.rect(
                    alpha_surface,
                    (255, 255, 255, 255 * (particle.ttl / 16)),
                    particle.rect.move(-self.camera.x, -self.camera.y),
                )
        screen.blit(alpha_surface, (0, 0))

        for player in self.player_sprite_group:
            screen.blit(
                player.ship_image if player.flying else player.image,
                player.rect.move(-self.camera.x, -self.camera.y),
            )

        self.progress_bar.draw(screen)

        Text(
            f"Time: {game_time:.2f}s",
            30,
            bottomleft=(20, SCREEN_SIZE[1] - 20),
        ).draw(screen)

        if not simulate:
            Text(
                f"ATTEMPT {attempt_num}",
                50,
                center=(
                    SCREEN_SIZE[0] / 2 - self.camera.x,
                    self.map_height - 8 * BLOCK_SIZE - self.camera.y,
                ),
            ).draw(screen)
        else:
            Text(f"Generation {attempt_num}", 30, topleft=(20, 20)).draw(screen)
            Text(
                f"{self.count_alive()}/{self.num_ai_players} alive",
                30,
                topleft=(20, 50),
            ).draw(screen)
            best_score = self.best_ai_player.score if self.best_ai_player else 0
            Text(
                f"Best score: {(100 * best_score / self.map_width):.2f}%",
                30,
                topleft=(20, 80),
            ).draw(screen)
            Text(f"Total time: {total_time:.2f}s", 30, topleft=(20, 110)).draw(screen)
