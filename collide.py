import math

import pygame
from pygame.math import Vector2

from config import BLOCK_SIZE, CollisionType
from jump_controller import JumpControllerManual
from sprite import ElementSprite, Player
from utils import load_image


pygame.init()
size = (BLOCK_SIZE * 11, BLOCK_SIZE * 11)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

player = Player(
    (size[0] / 2, size[1] / 2 - BLOCK_SIZE),
    Vector2(0, 0),
    load_image(f"assets/players/player-0.png"),
    load_image(f"assets/ships/ship-1.png"),
    JumpControllerManual(),
    False,
)
element = ElementSprite(
    (size[0] / 2, size[1] / 2),
    load_image("assets/elements/element-1.png"),
    CollisionType.SOLID,
)


done = False
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    next_frame = False
    while not next_frame:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    next_frame = True

    print("player", player.rect, player.rect.bottom)
    print("  velocity", player.velocity)
    print("element", element.rect, element.rect.top)

    screen.fill(0)

    screen.blit(player.image, player.rect)
    screen.blit(element.image, element.rect)

    player.update({(5, 5): element}, size[1] - BLOCK_SIZE)

    print()

    pygame.display.flip()

pygame.quit()
exit()
