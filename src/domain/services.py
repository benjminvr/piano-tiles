
import random
from typing import List
from .entities import Tile, TileColor

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