import math
import time
from typing import Dict, Tuple, Union
from ..utils.circle_classes import MediumCircle, SmallCircle
from .base_animation_controller import BaseAnimationController
from ..utils.settings import DEFAULT_ROTATION_DURATION


class CenterRotationController(BaseAnimationController):
    """Handles center rotation animations."""

    def __init__(self, circle_system, rotation_duration: float = DEFAULT_ROTATION_DURATION):
        super().__init__(rotation_duration)
        self.system = circle_system
        self.is_rotating = False
        self.rotation_start = 0
        self.initial_angles: Dict[Union[MediumCircle, SmallCircle], Tuple] = {}

    def start_rotation(self) -> None:
        """Initialize center rotation animation for all circles."""
        self.is_rotating = True
        self.rotation_start = time.time()
        self.initial_angles.clear()
        center = self.system.center

        # Calculate initial angles for medium circles
        for medium_circle in self.system.medium_circles:
            dx = medium_circle.pos[0] - center[0]
            dy = medium_circle.pos[1] - center[1]
            self.initial_angles[medium_circle] = (
                math.atan2(dy, dx),
                math.sqrt(dx**2 + dy**2),
            )

            # Calculate initial angles for small circles inside each medium circle
            circles_inside = self.system.circle_manager.get_circles_inside(medium_circle)
            for small_circle in circles_inside:
                dx_small = small_circle.pos[0] - medium_circle.pos[0]
                dy_small = small_circle.pos[1] - medium_circle.pos[1]
                self.initial_angles[small_circle] = (
                    math.atan2(dy_small, dx_small),
                    math.sqrt(dx_small**2 + dy_small**2),
                    medium_circle,
                )

    def update(self, current_time: float) -> None:
        """Update center rotation animation."""
        if not self.is_rotating:
            return

        elapsed = current_time - self.rotation_start
        target_rotation = math.pi / 4

        if elapsed >= self.rotation_duration:
            self._complete_rotation(target_rotation)
        else:
            self._update_rotation(elapsed, target_rotation)

    def _complete_rotation(self, target_rotation: float) -> None:
        """Complete the center rotation animation."""
        self.is_rotating = False
        center = self.system.center

        for obj, data in self.initial_angles.items():
            if isinstance(obj, MediumCircle):
                initial_angle, distance = data
                final_angle = initial_angle + target_rotation
                obj.pos[0] = center[0] + math.cos(final_angle) * distance
                obj.pos[1] = center[1] + math.sin(final_angle) * distance
            else:  # SmallCircle
                initial_angle, distance, parent_circle = data
                final_angle = initial_angle + target_rotation
                obj.pos[0] = parent_circle.pos[0] + math.cos(final_angle) * distance
                obj.pos[1] = parent_circle.pos[1] + math.sin(final_angle) * distance

    def _update_rotation(self, elapsed: float, target_rotation: float) -> None:
        """Update the center rotation animation."""
        progress = self._calculate_animation_progress(elapsed, self.rotation_duration)
        current_rotation = target_rotation * progress
        center = self.system.center

        for obj, data in self.initial_angles.items():
            if isinstance(obj, MediumCircle):
                initial_angle, distance = data
                current_angle = initial_angle + current_rotation
                obj.pos[0] = center[0] + math.cos(current_angle) * distance
                obj.pos[1] = center[1] + math.sin(current_angle) * distance
            else:
                initial_angle, distance, parent_circle = data
                current_angle = initial_angle + current_rotation
                obj.pos[0] = parent_circle.pos[0] + math.cos(current_angle) * distance
                obj.pos[1] = parent_circle.pos[1] + math.sin(current_angle) * distance
