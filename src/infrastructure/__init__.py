"""
Infrastructure layer for Piano Tiles game.

This module contains all the infrastructure adapters that implement
the domain ports, bridging the domain layer with external systems.
All leaderboard functionality uses local file storage.
"""

from .pygame_audio_adapter import PygameAudioAdapter
from .system_clock_adapter import SystemClockAdapter
from .leaderboard_adapter import LeaderboardAdapter
from .leaderboard_local import LocalLeaderboard
from .pygame_audio import PygameAudio, PianoNoteGenerator, PRESET_SEQUENCES
from .system_clock import SystemClock

__all__ = [
    # Adapters (implement domain ports)
    'PygameAudioAdapter',
    'SystemClockAdapter', 
    'LeaderboardAdapter',
    
    # Concrete implementations
    'LocalLeaderboard',
    'PygameAudio',
    'PianoNoteGenerator',
    'SystemClock',
    
    # Constants
    'PRESET_SEQUENCES',
]
