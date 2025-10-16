from ..settings import (
    RED,
    BLUE,
    PHASE_ROTATION,
    CIRCLE_MEDIUM_RADIUS,
    CIRCLE_LARGE_RADIUS,
)
from ..geometry import get_circles_inside_at_position, get_completely_contained_circles
import pygame


class MoveExecutor:
    def __init__(self, circle_system):
        self.system = circle_system
        self.placement_sound = pygame.mixer.Sound("assets/sounds/l1.wav")

    def make_placement_move(self, circle, player_color):
        """Make a placement move if valid."""
        if self.system.is_any_circle_animating():
            return False

        current_color = RED if player_color == "red" else BLUE
        circle.set_color(current_color)

        # Play placement sound
        self.placement_sound.play()

        self.system.color_manager.update_all_colors(
            self.system.medium_circles,
            self.system.large_circles,
            self.system.circle_manager.get_circles_inside,
            self.system.connection_manager,
            after_rotation=False,
        )

        # Change phase to rotation after placement
        self.system.game_state.phase = PHASE_ROTATION
        return True

    def make_rotation_move(self, circle, player_color, contained_circles_only=False):
        """Make a rotation move for either a medium circle or large circle."""
        if self.system.is_any_circle_animating():
            return False

        current_color = RED if player_color == "red" else BLUE

        if isinstance(circle, type(self.system.medium_circles[0])):
            return self._execute_medium_circle_rotation(circle, current_color)
        else:
            return self._execute_super_circle_rotation(
                circle, current_color, contained_circles_only
            )

    def _execute_medium_circle_rotation(self, medium_circle, current_color):
        circles_inside = get_circles_inside_at_position(
            medium_circle.pos, CIRCLE_MEDIUM_RADIUS, self.system.small_circles
        )

        if any(circle.color == current_color for circle in circles_inside):
            self.system.animation_handler.start_medium_circle_rotation(
                medium_circle, circles_inside
            )
            return True
        return False

    def _execute_super_circle_rotation(self, super_circle, current_color, contained_circles_only):
        print(f"Executing large rotation in {super_circle.id}")

        if contained_circles_only:
            medium_circles_inside = get_completely_contained_circles(
                super_circle.pos,
                CIRCLE_LARGE_RADIUS,
                self.system.medium_circles,
                CIRCLE_MEDIUM_RADIUS,
            )
        else:
            medium_circles_inside = get_circles_inside_at_position(
                super_circle.pos, CIRCLE_LARGE_RADIUS, self.system.medium_circles
            )

        if self._validate_super_circle_rotation(
            super_circle.pos, medium_circles_inside, current_color
        ):
            super_circle.medium_circles = medium_circles_inside
            self.system.animation_handler.start_large_circle_rotation(super_circle)
            return True
        return False

    def _validate_super_circle_rotation(self, center, medium_circles, current_color):
        for medium_circle in medium_circles:
            circles_inside = get_circles_inside_at_position(
                medium_circle.pos, CIRCLE_MEDIUM_RADIUS, self.system.small_circles
            )
            if any(circle.color == current_color for circle in circles_inside):
                return True
        return False
