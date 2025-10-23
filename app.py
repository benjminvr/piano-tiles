import pygame
import sys
import random

from src.presentation.game_view import GameView, Color
from src.presentation.input_controller import InputController, GameAction
from src.infrastructure.pygame_audio import PygameAudio, PRESET_SEQUENCES
from src.domain.services import SongService, TileGeneratorService

from audio_config import get_active_notes, get_active_song_info

class PianoTilesApp:
    def __init__(self):
        self.WIDTH = 400
        self.HEIGHT = 600

        self.view = GameView(self.WIDTH, self.HEIGHT)
        self.input_controller = InputController()
        self.clock = self.view.get_clock()
        
        self.song_service = SongService()
        self.tile_generator = TileGeneratorService(self.WIDTH // 4, 150)

        try:
            notes = get_active_notes()
            song_info = get_active_song_info()
            self.audio = PygameAudio(note_sequence=notes)
            self.audio_enabled = True
        except Exception as e:
            self.audio = None
            self.audio_enabled = False

        self.game_state = "SONG_MENU"
        self.running = True

        self.tiles = []
        self.score = 0
        self.high_score = 0
        self.speed = 4.0
        self.tile_height = 150
        self.tile_width = self.WIDTH // 4
        self.game_start_time = 0
        self.base_speed = self.speed
        
        self.selected_song_index = 0
        self.available_songs = self.song_service.get_available_songs()
        
        default_song = self.song_service.get_default_song()
        if default_song:
            self.song_service.select_song(default_song.id)

    def run(self):
        while self.running:
            actions = self.input_controller.process_events()
            self._handle_actions(actions)

            if self.game_state == "PLAYING":
                self._update_game()
            self._render()
            self.clock.tick(60)

        pygame.time.wait(100)

        self.view.quit()
        sys.exit()

    def _handle_actions(self, actions):
        for action, data in actions:
            if action == GameAction.QUIT:
                self.running = False

            elif action == GameAction.START:
                if self.game_state == "MENU":
                    self.game_state = "SONG_MENU"

            elif action == GameAction.MENU_UP:
                if self.game_state == "SONG_MENU":
                    self.selected_song_index = (self.selected_song_index - 1) % len(self.available_songs)

            elif action == GameAction.MENU_DOWN:
                if self.game_state == "SONG_MENU":
                    self.selected_song_index = (self.selected_song_index + 1) % len(self.available_songs)

            elif action == GameAction.MENU_SELECT:
                if self.game_state == "SONG_MENU":
                    selected_song = self.available_songs[self.selected_song_index]
                    self.song_service.select_song(selected_song['id'])
                    self._start_game()

            elif action == GameAction.RESTART:
                if self.game_state == "GAME_OVER" or self.game_state == "SONG_WON":
                    self._start_game()

            elif action == GameAction.BACK_TO_MENU:
                if self.game_state == "GAME_OVER" or self.game_state == "SONG_WON":
                    self.game_state = "SONG_MENU"

            elif action == GameAction.PAUSE:
                if self.game_state == "PLAYING":
                    self.game_state = "PAUSED"
                elif self.game_state == "PAUSED":
                    self.game_state = "PLAYING"

            elif action == GameAction.CLICK:
                if self.game_state == "PLAYING":
                    self._handle_click(data)

    def _start_game(self):
        self.game_state = "PLAYING"
        self.tiles.clear()
        self.score = 0
        self.speed = 4.0
        self.game_start_time = pygame.time.get_ticks() + 1000
        
        current_song = self.song_service.get_current_song()
        if current_song:
            current_song.reset()

    def _update_game(self):
        current_time = pygame.time.get_ticks()
        
        if current_time < self.game_start_time:
            return
            
        game_time = (current_time - self.game_start_time) / 1000.0
        
        self.speed = self.base_speed + (game_time * 0.1)
        
        current_song = self.song_service.get_current_song()
        if current_song:
            note = current_song.get_next_note_at_time(game_time, self.speed)
            if note:
                self._spawn_song_row(note['column'])

        for tile in self.tiles:
            tile['rect'].y += self.speed

        for tile in self.tiles:
            if (tile['rect'].bottom >= self.HEIGHT and
                tile['color'] == Color.BLACK and
                not tile['clicked']):
                self._game_over()
                return

        self.tiles = [t for t in self.tiles if t['rect'].top < self.HEIGHT]
        
        if current_song and current_song.is_completed() and len(self.tiles) == 0:
            self._song_completed()

    def _spawn_song_row(self, black_column: int):
        for i in range(4):
            color = Color.BLACK if i == black_column else Color.WHITE
            rect = pygame.Rect(
                i * self.tile_width,
                -self.tile_height,
                self.tile_width,
                self.tile_height
            )
            self.tiles.append({
                'rect': rect,
                'color': color,
                'clicked': False
            })

    def _handle_click(self, position):
        clicked_tile = self.input_controller.check_tile_click(position, self.tiles)

        if clicked_tile:
            column = self.input_controller.get_clicked_tile_column(position, self.tile_width)

            if clicked_tile['color'] == Color.BLACK:
                clicked_tile['clicked'] = True
                clicked_tile['color'] = Color.GRAY
                self.score += 10

                if self.audio_enabled and self.audio:
                    self.audio.play_note_for_column(column)
            else:
                if self.audio_enabled and self.audio:
                    self.audio.play_error_sound()
                self._game_over()

    def _spawn_row(self):
        black_index = random.randint(0, 3)

        for i in range(4):
            color = Color.BLACK if i == black_index else Color.WHITE
            rect = pygame.Rect(
                i * self.tile_width,
                -self.tile_height,
                self.tile_width,
                self.tile_height
            )
            self.tiles.append({
                'rect': rect,
                'color': color,
                'clicked': False
            })

    def _game_over(self):
        self.game_state = "GAME_OVER"

        if self.audio_enabled and self.audio:
            self.audio.play_game_over_sound()

        if self.score > self.high_score:
            self.high_score = self.score

    def _song_completed(self):
        self.game_state = "SONG_WON"
        
        if self.score > self.high_score:
            self.high_score = self.score

    def _render(self):
        if self.game_state == "MENU":
            self.view.draw_start_screen()

        elif self.game_state == "SONG_MENU":
            self.view.draw_song_selection_menu(self.available_songs, self.selected_song_index)

        elif self.game_state == "PLAYING":
            current_time = pygame.time.get_ticks()
            
            self.view.clear_screen()
            self.view.draw_grid_lines()
            self.view.draw_tiles(self.tiles)
            
            current_song = self.song_service.get_current_song()
            song_name = current_song.name if current_song else "No Song"
            
            if current_time < self.game_start_time:
                countdown = int((self.game_start_time - current_time) / 1000) + 1
                self.view.draw_countdown(countdown, song_name)
            else:
                progress = self._get_game_progress()
                self.view.draw_game_ui(self.score, song_name, progress)

        elif self.game_state == "PAUSED":
            self.view.clear_screen()
            self.view.draw_grid_lines()
            self.view.draw_tiles(self.tiles)
            self.view.draw_pause_screen(self.score)

        elif self.game_state == "GAME_OVER":
            self.view.clear_screen()
            self.view.draw_grid_lines()
            self.view.draw_tiles(self.tiles)
            self.view.draw_game_over_screen(
                self.score,
                self.high_score if self.high_score > 0 else None
            )

        elif self.game_state == "SONG_WON":
            self.view.clear_screen()
            self.view.draw_grid_lines()
            self.view.draw_tiles(self.tiles)
            current_song = self.song_service.get_current_song()
            song_name = current_song.name if current_song else "Song"
            self.view.draw_victory_screen(
                self.score,
                song_name,
                self.high_score if self.high_score > 0 else None
            )

        self.view.update_display()

    def _get_game_progress(self) -> float:
        current_song = self.song_service.get_current_song()
        if not current_song or self.game_start_time == 0:
            return 0.0
            
        current_time = pygame.time.get_ticks()
        game_time = (current_time - self.game_start_time) / 1000.0
        return current_song.get_progress(game_time)

def main():
    app = PianoTilesApp()
    app.run()

if __name__ == "__main__":
    main()