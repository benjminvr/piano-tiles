
import random
import json
import os
from typing import List, Dict, Any, Optional
from .entities import Tile, TileColor

class Song:
    def __init__(self, song_id: str, name: str, tempo: int, difficulty: str, notes: List[Dict[str, Any]]):
        self.id = song_id
        self.name = name
        self.tempo = tempo
        self.difficulty = difficulty
        self.notes = sorted(notes, key=lambda x: x['time'])
        self.current_note_index = 0
        self.duration = max(note['time'] for note in notes) if notes else 0
        self.last_spawned_time = -999
        self.song_completed = False
        
    def get_next_note_at_time(self, current_time: float, current_speed: float = 4.0) -> Optional[Dict[str, Any]]:
        if self.song_completed or self.current_note_index >= len(self.notes):
            return None
            
        spawn_time_offset = 2.0
        
        note = self.notes[self.current_note_index]
        spawn_time = note['time'] - spawn_time_offset
        
        if current_time >= spawn_time:
            self.current_note_index += 1
            self.last_spawned_time = current_time
            
            if self.current_note_index >= len(self.notes):
                self.song_completed = True
                
            return note
                
        return None
    
    def has_more_notes(self) -> bool:
        return not self.song_completed and self.current_note_index < len(self.notes)
    
    def get_progress(self, current_time: float) -> float:
        if self.duration <= 0:
            return 1.0
        return min(current_time / self.duration, 1.0)
    
    def is_completed(self) -> bool:
        return self.song_completed
    
    def reset(self):
        self.current_note_index = 0
        self.last_spawned_time = -999
        self.song_completed = False

class SongService:
    def __init__(self, songs_file_path: str = None):
        self.songs: Dict[str, Song] = {}
        self.current_song: Optional[Song] = None
        
        if songs_file_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            songs_file_path = os.path.join(base_dir, 'songs.json')
            
        self.load_songs(songs_file_path)
    
    def load_songs(self, songs_file_path: str):
        try:
            with open(songs_file_path, 'r', encoding='utf-8') as f:
                songs_data = json.load(f)
                
            for song_id, song_data in songs_data.items():
                song = Song(
                    song_id=song_id,
                    name=song_data['name'],
                    tempo=song_data['tempo'],
                    difficulty=song_data.get('difficulty', 'Medium'),
                    notes=song_data['notes']
                )
                self.songs[song_id] = song
                
        except FileNotFoundError:
            print(f"Songs file {songs_file_path} not found")
        except json.JSONDecodeError:
            print(f"Error parsing {songs_file_path}")
    
    def get_available_songs(self) -> List[Dict[str, str]]:
        return [
            {
                'id': song.id,
                'name': song.name,
                'difficulty': song.difficulty,
                'tempo': song.tempo
            }
            for song in self.songs.values()
        ]
    
    def select_song(self, song_id: str) -> bool:
        if song_id in self.songs:
            self.current_song = self.songs[song_id]
            self.current_song.reset()
            return True
        return False
    
    def get_current_song(self) -> Optional[Song]:
        return self.current_song
    
    def get_default_song(self) -> Optional[Song]:
        if 'twinkle_star' in self.songs:
            return self.songs['twinkle_star']
        elif self.songs:
            return list(self.songs.values())[0]
        return None

class TileGeneratorService:

    def __init__(self, tile_width: int, tile_height: int):
        self.tile_width = tile_width
        self.tile_height = tile_height

    def generate_row(self, y_position: int = 0) -> List[Tile]:

        black_column = random.randint(0, 3)
        tiles = []

        for i in range(4):
            color = TileColor.BLACK if i == black_column else TileColor.WHITE
            tile = Tile(
                x=i * self.tile_width,
                y=y_position,
                width=self.tile_width,
                height=self.tile_height,
                color=color
            )
            tiles.append(tile)

        return tiles

    def generate_song_row(self, black_column: int, y_position: int = 0) -> List[Tile]:
        tiles = []
        for i in range(4):
            color = TileColor.BLACK if i == black_column else TileColor.WHITE
            tile = Tile(
                x=i * self.tile_width,
                y=y_position,
                width=self.tile_width,
                height=self.tile_height,
                color=color
            )
            tiles.append(tile)
        return tiles

class GameValidationService:

    @staticmethod
    def is_valid_click(tile: Tile) -> bool:

        return tile.is_black() and not tile.clicked

    @staticmethod
    def check_game_over_condition(tiles: List[Tile], bottom_boundary: int) -> bool:

        for tile in tiles:
            if tile.is_black() and not tile.clicked and (tile.y + tile.height >= bottom_boundary):
                return True
        return False