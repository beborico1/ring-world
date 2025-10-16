from ..utils.settings import (
    RED,
    BLUE,
    GREY,
    PHASE_PLACEMENT,
    PHASE_ROTATION,
)
from ..utils.move.move_recorder import MoveRecorder
from ..utils.move.move_validator import MoveValidator
from ..utils.move.move_executor import MoveExecutor


class MoveHandler:
    def __init__(self, circle_system):
        self.system = circle_system
        self.validator = MoveValidator(circle_system)
        self.executor = MoveExecutor(circle_system)
        self.recorder = MoveRecorder()

    def get_valid_moves(self):
        return self.validator.get_valid_moves()

    def make_placement_move(self, circle, player_color):
        if self.executor.make_placement_move(circle, player_color):
            self.recorder.record_placement_move(circle.pos, player_color)
            return True
        return False

    def make_rotation_move(self, circle, player_color, contained_circles_only=False):
        if self.executor.make_rotation_move(circle, player_color, contained_circles_only):
            rotation_type = (
                "medium" if isinstance(circle, type(self.system.medium_circles[0])) else "super"
            )
            self.recorder.record_rotation_move(circle.pos, player_color, rotation_type)
            return True
        return False

    def has_new_move(self):
        return self.recorder.has_new_move()

    def get_move_data(self):
        return self.recorder.get_move_data()

    def _is_invalid_turn(self, opponent_color):
        player_color = "red" if self.system.color_manager.player_color == RED else "blue"
        return opponent_color == player_color

    def _apply_placement_move(self, position, color_rgb):
        for circle in self.system.small_circles:
            if self._is_matching_position(circle.pos, position) and circle.color == GREY:
                circle.set_color(color_rgb)
                self.system.color_manager.update_all_colors(
                    self.system.medium_circles,
                    self.system.large_circles,
                    self.system.circle_manager.get_circles_inside,
                    self.system.connection_manager,
                    after_rotation=False,
                )
                self.system.game_state.phase = PHASE_ROTATION
                break

    def _apply_rotation_move(self, position, opponent_color):
        if self.recorder.has_new_move():
            return

        for medium_circle in self.system.medium_circles:
            if self._is_matching_position(medium_circle.pos, position):
                circles_inside = self.system.circle_manager.get_circles_inside(medium_circle)
                self.system.animation_handler.start_medium_circle_rotation(
                    medium_circle, circles_inside
                )
                self._update_game_state(opponent_color)
                break

    def _is_matching_position(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) < 1 and abs(pos1[1] - pos2[1]) < 1

    def _update_game_state(self, opponent_color):
        self.system.game_state.phase = PHASE_PLACEMENT
        self.system.game_state.turn = "blue" if opponent_color == "red" else "red"
