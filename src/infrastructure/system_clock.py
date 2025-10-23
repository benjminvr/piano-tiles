

import pygame

class SystemClock:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()

    def get_current_time(self) -> int:
        return pygame.time.get_ticks()

    def get_delta_time(self) -> float:
        current = pygame.time.get_ticks()
        delta = (current - self.last_tick) / 1000.0
        self.last_tick = current
        return delta

    def tick(self, fps: int = 60):
        self.clock.tick(fps)