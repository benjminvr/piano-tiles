from typing import Optional
from ..domain.ports import AudioPort
from .pygame_audio import PygameAudio


class PygameAudioAdapter(AudioPort):
    """
    Adapter that implements AudioPort interface using PygameAudio implementation.
    """
    
    def __init__(self, note_sequence: Optional[list] = None):
        self._pygame_audio = PygameAudio(note_sequence)
    
    def play_click_sound(self):
        """Play a click sound when a tile is clicked."""
        self._pygame_audio.play_click_sound()
    
    def play_error_sound(self):
        """Play an error sound when a wrong tile is clicked."""
        self._pygame_audio.play_error_sound()
    
    def play_game_over_sound(self):
        """Play a game over sound when the game ends."""
        self._pygame_audio.play_game_over_sound()
    
    def stop_all_sounds(self):
        """Stop all currently playing sounds."""
        self._pygame_audio.stop_all_sounds()
    
    def play_note_for_column(self, column: int):
        """Play a specific note for a column (additional method for enhanced audio)."""
        self._pygame_audio.play_note_for_column(column)
    
    def set_volume(self, volume: float):
        """Set the volume for all sounds."""
        self._pygame_audio.set_volume(volume)
    
    def change_note_sequence(self, note_sequence: list):
        """Change the note sequence for the columns."""
        self._pygame_audio.change_note_sequence(note_sequence)
