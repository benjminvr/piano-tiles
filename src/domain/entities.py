# src/domain/entities.py
from dataclasses import dataclass, field
from typing import List, Tuple

Color = Tuple[int, int, int]


@dataclass
class Tile:
    x: int
    y: int
    width: int
    height: int
    color: Color
    clicked: bool = False

    def move(self, speed: float):
        self.y += speed

    def contains(self, pos: Tuple[int, int]) -> bool:
        px, py = pos
        return self.x <= px < self.x + self.width and self.y <= py < self.y + self.height

    def is_missed(self, screen_height: int) -> bool:
        return self.y + self.height >= screen_height and self.color == (0, 0, 0) and not self.clicked


@dataclass
class Board:
    width: int
    height: int
    tiles: List[Tile] = field(default_factory=list)

    def remove_offscreen(self):
        self.tiles = [t for t in self.tiles if t.y < self.height]


@dataclass
class GameState:
    score: int = 0
    speed: float = 4.0
    base_speed: float = 4.0
    speed_increment: float = 0.5
    game_over: bool = False
