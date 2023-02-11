import csv

import pygame
from pygame.math import Vector2
from pygame.draw import rect

from config import (
    SCREEN_SIZE,
    BLOCK_SIZE,
    VELOCITY_X,
    BACKGROUND_IMG_FILENAME,
    PLAYER_IMG_FILENAME,
    BLOCK_IMG_FILENAME,
    SPIKE_IMG_FILENAME,
)
from sprites import Sprite, Player
from utils import resize_image


player_img = resize_image(pygame.image.load(PLAYER_IMG_FILENAME))
block_img = resize_image(pygame.image.load(BLOCK_IMG_FILENAME))
spike_img = resize_image(pygame.image.load(SPIKE_IMG_FILENAME))


def load_objects(object_sprites, filename):
    with open(filename, "r") as file:
        map = csv.reader(file)

        x, y = 0, BLOCK_SIZE
        for row in map:
            for cell in row:
                if cell == "block":
                    Sprite((x, y), block_img, object_sprites)
                if cell == "spike":
                    Sprite((x, y), spike_img, object_sprites)
                x += BLOCK_SIZE
            x = 0
            y += BLOCK_SIZE

def restart(level_filename="./maps/1.csv"):
    # Create the player
    player_sprite = pygame.sprite.Group()
    print("player_sprite", player_sprite)
    player = Player((BLOCK_SIZE * 5, BLOCK_SIZE * 15), player_img, player_sprite)

    # Create the objects
    object_sprites = pygame.sprite.Group()
    load_objects(object_sprites, level_filename)
    
    return player_sprite, player, object_sprites


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Geometry Dash AI")
    # pygame.display.set_icon(player)
    clock = pygame.time.Clock()
    
    background = pygame.image.load(BACKGROUND_IMG_FILENAME)
    
    player_sprite, player, object_sprites = restart()
    
    exit = False
    background_x = 0
    while not exit:
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player.jumping = True

        player_sprite.update()

        # Move map
        for sprite in object_sprites:
            sprite.rect.x -= VELOCITY_X

        # Redraw
        screen.blit(background, (background_x, 0))
        object_sprites.draw(screen)
        player_sprite.draw(screen)

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         exit = True
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             exit = True
    
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
