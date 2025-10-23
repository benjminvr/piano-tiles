

import pygame
from typing import Optional, Tuple
from enum import Enum

class GameAction(Enum):
    NONE = 0
    QUIT = 1
    RESTART = 2
    START = 3
    PAUSE = 4
    RESUME = 5
    CLICK = 6

class InputController:


    def __init__(self):
        self.mouse_position: Optional[Tuple[int, int]] = None
        self.last_click_position: Optional[Tuple[int, int]] = None

    def process_events(self) -> list:
        actions = []

        for event in pygame.event.get():
            action = self._process_single_event(event)
            if action:
                actions.append(action)

        return actions

    def _process_single_event(self, event: pygame.event.Event) -> Optional[Tuple[GameAction, any]]:
        if event.type == pygame.QUIT:
            return (GameAction.QUIT, None)

        if event.type == pygame.KEYDOWN:
            return self._process_keydown(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._process_mouse_click(event)

        if event.type == pygame.MOUSEMOTION:
            self.mouse_position = event.pos

        return None

    def _process_keydown(self, event: pygame.event.Event) -> Optional[Tuple[GameAction, any]]:
        key = event.key

        if key == pygame.K_ESCAPE:
            return (GameAction.QUIT, None)

        if key == pygame.K_r:
            return (GameAction.RESTART, None)

        if key == pygame.K_SPACE:
            return (GameAction.START, None)

        if key == pygame.K_p:
            return (GameAction.PAUSE, None)

        return None

    def _process_mouse_click(self, event: pygame.event.Event) -> Optional[Tuple[GameAction, any]]:
        if event.button == 1:
            position = event.pos
            self.last_click_position = position
            return (GameAction.CLICK, position)

        return None

    def get_mouse_position(self) -> Optional[Tuple[int, int]]:
        return self.mouse_position

    def get_last_click_position(self) -> Optional[Tuple[int, int]]:
        return self.last_click_position

    def check_tile_click(self, click_position: Tuple[int, int], tiles: list) -> Optional[dict]:
        x, y = click_position

        for tile in tiles:
            if tile['rect'].collidepoint(x, y) and not tile.get('clicked', False):
                return tile

        return None

    def get_clicked_tile_column(self, click_position: Tuple[int, int], tile_width: int) -> int:
        x, y = click_position
        column = x // tile_width
        return max(0, min(3, column))

    def is_within_game_area(self, position: Tuple[int, int], width: int, height: int) -> bool:
        x, y = position
        return 0 <= x < width and 0 <= y < height

    def reset(self):
        self.mouse_position = None
        self.last_click_position = None

    @staticmethod
    def wait_for_key(key: int, timeout: Optional[int] = None) -> bool:
        start_time = pygame.time.get_ticks()

        while True:
            if timeout and (pygame.time.get_ticks() - start_time) > timeout:
                return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == key:
                    return True

            pygame.time.wait(10)

    @staticmethod
    def clear_event_queue():
        pygame.event.clear()