

from ..domain.ports import AudioPort, ClockPort, LeaderboardPort
from ..domain.entities import GameState, Score, Board
from ..domain.services import TileGeneratorService


class StartGameUseCase:
    """
    Use case for starting a new game.
    """

    def __init__(self, audio_port: AudioPort, clock_port: ClockPort, leaderboard_port: LeaderboardPort):
        self.audio_port = audio_port
        self.clock_port = clock_port
        self.leaderboard_port = leaderboard_port

    def execute(self, board_width: int = 400, board_height: int = 600) -> dict:
        """
        Start a new game.
        """

        self.audio_port.stop_all_sounds()
        
        high_score = self.leaderboard_port.get_high_score() or 0
        
        game_state = {
            'state': GameState.PLAYING,
            'score': Score(),
            'board': Board(width=board_width, height=board_height),
            'tiles': [],
            'speed': 4.0,
            'high_score': high_score,
            'last_spawn_time': self.clock_port.get_current_time(),
            'base_spawn_interval': 800,
            'base_speed': 4.0
        }
        
        return game_state