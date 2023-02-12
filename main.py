import csv
import os
import sys

import pygame
from pygame.draw import rect

from config import (
    SCREEN_BLOCKS,
    SCREEN_SIZE,
    BLOCK_SIZE,
    VELOCITY_X,
    BACKGROUND_IMG_FILENAME,
    GROUND_IMG_FILENAME,
    HIGHLIGHT_IMG_FILENAME,
    PLAYER_IMG_FILENAME,
)
from sprites import Player, Sprite, Object
from utils import resize_image


player_img = resize_image(pygame.image.load(PLAYER_IMG_FILENAME))


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
                if os.path.exists(f"assets/tile-{cell}.png"):
                    Sprite(
                        (x, y),
                        resize_image(pygame.image.load(f"assets/tile-{cell}.png")),
                        object_sprites,
                    )
                x += BLOCK_SIZE
            x = 0
            y += BLOCK_SIZE


def restart(level_filename="./maps/0.csv"):
    # Create the player
    player_sprite = pygame.sprite.Group()
    player = Player((BLOCK_SIZE * 5, BLOCK_SIZE * 5), player_img, player_sprite)

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


def main():
    if len(sys.argv) != 2:
        raise Exception(f"usage: python {sys.argv[0]} <level>")

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Geometry Dash AI")
    # pygame.display.set_icon(player)
    clock = pygame.time.Clock()

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
