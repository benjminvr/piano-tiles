import pygame
import sys
import random

from src.presentation.game_view import GameView, Color
from src.presentation.input_controller import InputController, GameAction
from src.infrastructure.pygame_audio import PygameAudio, PRESET_SEQUENCES

from audio_config import get_active_notes, get_active_song_info

class PianoTilesApp:
    def __init__(self):
        self.WIDTH = 400
        self.HEIGHT = 600

        self.view = GameView(self.WIDTH, self.HEIGHT)
        self.input_controller = InputController()
        self.clock = self.view.get_clock()

        try:
            notes = get_active_notes()
            song_info = get_active_song_info()
            self.audio = PygameAudio(note_sequence=notes)
            self.audio_enabled = True
        except Exception as e:
            self.audio = None
            self.audio_enabled = False

        self.game_state = "MENU"
        self.running = True

        self.tiles = []
        self.score = 0
        self.high_score = 0
        self.speed = 4.0
        self.tile_height = 150
        self.tile_width = self.WIDTH // 4
        self.last_spawn_time = 0
        self.base_spawn_interval = 800
        self.base_speed = self.speed

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
                    self._start_game()

            elif action == GameAction.RESTART:
                if self.game_state == "GAME_OVER":
                    self._start_game()

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
        self.last_spawn_time = pygame.time.get_ticks()
        self._spawn_row()

    def _update_game(self):
        current_time = pygame.time.get_ticks()

        spawn_interval = int(self.base_spawn_interval * (self.base_speed / max(self.speed, 0.0001)))
        if current_time - self.last_spawn_time > spawn_interval:
            self._spawn_row()
            self.last_spawn_time = current_time
            self.speed += 0.1

        for tile in self.tiles:
            tile['rect'].y += self.speed

        for tile in self.tiles:
            if (tile['rect'].bottom >= self.HEIGHT and
                tile['color'] == Color.BLACK and
                not tile['clicked']):
                self._game_over()
                return

        self.tiles = [t for t in self.tiles if t['rect'].top < self.HEIGHT]

    def _handle_click(self, position):
        clicked_tile = self.input_controller.check_tile_click(position, self.tiles)

        if clicked_tile:
            column = self.input_controller.get_clicked_tile_column(position, self.tile_width)

            if clicked_tile['color'] == Color.BLACK:
                clicked_tile['clicked'] = True
                clicked_tile['color'] = Color.GRAY
                self.score += 1

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

    def _render(self):
        if self.game_state == "MENU":
            self.view.draw_start_screen()

        elif self.game_state == "PLAYING":
            self.view.clear_screen()
            self.view.draw_grid_lines()
            self.view.draw_tiles(self.tiles)
            self.view.draw_score(self.score)
            self.view.draw_speed_indicator(self.speed / 4.0)

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

        self.view.update_display()

def main():
    app = PianoTilesApp()
    app.run()

if __name__ == "__main__":
    main()