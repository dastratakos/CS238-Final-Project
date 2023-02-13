import csv
from enum import Enum
import os
import sys

import pygame
from pygame.draw import rect

from config import (
    SCREEN_BLOCKS,
    SCREEN_SIZE,
    BLOCK_SIZE,
    VELOCITY_X,
)
from sprites import Player, Sprite, Object
from utils import resize_image
from tile_config import CollisionType, ActionType, tile_config


class Camera:
    def __init__(self):
        self.x, self.y = 0, 0


def check_collisions(player, object_sprites, floor):
    for object in object_sprites:
        if pygame.sprite.collide_rect(player, object):
            # if isinstance(object, End):
            #     print("You win!")
            if isinstance(object, Sprite):
                if player.velocity.y > 0:  # player is falling
                    print("Collision and player falling")
                    player.rect.bottom = object.rect.top
                    player.velocity.y = 0
                    player.on_ground = True
                    player.should_jump = False
                elif player.velocity.y < 0:  # player is jumping
                    print("Collision and player jumping")
                    player.rect.top = object.rect.bottom
                else:  # player is going forward
                    player.velocity.x = 0
                    player.rect.right = object.rect.left
                    print("You lose!")


def load_objects(object_sprites, filename):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        map = []
        for row in reader:
            r = []
            for cell in row:
                r.append(cell)
            map.append(r)

        x, y = 0, -(len(map) - SCREEN_BLOCKS[1] + 4) * BLOCK_SIZE
        for row in map:
            for cell in row:
                # if cell != "0":
                if os.path.exists(f"assets/tiles/tile-{cell}.png"):
                    Sprite(
                        (x, y),
                        resize_image(
                            pygame.image.load(f"assets/tiles/tile-{cell}.png")
                        ),
                        object_sprites,
                    )
                x += BLOCK_SIZE
            x = 0
            y += BLOCK_SIZE


def restart(level_filename="./maps/0.csv"):
    # Create the player
    player_sprite = pygame.sprite.Group()
    player = Player(
        (BLOCK_SIZE * 5, BLOCK_SIZE * 5),
        resize_image(pygame.image.load("assets/players/player-0.png")),
        player_sprite,
    )

    # Create the objects
    object_sprites = pygame.sprite.Group()
    load_objects(object_sprites, level_filename)

    # Create the floor
    floor_sprite = pygame.sprite.Group()
    floor = Object(
        (0, BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4)),
        resize_image(pygame.image.load(HIGHLIGHT_IMG_FILENAME), (800, 2.5)),
        floor_sprite,
    )

    # Create the camera
    camera = Camera()

    return player_sprite, player, object_sprites, floor, camera


class MovingTile:
    def __init__(self, image, pos, num_siblings):
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.width = self.image.get_width()
        self.num_siblings = num_siblings

    def update(self, velocity_x):
        self.x -= velocity_x
        if self.x <= -self.width:
            self.x += self.width * self.num_siblings


class View(Enum):
    HOME = 1
    LEVEL_SELECT = 2
    PLAY = 3
    PAUSE = 4


class GameState:
    def __init__(self):
        self.screen = Screen.HOME
        self.level = 1
        self.attempts = 0
        self.progress = 0
        self.practice_mode = False


def display_view_start(
    game_state: GameState, screen: pygame.Surface, font: pygame.font.Font
):
    screen.fill((0, 0, 0))
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        game_state.level -= 1
        if game_state.level == 0:
            game_state.level = 5
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        game_state.level += 1
        if game_state.level == 6:
            game_state.level = 1

    welcome = font.render(
        f"Welcome to Geometry Dash AI. Choose a level using the left and right arrow keys. Press space to start.",
        True,
        (255, 255, 255),
    )
    controls = font.render("Controls\nJump: Space\nExit: Esc", True, (255, 255, 0))
    level_memo = font.render(f"Level {game_state.level + 1}.", True, (255, 255, 0))
    screen.blits(
        [[welcome, (100, 100)], [controls, (100, 400)], [level_memo, (100, 200)]]
    )


def display_view_level_select(
    game_state: GameState, screen: pygame.Surface, font: pygame.font.Font
):
    pass


def display_view_play(
    game_state: GameState, screen: pygame.Surface, font: pygame.font.Font
):
    pass


def display_view_pause(
    game_state: GameState, screen: pygame.Surface, font: pygame.font.Font
):
    pass


def display_view(
    view: View, game_state: GameState, screen: pygame.Surface, font: pygame.font.Font
):
    if view == View.HOME:
        display_view_start(game_state, screen, font)
    elif view == View.LEVEL_SELECT:
        display_view_level_select(game_state, screen, font)
    elif view == View.PLAY:
        display_view_play(game_state, screen, font)
    elif view == View.PAUSE:
        display_view_pause(game_state, screen, font)


def main():
    if len(sys.argv) != 2:
        raise Exception(f"usage: python {sys.argv[0]} <level>")

    pygame.init()
    pygame.display.set_caption("Geometry Dash AI")
    pygame.display.set_icon(resize_image(pygame.image.load("assets/icon.png")))
    screen = pygame.display.set_mode(SCREEN_SIZE)
    font = pygame.font.SysFont("lucidaconsole", 20)
    clock = pygame.time.Clock()

    game_state = GameState()

    alpha_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    backgrounds = [
        MovingTile(pygame.image.load(BACKGROUND_IMG_FILENAME), (i * 800, 0), 2)
        for i in range(2)
    ]
    grounds = [
        MovingTile(
            resize_image(
                pygame.image.load(GROUND_IMG_FILENAME), (BLOCK_SIZE * 4, BLOCK_SIZE * 4)
            ),
            (i * BLOCK_SIZE * 4, BLOCK_SIZE * (SCREEN_BLOCKS[1] - 4)),
            8,
        )
        for i in range(8)
    ]

    started = False
    exit = False
    while not exit:
        if not started:
            while not started:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        started = True
            player_sprite, player, object_sprites, floor, camera = restart(
                level_filename=f"./maps/{sys.argv[1]}.csv"
            )

        # TODO: decompose into PlayerController class
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player.should_jump = True

        # 1. Update player(s), objects, floor, camera, background, and ground
        player_sprite.update()

        for sprite in object_sprites:
            sprite.rect.x = sprite.initial_pos[0] - camera.x
            sprite.rect.y = sprite.initial_pos[1] - camera.y

        floor.rect.y = floor.initial_pos[1] - camera.y

        camera.x += VELOCITY_X
        # camera.y += player.velocity.y

        for background in backgrounds:
            background.update(VELOCITY_X / 10)

        for ground in grounds:
            ground.update(VELOCITY_X)

        # 2. Check for collisions and update player(s) as necessary
        check_collisions(player, object_sprites, floor)

        # 3, Redraw
        for background in backgrounds:
            screen.blit(background.image, (background.x, background.y))
        for ground in grounds:
            screen.blit(ground.image, (ground.x, ground.y))
        screen.blit(floor, (floor.rect.x, floor.rect.y))

        alpha_surface.fill((255, 255, 255, 1), special_flags=pygame.BLEND_RGBA_MULT)
        for particle in player.particles:
            rect(alpha_surface, (255, 255, 255), particle.get_rect())
        screen.blit(alpha_surface, (0, 0))

        object_sprites.draw(screen)
        if player.should_jump:
            screen.blit(player.image, player.pos)
        else:
            # screen.blit(player.image, player.pos)
            player_sprite.draw(screen)

        # 4. Check for inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit = True
                if event.key == pygame.K_r:
                    player_sprite, player, object_sprites, floor, camera = restart(
                        level_filename=f"./maps/{sys.argv[1]}.csv"
                    )

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
