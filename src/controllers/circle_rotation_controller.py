import math
import time
from typing import List, Dict
from ..utils.circle_classes import MediumCircle, SmallCircle
from .base_animation_controller import BaseAnimationController
from ..utils.settings import DEFAULT_ROTATION_DURATION


class CircleRotationController(BaseAnimationController):
    """Handles individual circle rotation animations."""

    def __init__(self, circle_system, rotation_duration: float = DEFAULT_ROTATION_DURATION):
        super().__init__(rotation_duration)
        self.system = circle_system
        self.pending_post_rotation = False
        self._animating_circles: Dict[MediumCircle, float] = {}  # Tracks active animations

    @property
    def rotation_duration(self) -> float:
        return self._rotation_duration

    @rotation_duration.setter
    def rotation_duration(self, duration: float) -> None:
        """Update rotation duration and adjust ongoing animations."""
        old_duration = self._rotation_duration
        self._rotation_duration = duration

        current_time = time.time()
        # Adjust animation timing for all active animations
        for circle, start_time in self._animating_circles.items():
            if circle.is_animating:
                elapsed = current_time - start_time
                if old_duration != 0:
                    progress = elapsed / old_duration
                else:
                    progress = 0
                # Adjust the start time to maintain the same relative progress
                new_elapsed = progress * duration
                circle.animation_start = current_time - new_elapsed

    def start_rotation(
        self, medium_circle: MediumCircle, circles_inside: List[SmallCircle]
    ) -> None:
        """Start rotation animation for a specific medium circle."""
        medium_circle.is_animating = True
        start_time = time.time()
        medium_circle.animation_start = start_time
        medium_circle.target_rotation = math.pi / 4
        medium_circle.initial_angles = {}
        self.pending_post_rotation = True
        self._animating_circles[medium_circle] = start_time

        for circle in circles_inside:
            dx = circle.pos[0] - medium_circle.pos[0]
            dy = circle.pos[1] - medium_circle.pos[1]
            medium_circle.initial_angles[circle] = (math.atan2(dy, dx), math.sqrt(dx**2 + dy**2))

    def update(self, current_time: float) -> None:
        """Update individual circle rotation animations."""
        completed_circles = []

        for medium_circle in self._animating_circles:
            if medium_circle.is_animating:
                elapsed = current_time - medium_circle.animation_start
                # print(f"elapsed: {elapsed}, rotation_duration: {self.rotation_duration}")
                if elapsed >= self.rotation_duration:
                    self._complete_rotation(medium_circle)
                    completed_circles.append(medium_circle)
                else:
                    self._update_rotation(medium_circle, elapsed)

        # Clean up completed animations
        for circle in completed_circles:
            del self._animating_circles[circle]

    def _complete_rotation(self, medium_circle: MediumCircle) -> None:
        """Complete rotation animation for a specific medium circle."""
        medium_circle.is_animating = False
        for circle, (initial_angle, distance) in medium_circle.initial_angles.items():
            final_angle = initial_angle + medium_circle.target_rotation
            circle.pos[0] = medium_circle.pos[0] + math.cos(final_angle) * distance
            circle.pos[1] = medium_circle.pos[1] + math.sin(final_angle) * distance

    def _update_rotation(self, medium_circle: MediumCircle, elapsed: float) -> None:
        """Update rotation animation for a specific medium circle."""
        progress = self._calculate_animation_progress(elapsed, self.rotation_duration)
        current_rotation = medium_circle.target_rotation * progress

        for circle, (initial_angle, distance) in medium_circle.initial_angles.items():
            current_angle = initial_angle + current_rotation
            circle.pos[0] = medium_circle.pos[0] + math.cos(current_angle) * distance
            circle.pos[1] = medium_circle.pos[1] + math.sin(current_angle) * distance
