
import pygame
import numpy as np
from typing import Dict, Optional
import os

class PianoNoteGenerator:

    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate

    def generate_piano_note(self, frequency: float, duration: float = 0.5) -> pygame.mixer.Sound:

        n_samples = int(self.sample_rate * duration)

        t = np.linspace(0, duration, n_samples, False)

        wave = np.zeros_like(t)

        wave += np.sin(2 * np.pi * frequency * t)

        wave += 0.5 * np.sin(2 * np.pi * frequency * 2 * t)

        wave += 0.25 * np.sin(2 * np.pi * frequency * 3 * t)

        wave += 0.125 * np.sin(2 * np.pi * frequency * 4 * t)

        wave = wave / np.max(np.abs(wave))

        envelope = self._create_adsr_envelope(n_samples, duration)
        wave = wave * envelope

        wave = np.int16(wave * 32767)

        stereo_wave = np.column_stack((wave, wave))

        sound = pygame.mixer.Sound(buffer=stereo_wave)

        return sound

    def _create_adsr_envelope(self, n_samples: int, duration: float) -> np.ndarray:
        envelope = np.ones(n_samples)

        attack_samples = int(n_samples * 0.05)
        decay_samples = int(n_samples * 0.1)
        release_samples = int(n_samples * 0.3)

        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

        if decay_samples > 0:
            decay_end = attack_samples + decay_samples
            envelope[attack_samples:decay_end] = np.linspace(1, 0.7, decay_samples)

        sustain_start = attack_samples + decay_samples
        sustain_end = n_samples - release_samples
        envelope[sustain_start:sustain_end] = 0.7

        if release_samples > 0:
            envelope[-release_samples:] = np.linspace(0.7, 0, release_samples)

        return envelope

class PygameAudio:

    NOTES = {
        'C4': 261.63,
        'D4': 293.66,
        'E4': 329.63,
        'F4': 349.23,
        'G4': 392.00,
        'A4': 440.00,
        'B4': 493.88,
        'C5': 523.25,
    }

    def __init__(self, note_sequence: Optional[list] = None):

        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

        if note_sequence is None:

            note_sequence = ['C4', 'E4', 'G4', 'C5']

        self.note_sequence = note_sequence

        self.note_generator = PianoNoteGenerator()

        self.column_sounds: Dict[int, pygame.mixer.Sound] = {}

        self._generate_column_sounds()

        self.error_sound: Optional[pygame.mixer.Sound] = None
        self.game_over_sound: Optional[pygame.mixer.Sound] = None

        self._generate_special_sounds()


    def _generate_column_sounds(self):
        for column in range(4):
            note_name = self.note_sequence[column]
            frequency = self.NOTES[note_name]

            print(f"   Generando nota {note_name} ({frequency:.2f} Hz) para columna {column}")

            sound = self.note_generator.generate_piano_note(frequency, duration=0.4)
            sound.set_volume(0.6)

            self.column_sounds[column] = sound

    def _generate_special_sounds(self):
        error_freq = 110.0
        self.error_sound = self.note_generator.generate_piano_note(error_freq, duration=0.3)
        self.error_sound.set_volume(0.5)

        gameover_freq = 130.81
        self.game_over_sound = self.note_generator.generate_piano_note(gameover_freq, duration=0.8)
        self.game_over_sound.set_volume(0.7)

    def play_note_for_column(self, column: int):
        if column in self.column_sounds:
            self.column_sounds[column].play()
        else:
            print(f"⚠️ Advertencia: Columna {column} fuera de rango")

    def play_click_sound(self, column: Optional[int] = None):
        if column is not None:
            self.play_note_for_column(column)
        else:

            self.column_sounds[0].play()

    def play_error_sound(self):
        if self.error_sound:
            self.error_sound.play()

    def play_game_over_sound(self):
        if self.game_over_sound:

            self.stop_all_sounds()
            pygame.time.wait(100)
            self.game_over_sound.play()

    def stop_all_sounds(self):
        pygame.mixer.stop()

    def set_volume(self, volume: float):
        volume = max(0.0, min(1.0, volume))

        for sound in self.column_sounds.values():
            sound.set_volume(volume * 0.6)

        if self.error_sound:
            self.error_sound.set_volume(volume * 0.5)

        if self.game_over_sound:
            self.game_over_sound.set_volume(volume * 0.7)

    def change_note_sequence(self, note_sequence: list):
        if len(note_sequence) != 4:
            return

        self.note_sequence = note_sequence
        self._generate_column_sounds()

PRESET_SEQUENCES = {
    'c_major': ['C4', 'E4', 'G4', 'C5'],
    'g_major': ['G4', 'B4', 'D4', 'G4'],
    'a_minor': ['A4', 'C4', 'E4', 'A4'],
    'f_major': ['F4', 'A4', 'C5', 'F4'],
    'pentatonic': ['C4', 'D4', 'E4', 'G4'],
    'chromatic': ['C4', 'D4', 'E4', 'F4'],
}