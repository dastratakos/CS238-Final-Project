import math
import pygame

from config import BLOCK_SIZE
from utils import load_image


def blitRotate(surf, image, pos, originPos, angle):
    """Rotates an image

    Args:
        surf (_type_): The surface to draw on
        image (_type_): The original image (not rotated)
        pos (_type_): The position of the pivot point relative to the surface
        originPos (_type_): The position of the pivot point relative to the image
        angle (_type_): The angle of rotation in degrees
    """
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)


pygame.init()
size = (400, 400)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

image = load_image("assets/players/player-0.png")
pivot = (BLOCK_SIZE, BLOCK_SIZE)

angle, frame = 0, 0
done = False
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(0)

    # pos = (200 + math.cos(frame * 0.05) * 100, 200 + math.sin(frame * 0.05) * 50)
    pos = (200, 200)
    blitRotate(screen, image, pos, pivot, angle)
    blitRotate(screen, image, pos, pivot, angle)

    pygame.draw.line(
        screen, (0, 255, 0), (pos[0] - 20, pos[1]), (pos[0] + 20, pos[1]), 1
    )
    pygame.draw.line(
        screen, (0, 255, 0), (pos[0], pos[1] - 20), (pos[0], pos[1] + 20), 1
    )
    pygame.draw.circle(screen, (0, 255, 0), pos, 3, 0)

    pygame.display.flip()
    frame += 1
    angle += 7

pygame.quit()
exit()
