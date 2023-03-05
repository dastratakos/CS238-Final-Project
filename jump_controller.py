from abc import ABC, abstractmethod
import random

import pygame
import torch
import torch.nn as nn
import torch.nn.functional as F


class JumpController(ABC):
    @abstractmethod
    def should_jump(self):
        pass


class JumpControllerManual(JumpController):
    def should_jump(self):
        return pygame.key.get_pressed()[pygame.K_SPACE]


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        # 5 inputs, size 3 hidden layer, 1 output
        self.fc1 = nn.Linear(5, 3)
        self.fc2 = nn.Linear(3, 1)

    def forward(self, x):
        # x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        x = torch.sigmoid(x)
        x = torch.sigmoid(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x


class JumpControllerAI(JumpController):
    def __init__(self, parent_net=None):
        self.farthest_distance = 0
        if parent_net:
            self.net = parent_net
            for param in self.net.parameters():
                param.data += torch.randn(param.size()) * 0.1
        else:
            self.net = Net()

    def predict(self, input=[1, 2, 3, 4, 5]):
        """
        # TODO: inputs
        1. distance from safePosition?
        2. is flying
        3. flyingVerticalObstacleHeight
        4. onJumpOrb
        5. calculateJumpDeathStatus
        """
        return self.net(torch.Tensor(input)).item() > 0.5
        return random.random() < 0.1

    def should_jump(self):
        return self.predict()


if __name__ == "__main__":
    jump_controller = JumpControllerAI()
    input = torch.Tensor([1, 2, 3, 4, 5])
    out = jump_controller.net(input)
    breakpoint()
