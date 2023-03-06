import pygame
from pygame.math import Vector2

from config import BLOCK_SIZE, CollisionType
from sprites.basic import ElementSprite
from sprites.player import Player
from utils import FillType, load_image


pygame.init()
size = (BLOCK_SIZE * 11, BLOCK_SIZE * 11)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

player = Player(
    (size[0] / 2, size[1] / 2 - BLOCK_SIZE),
    Vector2(0, 0),
    load_image(f"assets/players/player-18.png", fill_type=FillType.PLAYER),
    load_image(f"assets/ships/ship-1.png", fill_type=FillType.SHIP),
    flying=False,
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

    screen.fill((43,91,168))

    screen.blit(player.ship_image if player.flying else player.image, player.rect)
    screen.blit(element.image, element.rect)

    pygame.display.flip()

pygame.quit()
exit()
