

import pygame
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (180, 180, 180)
    RED = (255, 50, 50)
    BLUE = (50, 120, 255)
    GREEN = (50, 200, 100)
    DARK_GRAY = (100, 100, 100)
    LIGHT_GRAY = (220, 220, 220)

class GameView:

    def __init__(self, width: int = 400, height: int = 600):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Piano Tiles - Arquitectura en Capas")

        self.font_large = pygame.font.SysFont("arial", 40, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 30)
        self.font_small = pygame.font.SysFont("arial", 20)

        self.tile_width = width // 4
        self.tile_height = 150

        self.colors = Color()

    def clear_screen(self, color: tuple = None):
        if color is None:
            color = self.colors.WHITE
        self.screen.fill(color)

    def draw_tile(self, x: int, y: int, width: int, height: int,
                  color: tuple, clicked: bool = False):
        rect = pygame.Rect(x, y, width, height)

        tile_color = self.colors.GRAY if clicked else color
        pygame.draw.rect(self.screen, tile_color, rect)

        border_color = self.colors.DARK_GRAY
        pygame.draw.rect(self.screen, border_color, rect, 2)

    def draw_tiles(self, tiles: List[dict]):
        for tile in tiles:
            rect = tile['rect']
            self.draw_tile(
                rect.x,
                rect.y,
                rect.width,
                rect.height,
                tile['color'],
                tile.get('clicked', False)
            )

    def draw_score(self, score: int, x: int = 10, y: int = 10):
        score_text = self.font_medium.render(f"Score: {score}", True, self.colors.BLACK)

        background = pygame.Surface((score_text.get_width() + 20, score_text.get_height() + 10))
        background.fill(self.colors.LIGHT_GRAY)
        background.set_alpha(200)
        self.screen.blit(background, (x - 5, y - 5))

        self.screen.blit(score_text, (x, y))

    def draw_speed_indicator(self, speed: float, x: int = 10, y: int = 50):
        speed_text = self.font_small.render(f"Speed: {speed:.1f}x", True, self.colors.BLUE)
        self.screen.blit(speed_text, (x, y))

    def draw_game_over_screen(self, score: int, high_score: Optional[int] = None):
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill(self.colors.BLACK)
        overlay.set_alpha(150)
        self.screen.blit(overlay, (0, 0))

        title = self.font_large.render("GAME OVER", True, self.colors.RED)
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 80))
        self.screen.blit(title, title_rect)

        score_text = self.font_medium.render(f"Score: {score}", True, self.colors.WHITE)
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
        self.screen.blit(score_text, score_rect)

        if high_score is not None:
            high_score_text = self.font_small.render(
                f"Best: {high_score}",
                True,
                self.colors.GREEN if score >= high_score else self.colors.WHITE
            )
            high_score_rect = high_score_text.get_rect(center=(self.width // 2, self.height // 2 + 15))
            self.screen.blit(high_score_text, high_score_rect)

        restart_text = self.font_small.render("Press R to Restart", True, self.colors.WHITE)
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(restart_text, restart_rect)

        menu_text = self.font_small.render("Press M for Menu", True, self.colors.WHITE)
        menu_rect = menu_text.get_rect(center=(self.width // 2, self.height // 2 + 75))
        self.screen.blit(menu_text, menu_rect)

    def draw_victory_screen(self, score: int, song_name: str, high_score: Optional[int] = None):
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill(self.colors.BLACK)
        overlay.set_alpha(150)
        self.screen.blit(overlay, (0, 0))

        title = self.font_large.render("SONG COMPLETED!", True, self.colors.GREEN)
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(title, title_rect)

        won_text = self.font_medium.render("🎉 YOU WON! 🎉", True, self.colors.GREEN)
        won_rect = won_text.get_rect(center=(self.width // 2, self.height // 2 - 60))
        self.screen.blit(won_text, won_rect)

        song_text = self.font_medium.render(f"♪ {song_name}", True, self.colors.WHITE)
        song_rect = song_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
        self.screen.blit(song_text, song_rect)

        score_text = self.font_medium.render(f"Score: {score}", True, self.colors.WHITE)
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
        self.screen.blit(score_text, score_rect)

        if high_score is not None:
            if score >= high_score:
                high_score_text = self.font_small.render("🏆 NEW HIGH SCORE! 🏆", True, self.colors.GREEN)
            else:
                high_score_text = self.font_small.render(f"Best: {high_score}", True, self.colors.WHITE)
            high_score_rect = high_score_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
            self.screen.blit(high_score_text, high_score_rect)

        restart_text = self.font_small.render("Press R to Play Again", True, self.colors.WHITE)
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 80))
        self.screen.blit(restart_text, restart_rect)

        menu_text = self.font_small.render("Press M for Menu", True, self.colors.WHITE)
        menu_rect = menu_text.get_rect(center=(self.width // 2, self.height // 2 + 105))
        self.screen.blit(menu_text, menu_rect)

        quit_text = self.font_small.render("Press ESC to Quit", True, self.colors.LIGHT_GRAY)
        quit_rect = quit_text.get_rect(center=(self.width // 2, self.height // 2 + 130))
        self.screen.blit(quit_text, quit_rect)

    def draw_start_screen(self):
        self.clear_screen(self.colors.BLACK)

        title = self.font_large.render("PIANO TILES", True, self.colors.WHITE)
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 80))
        self.screen.blit(title, title_rect)

        subtitle = self.font_small.render("Song Mode", True, self.colors.GRAY)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, self.height // 2 - 40))
        self.screen.blit(subtitle, subtitle_rect)

        instructions = [
            "Click on BLACK tiles only!",
            "Don't let them reach the bottom",
            "",
            "Press SPACE to Start",
            "Press ESC to Quit"
        ]

        y_offset = self.height // 2
        for i, instruction in enumerate(instructions):
            if instruction == "":
                y_offset += 15
                continue
            text = self.font_small.render(instruction, True, self.colors.WHITE)
            text_rect = text.get_rect(center=(self.width // 2, y_offset + i * 30))
            self.screen.blit(text, text_rect)

    def draw_song_selection_menu(self, songs: list, selected_index: int):
        self.clear_screen(self.colors.BLACK)

        title = self.font_large.render("SELECT SONG", True, self.colors.WHITE)
        title_rect = title.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title, title_rect)

        y_start = 150
        for i, song in enumerate(songs):
            color = self.colors.BLUE if i == selected_index else self.colors.WHITE
            
            song_text = self.font_medium.render(f"{i+1}. {song['name']}", True, color)
            song_rect = song_text.get_rect(center=(self.width // 2, y_start + i * 70))
            self.screen.blit(song_text, song_rect)
            
            difficulty_text = self.font_small.render(f"[{song['difficulty']}]", True, color)
            difficulty_rect = difficulty_text.get_rect(center=(self.width // 2, y_start + i * 70 + 25))
            self.screen.blit(difficulty_text, difficulty_rect)

        controls = self.font_small.render("↑↓: Navigate | ENTER: Select | ESC: Quit", True, self.colors.GRAY)
        controls_rect = controls.get_rect(center=(self.width // 2, self.height - 50))
        self.screen.blit(controls, controls_rect)

    def draw_game_ui(self, score: int, song_name: str, progress: float = 0.0, speed: float = 4.0):
        self.draw_score(score, 10, 10)
        
        song_text = self.font_small.render(f"♪ {song_name}", True, self.colors.BLUE)
        self.screen.blit(song_text, (10, 45))
        
        speed_text = self.font_small.render(f"Speed: {speed:.1f}x", True, self.colors.RED)
        self.screen.blit(speed_text, (10, 70))
        
        if progress > 0:
            progress_bar_width = 200
            progress_bar_height = 8
            progress_x = self.width - progress_bar_width - 10
            progress_y = 15
            
            pygame.draw.rect(self.screen, self.colors.DARK_GRAY, 
                           (progress_x, progress_y, progress_bar_width, progress_bar_height))
            
            fill_width = int(progress_bar_width * min(progress, 1.0))
            if fill_width > 0:
                pygame.draw.rect(self.screen, self.colors.GREEN, 
                               (progress_x, progress_y, fill_width, progress_bar_height))

    def draw_countdown(self, countdown: int, song_name: str):
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill(self.colors.BLACK)
        overlay.set_alpha(100)
        self.screen.blit(overlay, (0, 0))
        
        song_text = self.font_medium.render(f"♪ {song_name}", True, self.colors.WHITE)
        song_rect = song_text.get_rect(center=(self.width // 2, self.height // 2 - 60))
        self.screen.blit(song_text, song_rect)
        
        if countdown > 0:
            countdown_text = self.font_large.render(str(countdown), True, self.colors.WHITE)
            countdown_rect = countdown_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(countdown_text, countdown_rect)
        else:
            start_text = self.font_large.render("GO!", True, self.colors.GREEN)
            start_rect = start_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(start_text, start_rect)

    def draw_pause_screen(self, score: int):
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill(self.colors.BLACK)
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        title = self.font_large.render("PAUSED", True, self.colors.BLUE)
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 60))
        self.screen.blit(title, title_rect)

        score_text = self.font_medium.render(f"Score: {score}", True, self.colors.WHITE)
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(score_text, score_rect)

        resume_text = self.font_small.render("Press P to Resume", True, self.colors.WHITE)
        resume_rect = resume_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(resume_text, resume_rect)

        quit_text = self.font_small.render("Press ESC to Quit", True, self.colors.LIGHT_GRAY)
        quit_rect = quit_text.get_rect(center=(self.width // 2, self.height // 2 + 80))
        self.screen.blit(quit_text, quit_rect)

    def draw_grid_lines(self):
        for i in range(1, 4):
            x = i * self.tile_width
            pygame.draw.line(
                self.screen,
                self.colors.DARK_GRAY,
                (x, 0),
                (x, self.height),
                2
            )

    def update_display(self):
        pygame.display.flip()

    def get_clock(self) -> pygame.time.Clock:
        return pygame.time.Clock()

    def quit(self):
        pygame.quit()