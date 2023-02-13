from abc import ABC, abstractmethod

import pygame


class JumpController(ABC):
    @abstractmethod
    def should_jump(self):
        pass


class JumpControllerManual(JumpController):
    def should_jump(self):
        return pygame.key.get_pressed()[pygame.K_SPACE]


class JumpControllerAI(JumpController):
    def should_jump(self):
        return False
