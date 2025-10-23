

import pygame
from ..domain.ports import AudioPort, ClockPort
from ..domain.entities import GameState, TileColor
from ..domain.services import TileGeneratorService, GameValidationService
import random


class UpdateGameUseCase:
    """
    Use case for updating the game state each frame.
    """

    def __init__(self, audio_port: AudioPort, clock_port: ClockPort):
        self.audio_port = audio_port
        self.clock_port = clock_port
        self.tile_generator = TileGeneratorService(tile_width=100, tile_height=150)

    def execute(self, game_state: dict) -> dict:
        """
        Update the game state for one frame.
        """
        current_time = self.clock_port.get_current_time()
        delta_time = self.clock_port.get_delta_time()
        
        # Update tile positions
        for tile in game_state['tiles']:
            tile['rect'].y += game_state['speed']
        
        # Remove tiles that are off screen
        game_state['tiles'] = [t for t in game_state['tiles'] if t['rect'].top < game_state['board'].height]
        
        # Spawn new tiles
        spawn_interval = game_state['base_spawn_interval'] * (game_state['base_speed'] / game_state['speed'])
        if current_time - game_state['last_spawn_time'] > spawn_interval:
            self._spawn_row(game_state)
            game_state['last_spawn_time'] = current_time
            game_state['speed'] += 0.5  # Increase speed gradually
        
        if self._check_game_over(game_state):
            game_state['state'] = GameState.GAME_OVER
            self.audio_port.play_game_over_sound()
            
            if game_state['score'].value > game_state['high_score']:
                game_state['high_score'] = game_state['score'].value
        
        return game_state
    
    def _spawn_row(self, game_state: dict):
        """Spawn a new row of tiles."""
        black_index = random.randint(0, 3)
        tile_width = game_state['board'].width // 4
        
        for i in range(4):
            color = TileColor.BLACK if i == black_index else TileColor.WHITE
            rect = pygame.Rect(i * tile_width, -game_state['board'].height // 4, tile_width, game_state['board'].height // 4)
            game_state['tiles'].append({
                'rect': rect,
                'color': color,
                'clicked': False
            })
    
    def _check_game_over(self, game_state: dict) -> bool:
        """Check if the game should end."""
        for tile in game_state['tiles']:
            if (tile['color'] == TileColor.BLACK and 
                not tile['clicked'] and 
                tile['rect'].bottom >= game_state['board'].height):
                return True
        return False