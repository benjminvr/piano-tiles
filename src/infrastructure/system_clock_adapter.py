from ..domain.ports import ClockPort
from .system_clock import SystemClock


class SystemClockAdapter(ClockPort):
    """
    Adapter that implements ClockPort interface using SystemClock implementation.
    This bridges the domain layer with the pygame clock infrastructure.
    """
    
    def __init__(self):
        self._system_clock = SystemClock()
    
    def get_current_time(self) -> int:
        """Get the current time in milliseconds."""
        return self._system_clock.get_current_time()
    
    def get_delta_time(self) -> float:
        """Get the time elapsed since the last call in seconds."""
        return self._system_clock.get_delta_time()
    
    def tick(self, fps: int = 60):
        """Control the frame rate by limiting the clock tick."""
        self._system_clock.tick(fps)
