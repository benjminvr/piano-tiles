
from abc import ABC, abstractmethod
from typing import List, Optional

class AudioPort(ABC):

    @abstractmethod
    def play_click_sound(self):
        pass

    @abstractmethod
    def play_error_sound(self):
        pass

    @abstractmethod
    def play_game_over_sound(self):
        pass

    @abstractmethod
    def stop_all_sounds(self):
        pass

class ClockPort(ABC):

    @abstractmethod
    def get_current_time(self) -> int:
        pass

    @abstractmethod
    def get_delta_time(self) -> float:
        pass

class LeaderboardPort(ABC):

    @abstractmethod
    def save_score(self, player_name: str, score: int) -> bool:
        pass

    @abstractmethod
    def get_top_scores(self, limit: int = 10) -> List[dict]:
        pass

    @abstractmethod
    def get_high_score(self) -> Optional[int]:
        pass