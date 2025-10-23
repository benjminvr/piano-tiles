import json
from typing import List, Dict, Any

class Song:
    def __init__(self, name: str, tempo: int, notes: List[Dict[str, Any]], difficulty: str = "Medium"):
        self.name = name
        self.tempo = tempo
        self.difficulty = difficulty
        self.notes = sorted(notes, key=lambda x: x['time'])
        self.current_note_index = 0
        
    def get_next_note(self) -> Dict[str, Any]:
        if self.current_note_index < len(self.notes):
            note = self.notes[self.current_note_index]
            self.current_note_index += 1
            return note
        return None
    
    def has_more_notes(self) -> bool:
        return self.current_note_index < len(self.notes)
    
    def reset(self):
        self.current_note_index = 0

class SongManager:
    def __init__(self, songs_file: str = "songs.json"):
        self.songs = {}
        self.current_song = None
        self.load_songs(songs_file)
    
    def load_songs(self, songs_file: str):
        try:
            with open(songs_file, 'r', encoding='utf-8') as f:
                songs_data = json.load(f)
                
            for song_id, song_data in songs_data.items():
                self.songs[song_id] = Song(
                    name=song_data['name'],
                    tempo=song_data['tempo'],
                    notes=song_data['notes'],
                    difficulty=song_data.get('difficulty', 'Medium')
                )
        except FileNotFoundError:
            print(f"Songs file {songs_file} not found")
        except json.JSONDecodeError:
            print(f"Error parsing {songs_file}")
    
    def select_song(self, song_id: str) -> bool:
        if song_id in self.songs:
            self.current_song = self.songs[song_id]
            self.current_song.reset()
            return True
        return False
    
    def get_available_songs(self) -> List[str]:
        return list(self.songs.keys())
    
    def get_current_song(self) -> Song:
        return self.current_song