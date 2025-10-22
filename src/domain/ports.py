# src/domain/ports.py
from abc import ABC, abstractmethod


class AudioPort(ABC):
    @abstractmethod
    def play_sound(self, sound_name: str):
        pass


class ClockPort(ABC):
    @abstractmethod
    def now(self) -> int:
        """Retorna el tiempo actual en milisegundos."""
        pass
