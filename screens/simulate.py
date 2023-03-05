"""
- Call play()
    PARAMS
    - num AIs (20)
    - best player (None to begin with)
    - generation
    
    RETURNS
    - best player
"""

import pygame

from screens.play import play


def simulate(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    level_id: int,
    # num_generations=100,
    # population_size=100,
    # mutation_rate=0.01,
    # crossover_rate=0.7,
    # elitism_rate=0.2,
):
    generation = 0
    best_ai_player = None
    while not best_ai_player or best_ai_player.died_at < 95:
        winner = play(screen, clock, level_id, best_ai_player, generation, 20)
        if not best_ai_player or winner.died_at > best_ai_player.died_at:
            best_ai_player = winner
        generation += 1
