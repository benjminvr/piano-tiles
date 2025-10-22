# src/domain/services.py
import random
from typing import List
from .entities import Tile, Board, GameState

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)


def spawn_row(board: Board, tile_width: int, tile_height: int):
    """Crea una nueva fila de 4 tiles, uno negro y tres blancos."""
    black_index = random.randint(0, 3)
    for i in range(4):
        color = BLACK if i == black_index else WHITE
        tile = Tile(i * tile_width, -tile_height, tile_width, tile_height, color)
        board.tiles.append(tile)


def update_board(board: Board, state: GameState):
    """Mueve tiles y elimina los que salen de pantalla."""
    for tile in board.tiles:
        tile.move(state.speed)
    board.remove_offscreen()


def process_click(board: Board, state: GameState, pos):
    """Procesa clic del usuario sobre un tile."""
    for tile in board.tiles:
        if tile.contains(pos) and not tile.clicked:
            if tile.color == BLACK:
                tile.color = GRAY
                tile.clicked = True
                state.score += 1
                state.speed += state.speed_increment / 10
            else:
                state.game_over = True
            break


def check_missed_tiles(board: Board, state: GameState):
    """Finaliza el juego si un tile negro llega al fondo sin ser tocado."""
    for tile in board.tiles:
        if tile.is_missed(board.height):
            state.game_over = True
            break
