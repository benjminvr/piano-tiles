from typing import List, Optional
from ..domain.ports import LeaderboardPort
from .leaderboard_local import LocalLeaderboard


class LeaderboardAdapter(LeaderboardPort):
    """
    Adapter that implements LeaderboardPort interface using local file storage.
    This bridges the domain layer with the local leaderboard infrastructure.
    """
    
    def __init__(self, file_path: str = "leaderboard.json"):
        """
        Initialize the leaderboard adapter with local file storage.
        """
        self._leaderboard_client = LocalLeaderboard(file_path)
    
    def save_score(self, player_name: str, score: int) -> bool:
        """Save a player's score to the local leaderboard."""
        return self._leaderboard_client.save_score(player_name, score)
    
    def get_top_scores(self, limit: int = 10) -> List[dict]:
        """Get the top scores from the local leaderboard."""
        return self._leaderboard_client.get_top_scores(limit)
    
    def get_high_score(self) -> Optional[int]:
        """Get the highest score from the local leaderboard."""
        return self._leaderboard_client.get_high_score()
