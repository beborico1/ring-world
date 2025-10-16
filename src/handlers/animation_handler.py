import time
import pygame
from ..controllers.center_rotation_controller import CenterRotationController
from ..controllers.large_circle_rotation_controller import LargeCircleRotationController
from ..controllers.circle_rotation_controller import CircleRotationController
from ..utils.geometry import get_circles_inside_at_position
from ..utils.settings import CIRCLE_MEDIUM_RADIUS, DEFAULT_ROTATION_DURATION, PHASE_PLACEMENT


class AnimationHandler:
    """Handles animations for circle rotations in the game system."""

    def __init__(self, circle_system, rotation_duration: float = DEFAULT_ROTATION_DURATION):
        self.system = circle_system
        self._rotation_duration = rotation_duration
        self.center_controller = CenterRotationController(circle_system, rotation_duration)
        self.circle_controller = CircleRotationController(circle_system, rotation_duration)
        self.large_circle_controller = LargeCircleRotationController(
            circle_system, rotation_duration
        )

        # Load sound effects
        self.rot_start_sound = pygame.mixer.Sound("assets/sounds/rot_start.wav")
        self.rot_loop_sound = pygame.mixer.Sound("assets/sounds/rot.wav")
        self.rot_stop_sound = pygame.mixer.Sound("assets/sounds/rot_stop.wav")

        # Sound control flags
        self.is_playing_rotation = False
        self.rotation_sound_started = False
        self.last_loop_time = 0

        # Backward compatibility attributes
        self.is_center_rotating = False
        self.center_rotation_start = 0
        self.center_initial_angles = {}
        self.pending_post_rotation = False

    @property
    def rotation_duration(self) -> float:
        return self._rotation_duration

    @rotation_duration.setter
    def rotation_duration(self, duration: float) -> None:
        """Update rotation duration for all controllers."""
        self._rotation_duration = duration
        self.center_controller.rotation_duration = duration
        self.circle_controller.rotation_duration = duration
        self.large_circle_controller.rotation_duration = duration

    def _start_rotation_sound_sequence(self):
        """Start the rotation sound sequence"""
        # Stop any ongoing sounds first
        # pygame.mixer.stop()
        self.rot_start_sound.play()
        self.rotation_sound_started = True
        self.is_playing_rotation = True
        self.last_loop_time = time.time()

    def _update_rotation_sounds(self, current_time):
        """Update the rotation sound sequence"""
        if not self.is_playing_rotation:
            return

        # Wait for rot_start to finish before starting the loop sound
        if self.rotation_sound_started and not pygame.mixer.get_busy():
            self.rot_loop_sound.play()
            self.rotation_sound_started = False
            self.last_loop_time = current_time

        # If the loop sound has finished, restart it if we're still rotating
        if (
            not self.rotation_sound_started
            and current_time - self.last_loop_time >= self.rot_loop_sound.get_length()
        ):
            if self.is_any_circle_animating():
                self.rot_loop_sound.play()
                self.last_loop_time = current_time

    def _stop_rotation_sounds(self):
        """Stop rotation sounds and play the stop sound"""
        if self.is_playing_rotation:
            pygame.mixer.stop()
            self.rot_stop_sound.play()
            self.is_playing_rotation = False
            self.rotation_sound_started = False

    def reset(self):
        """Reset all animation states."""
        # Stop any playing sounds
        pygame.mixer.stop()
        self.is_playing_rotation = False
        self.rotation_sound_started = False

        self.center_controller = CenterRotationController(self.system, self.rotation_duration)
        self.circle_controller = CircleRotationController(self.system, self.rotation_duration)
        self.large_circle_controller = LargeCircleRotationController(
            self.system, self.rotation_duration
        )

        # Reset backward compatibility attributes
        self.is_center_rotating = False
        self.center_rotation_start = 0
        self.center_initial_angles.clear()
        self.pending_post_rotation = False

        for medium_circle in self.system.medium_circles:
            medium_circle.is_animating = False
            medium_circle.animation_start = 0
            medium_circle.target_rotation = 0
            medium_circle.initial_angles = {}

    def start_large_circle_rotation(self, large_circle):
        """Start rotation animation for a large circle and all circles within it."""
        if self.is_any_circle_animating():
            return False

        # Get all affected circles
        medium_circles = large_circle.medium_circles
        all_small_circles = []

        # Collect all small circles inside the affected medium circles
        for medium_circle in medium_circles:
            circles_inside = get_circles_inside_at_position(
                medium_circle.pos, CIRCLE_MEDIUM_RADIUS, self.system.small_circles
            )
            all_small_circles.extend(circles_inside)

        # Start the rotation sound sequence
        self._start_rotation_sound_sequence()

        # Start the large circle rotation with all affected circles
        self.large_circle_controller.start_rotation(large_circle, medium_circles, all_small_circles)
        return True

    def start_medium_circle_rotation(self, medium_circle, circles_inside):
        """Start rotation for a specific medium circle with dynamically calculated circles."""
        # Start the rotation sound sequence
        self._start_rotation_sound_sequence()

        self.circle_controller.start_rotation(medium_circle, circles_inside)
        self.pending_post_rotation = self.circle_controller.pending_post_rotation

    def start_center_rotation(self) -> None:
        """Start center rotation animation."""
        self.center_controller.start_rotation()
        # Update backward compatibility attributes
        self.is_center_rotating = self.center_controller.is_rotating
        self.center_rotation_start = self.center_controller.rotation_start
        self.center_initial_angles = self.center_controller.initial_angles

    def update(self):
        """Update all animations and handle post-animation effects."""
        current_time = time.time()
        was_animating = self.is_any_circle_animating()

        # Update sound effects
        if was_animating:
            self._update_rotation_sounds(current_time)

        self.center_controller.update(current_time)
        self.circle_controller.update(current_time)
        self.large_circle_controller.update(current_time)

        # Check if animation just finished
        if was_animating and not self.is_any_circle_animating():
            self._stop_rotation_sounds()
            self._handle_post_animation_effects()

    def _handle_post_animation_effects(self):
        """Handle effects that occur after animations complete."""
        # Update game state first
        self.system.game_state.phase = PHASE_PLACEMENT
        self.system.game_state.turn = "blue" if self.system.game_state.turn == "red" else "red"

        # Then update connections and colors
        self.system.update_adjacent_connections()
        self.system.color_manager.update_all_colors(
            self.system.medium_circles,
            self.system.large_circles,
            self.system.circle_manager.get_circles_inside,
            self.system.connection_manager,
            after_rotation=True,  # This ensures neighbor rules are applied post-animation
        )

        self.system.circle_manager.find_and_neutralize_islands(self.system.connection_manager)

    def is_any_circle_animating(self) -> bool:
        """Check if any animation is currently in progress."""
        return (
            self.center_controller.is_rotating
            or any(circle.is_animating for circle in self.system.medium_circles)
            or any(sc.is_animating for sc in self.system.circle_manager.large_circles)
            or self.large_circle_controller.is_rotating
        )

    def set_rotation_duration(self, duration: float) -> None:
        """Update the rotation duration for all controllers."""
        self.rotation_duration = duration
