

import json
import os
from typing import List, Optional

class LocalLeaderboard:

    def __init__(self, file_path: str = "leaderboard.json"):
        self.file_path = file_path
        self._initialize_file()

    def _initialize_file(self):
        """Crea el archivo si no existe"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def save_score(self, player_name: str, score: int) -> bool:

        try:
            scores = self._load_scores()
            scores.append({"name": player_name, "score": score})
            scores.sort(key=lambda x: x["score"], reverse=True)

            with open(self.file_path, 'w') as f:
                json.dump(scores, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving score: {e}")
            return False

    def _load_scores(self) -> List[dict]:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except:
            return []

    def get_top_scores(self, limit: int = 10) -> List[dict]:
        scores = self._load_scores()
        return scores[:limit]

    def get_high_score(self) -> Optional[int]:
        scores = self._load_scores()
        return scores[0]["score"] if scores else None