import math
import time
from typing import List, Dict
from ..utils.circle_classes import MediumCircle, SmallCircle
from .base_animation_controller import BaseAnimationController
from ..utils.settings import CIRCLE_MEDIUM_RADIUS, DEFAULT_ROTATION_DURATION


class LargeCircleRotationController(BaseAnimationController):
    """Handles large circle rotation animations"""

    def __init__(self, circle_system, rotation_duration: float = DEFAULT_ROTATION_DURATION):
        super().__init__(rotation_duration)
        self.system = circle_system
        self.is_rotating = False
        self.rotation_start = 0
        self.rotating_large_circle = None
        self.initial_angles: Dict = {}

    def start_rotation(
        self, large_circle, medium_circles: List[MediumCircle], small_circles: List[SmallCircle]
    ) -> None:
        """
        Initialize large circle rotation animation with explicitly provided circles.

        Args:
            large_circle: The large circle being rotated
            medium_circles: List of medium circles currently inside the large circle
            small_circles: List of small circles inside the medium circles
        """
        self.is_rotating = True
        self.rotation_start = time.time()
        self.rotating_large_circle = large_circle
        self.initial_angles.clear()

        # Store initial angles for all affected medium circles
        for medium_circle in medium_circles:
            # Store medium circle angles relative to large circle center
            dx = medium_circle.pos[0] - large_circle.pos[0]
            dy = medium_circle.pos[1] - large_circle.pos[1]
            self.initial_angles[medium_circle] = (math.atan2(dy, dx), math.sqrt(dx**2 + dy**2))

        # Store initial angles for all affected small circles
        for small_circle in small_circles:
            # Find the parent medium circle for this small circle
            for medium_circle in medium_circles:
                dx_medium = small_circle.pos[0] - medium_circle.pos[0]
                dy_medium = small_circle.pos[1] - medium_circle.pos[1]
                dist_to_medium = math.sqrt(dx_medium**2 + dy_medium**2)

                if (
                    dist_to_medium <= CIRCLE_MEDIUM_RADIUS
                ):  # If this small circle is inside this medium circle
                    self.initial_angles[small_circle] = (
                        math.atan2(dy_medium, dx_medium),
                        dist_to_medium,
                        medium_circle,
                    )
                    break

    def update(self, current_time: float) -> None:
        """Update large circle rotation animation"""
        if not self.is_rotating or not self.rotating_large_circle:
            return

        elapsed = current_time - self.rotation_start
        target_rotation = math.pi / 4  # 45 degrees rotation

        if elapsed >= self.rotation_duration:
            self._complete_rotation(target_rotation)
        else:
            self._update_rotation(elapsed, target_rotation)

    def _complete_rotation(self, target_rotation: float) -> None:
        """Complete the large circle rotation animation"""
        self.is_rotating = False
        large_circle = self.rotating_large_circle

        # Update final positions
        for obj, data in self.initial_angles.items():
            if isinstance(obj, MediumCircle):
                # Update medium circle position
                initial_angle, distance = data
                final_angle = initial_angle + target_rotation
                obj.pos[0] = large_circle.pos[0] + math.cos(final_angle) * distance
                obj.pos[1] = large_circle.pos[1] + math.sin(final_angle) * distance
            else:  # SmallCircle
                # Update small circle position relative to its parent medium circle
                initial_angle, distance, parent_circle = data
                final_angle = initial_angle + target_rotation
                obj.pos[0] = parent_circle.pos[0] + math.cos(final_angle) * distance
                obj.pos[1] = parent_circle.pos[1] + math.sin(final_angle) * distance

        self.rotating_large_circle = None

    def _update_rotation(self, elapsed: float, target_rotation: float) -> None:
        """Update the large circle rotation animation"""
        progress = self._calculate_animation_progress(elapsed, self.rotation_duration)
        current_rotation = target_rotation * progress
        large_circle = self.rotating_large_circle

        # Update positions during animation
        for obj, data in self.initial_angles.items():
            if isinstance(obj, MediumCircle):
                # Update medium circle position
                initial_angle, distance = data
                current_angle = initial_angle + current_rotation
                obj.pos[0] = large_circle.pos[0] + math.cos(current_angle) * distance
                obj.pos[1] = large_circle.pos[1] + math.sin(current_angle) * distance
            else:
                # Update small circle position relative to its parent medium circle
                initial_angle, distance, parent_circle = data
                current_angle = initial_angle + current_rotation
                obj.pos[0] = parent_circle.pos[0] + math.cos(current_angle) * distance
                obj.pos[1] = parent_circle.pos[1] + math.sin(current_angle) * distance
