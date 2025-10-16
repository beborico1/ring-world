from ..settings import (
    RED,
    BLUE,
    GREY,
    PHASE_PLACEMENT,
    CIRCLE_MEDIUM_RADIUS,
    CIRCLE_LARGE_RADIUS,
)
from ..geometry import get_circles_inside_at_position, get_completely_contained_circles


class MoveValidator:
    def __init__(self, circle_system):
        self.system = circle_system

    def get_valid_moves(self):
        """Returns the valid moves for the current phase and turn."""

        if self.system.is_any_circle_animating():
            return []

        current_color = RED if self.system.game_state.turn == "red" else BLUE

        if self.system.game_state.phase == PHASE_PLACEMENT:
            valid_moves = self._get_valid_placement_moves(current_color)
            return valid_moves
        else:
            valid_moves = self._get_valid_rotation_moves(current_color)
            return valid_moves

    def _get_valid_placement_moves(self, current_color):
        invalid_circles = []
        for medium_circle in self.system.medium_circles:
            circles_inside = get_circles_inside_at_position(
                medium_circle.pos, CIRCLE_MEDIUM_RADIUS, self.system.small_circles
            )
            if any(circle.color == current_color for circle in circles_inside):
                invalid_circles.extend(circles_inside)

        valid_moves = [
            circle
            for circle in self.system.small_circles
            if circle not in invalid_circles and circle.color == GREY
        ]

        if not valid_moves:
            self.system.game_state.phase = "rotation"
            print("No valid moves found. Changing phase to rotation for color ", current_color)

        return valid_moves

    def _get_valid_rotation_moves(self, current_color):
        valid_moves = []

        # Check medium circles
        for medium_circle in self.system.medium_circles:
            if self._is_valid_medium_circle_rotation(medium_circle, current_color):
                valid_moves.append(medium_circle)

        # Check large circles
        for large_circle in self.system.circle_manager.large_circles:
            if self._is_valid_large_circle_rotation(large_circle, current_color):
                valid_moves.append(large_circle)

        return valid_moves

    def _is_valid_medium_circle_rotation(self, medium_circle, current_color):
        circles_inside = get_circles_inside_at_position(
            medium_circle.pos, CIRCLE_MEDIUM_RADIUS, self.system.small_circles
        )
        return any(circle.color == current_color for circle in circles_inside)

    def _is_valid_large_circle_rotation(self, large_circle, current_color):
        medium_circles_inside = get_completely_contained_circles(
            large_circle.pos, CIRCLE_LARGE_RADIUS, self.system.medium_circles, CIRCLE_MEDIUM_RADIUS
        )

        return any(circle.color == current_color for circle in medium_circles_inside)
