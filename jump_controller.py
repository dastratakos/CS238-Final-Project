from __future__ import annotations
from abc import ABC, abstractmethod
import time
from typing import TYPE_CHECKING

import pygame
import torch
import torch.nn as nn
import torch.nn.functional as F

from config import BLOCK_SIZE, CollisionType

if TYPE_CHECKING:
    from sprite import Player


class JumpController(ABC):
    @abstractmethod
    def should_jump(self, player: Player, element_map: dict, floor_level: int):
        pass


class JumpControllerManual(JumpController):
    def should_jump(self, player: Player, element_map: dict, floor_level: int):
        return pygame.key.get_pressed()[pygame.K_SPACE]


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        # 5 inputs, size 3 hidden layer, 1 output
        self.fc1 = nn.Linear(5, 3)
        self.fc1 = nn.Linear(1, 3)
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

            # breakpoint()

            EVOLUTION_STRENGTH = 2  # The strength of the mutation
            EVOLUTION_FREQ = 0.5  # How many of the weights will be mutated
            for param in self.net.parameters():
                mask = torch.Tensor(param.size()).uniform_() <= EVOLUTION_FREQ
                mutation = mask * (torch.randn(param.size()) * EVOLUTION_STRENGTH)
                # breakpoint()
                param.data += mutation

            # breakpoint()
        else:
            self.net = Net()

    def hallucinate_dist_to_death(
        self, player: Player, element_map: dict, floor_level: int
    ):
        """Simulates 40 steps into the future and returns the distance to the
        furthest "safe" position before death.

        This tells the NN that it should jump sometime before this distance.

        Args:
            player (Player): The player to simulate.
            element_map (dict): Dictionary from tile coordinates to pygame Sprites.
            floor_level (int): The y coordinate of the floor.

        Returns:
            int: The distance to the furthest safe position before death.
        """
        curr_x = player.rect.x
        dist = 0

        clone = player.clone()

        """Count out 50 safe spaces

        Returns:
            _type_: _description_
        """

        # Around 8 * BLOCK_SIZE look-ahead
        num_steps = 0
        while num_steps < 50:
            clone.update(element_map, floor_level)
            if clone.dead:
                return dist
            if clone.won:
                return float("inf")
            if clone.on_ground or clone.flying:  # safe
                dist = clone.rect.x - curr_x
                num_steps += 1
        return dist

    def hallucinate_will_die_if_jump(
        self, player: Player, element_map: dict, floor_level: int, on_jump_orb: bool
    ):
        """Returns whether the player will die if it jumps.

        Args:
            player (Player): The player to simulate
            element_map (dict): Dictionary from tile coordinates to pygame Sprites.
            floor_level (int): The y coordinate of the floor.
            on_jump_orb (bool): Whether or not the player is on a jump orb.

        Returns:
            bool: Whether the player will die if it jumps.
        """
        if player.flying:  # jump is irrelevant
            return False
        if not player.on_ground and not on_jump_orb:  # cannot jump
            return False

        clone = player.clone()
        clone.should_jump = True

        # Around 8 * BLOCK_SIZE look-ahead
        for _ in range(50):
            clone.update(element_map, floor_level)
            if clone.dead:
                return True
            if clone.on_ground or clone.won:  # landed safely after the jump
                return False
        return False

    def get_vertical_obstacle_height(
        self, player: Player, element_map: dict, floor_level: int
    ):
        """Returns the combined height of SOLID and SPIKE elements directly
        below the player. This tells the NN that it should jump when flying.

        Args:
            player (Player): The player to simulate
            element_map (dict): Dictionary from tile coordinates to pygame Sprites.
            floor_level (int): The y coordinate of the floor.

        Returns:
            int: The combined height of vertical obstacles directly below the player.
        """
        tile_coord = (player.rect.x // BLOCK_SIZE, player.rect.y // BLOCK_SIZE)

        height = 0
        for y in range(tile_coord[1], floor_level // BLOCK_SIZE):
            element = element_map.get((tile_coord[0], y))
            if element and element.collision_type in (
                CollisionType.SOLID,
                CollisionType.SPIKE,
            ):
                height += 1
        return height * BLOCK_SIZE

    def should_jump(self, player: Player, element_map: dict, floor_level: int):
        dist_to_death = self.hallucinate_dist_to_death(player, element_map, floor_level)

        print("dist_to_death:", dist_to_death)

        if player.flying:
            vertical_obstacle_height = self.get_vertical_obstacle_height(
                player, element_map, floor_level
            )
            vertical_player_height = floor_level - player.rect.y
            if vertical_player_height - vertical_obstacle_height < 4 * BLOCK_SIZE:
                return True
            # return dist_to_death < 200

        # if dist_to_death < 46:  # jump anytime now
        if dist_to_death < 40:  # jump anytime now
            print("  jump anytime now")
            tile_coord = (player.rect.x // BLOCK_SIZE, player.rect.y // BLOCK_SIZE)
            element = element_map.get(tile_coord)
            on_jump_orb = (
                element.collision_type == CollisionType.JUMP_ORB if element else False
            )

            will_die_if_jump = self.hallucinate_will_die_if_jump(
                player, element_map, floor_level, on_jump_orb
            )

            print(f"  {'will' if will_die_if_jump else 'wont'} die")
            if not will_die_if_jump:
                print(f"  can{'' if player.on_ground or player.flying else 't'} jump")

            return not will_die_if_jump  # don't jump if it'll make you die
        return False

        features = [
            # int(player.flying),
            (240 - dist_to_death) / 200,
            # int(on_jump_orb),
            # int(will_die_if_jump),
            # vertical_obstacle_height,
        ]

        # print(time.time(), features, end=" ")

        should_jump = self.net(torch.Tensor(features)).item() > 0.5

        # print(should_jump)

        return should_jump
        # return self.net(torch.Tensor(input)).item() > 0.5


if __name__ == "__main__":
    jump_controller = JumpControllerAI()
    input = torch.Tensor([1, 2, 3, 4, 5])
    out = jump_controller.net(input)
    breakpoint()
