
from dataclasses import dataclass
from typing import Tuple
from enum import Enum

class TileColor(Enum):
    BLACK = "black"
    WHITE = "white"

@dataclass
class Tile:
    x: int
    y: int
    width: int
    height: int
    color: TileColor
    clicked: bool = False

    def is_black(self) -> bool:
        return self.color == TileColor.BLACK

    def is_white(self) -> bool:
        return self.color == TileColor.WHITE

    def mark_as_clicked(self):
        self.clicked = True

    def contains_point(self, x: int, y: int) -> bool:
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

@dataclass
class Score:
    value: int = 0
    player_name: str = "Player"

    def increment(self, amount: int = 1):
        self.value += amount

    def reset(self):
        self.value = 0

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

@dataclass
class Board:
    width: int
    height: int
    columns: int = 4
    tiles: list = None

    def __post_init__(self):
        if self.tiles is None:
            self.tiles = []

    def add_tile(self, tile: Tile):
        self.tiles.append(tile)

    def remove_tile(self, tile: Tile):
        if tile in self.tiles:
            self.tiles.remove(tile)

    def clear_tiles(self):
        self.tiles.clear()

    def get_column_width(self) -> int:
        return self.width // self.columns