import pygame

class Game:
    """
    A class that represents a game of Geometry Dash.
    """
    
    def __init__(self, level_id, num_manual_players, num_ai_players, best_ai_player, generation):
        self.camera = None
        self.map = None # dict from tile coord to sprite blocks
        self.players = None
        self.floor = None
        self.tiled_sprites = None # floor tiles and background tiles
        self.progress_bar = None
    
    def update(self):
        pass

    def check_collisions(self):
        pass
    
    
def play():
    """
    initialize a new game
    
    while True:
        for event in pygame.event.get():
            check for quit, restart, pause, or debug
        
        
    """
    pass