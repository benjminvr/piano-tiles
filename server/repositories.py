class InMemoryLeaderboardRepository:

    def __init__(self):
        self.scores = []

    def add_score(self, player_name: str, score: int):
        pass

    def get_all_scores(self):
        pass

    def get_top_scores(self, limit: int = 10):
        pass