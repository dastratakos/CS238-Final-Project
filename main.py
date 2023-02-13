import pygame
import sys

from config import SCREEN_SIZE
from utils import load_image
from screens.menu import menu

def main():
    pygame.init()
    pygame.display.set_caption("Geometry Dash AI")
    pygame.display.set_icon(load_image("assets/icon.png"))
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    # font = pygame.font.SysFont("lucidaconsole", 20)

    # game_state = GameState()

    menu(screen, clock)

if __name__ == "__main__":
    main()