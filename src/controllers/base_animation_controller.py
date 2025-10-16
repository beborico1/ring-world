import math
from ..utils.settings import DEFAULT_ROTATION_DURATION


class BaseAnimationController:
    """Base class for animation controllers with common utilities."""

    def __init__(self, rotation_duration: float = DEFAULT_ROTATION_DURATION):
        self._rotation_duration = rotation_duration

    @property
    def rotation_duration(self) -> float:
        return self._rotation_duration

    @rotation_duration.setter
    def rotation_duration(self, duration: float) -> None:
        self._rotation_duration = duration

    @staticmethod
    def _calculate_animation_progress(elapsed: float, duration: float) -> float:
        """Calculate smooth animation progress using cosine interpolation."""
        progress = elapsed / duration
        return -math.cos(progress * math.pi) / 2 + 0.5
