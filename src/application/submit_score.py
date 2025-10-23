

from ..domain.ports import LeaderboardPort


class SubmitScoreUseCase:
    """
    Use case for submitting a player's score to the leaderboard.
    """

    def __init__(self, leaderboard_port: LeaderboardPort):
        self.leaderboard_port = leaderboard_port

    def execute(self, player_name: str, score: int) -> bool:
        """
        Submit a player's score to the leaderboard.
        """
        if not player_name or not player_name.strip():
            player_name = "Anonymous"
        
        if score < 0:
            return False
            
        return self.leaderboard_port.save_score(player_name.strip(), score)