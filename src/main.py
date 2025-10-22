# app.py
import pygame
import sys
from domain.entities import Board, GameState
from domain.services import spawn_row, update_board, process_click, check_missed_tiles

# --- Configuración general ---
WIDTH, HEIGHT = 400, 600
TILE_WIDTH = WIDTH // 4
TILE_HEIGHT = 150
BASE_SPAWN_INTERVAL = 800
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

# --- Inicialización ---
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piano Tiles (Refactor)")
font = pygame.font.SysFont("arial", 30)
clock = pygame.time.Clock()

# --- Estado del juego ---
board = Board(WIDTH, HEIGHT)
state = GameState()
last_spawn_time = 0


def reset_game():
    global board, state, last_spawn_time
    board = Board(WIDTH, HEIGHT)
    state = GameState()
    last_spawn_time = pygame.time.get_ticks()
    spawn_row(board, TILE_WIDTH, TILE_HEIGHT)


def draw_tiles():
    for t in board.tiles:
        pygame.draw.rect(SCREEN, t.color, (t.x, t.y, t.width, t.height))
        pygame.draw.rect(SCREEN, (180, 180, 180), (t.x, t.y, t.width, t.height), 1)


# --- Inicio ---
reset_game()
running = True

while running:
    SCREEN.fill(WHITE)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if state.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            process_click(board, state, pygame.mouse.get_pos())

    if state.game_over:
        text = font.render(f"Game Over! Score: {state.score}", True, RED)
        tip = font.render("Press R to restart", True, RED)
        SCREEN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - 40))
        SCREEN.blit(tip, (WIDTH/2 - tip.get_width()/2, HEIGHT/2))
        pygame.display.flip()
        clock.tick(60)
        continue

    # --- Generación de nuevas filas ---
    spawn_interval = BASE_SPAWN_INTERVAL * (state.base_speed / state.speed)
    if current_time - last_spawn_time > spawn_interval:
        spawn_row(board, TILE_WIDTH, TILE_HEIGHT)
        last_spawn_time = current_time
        state.speed += state.speed_increment

    # --- Actualización y validación ---
    update_board(board, state)
    check_missed_tiles(board, state)

    # --- Renderizado ---
    draw_tiles()
    score_text = font.render(f"Score: {state.score}", True, BLACK)
    SCREEN.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
