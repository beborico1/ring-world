from .circle_renderer import CircleRenderer
from .ui_renderer import UIRenderer
from .game_board_renderer import GameBoardRenderer
from ..utils.settings import DRAW_CONNECTIONS, DRAW_TURN_AND_PHASE, DRAW_SCORES


class GameRenderer:
    def __init__(self, font, original_ui):
        self.original_ui = original_ui
        self.circle_renderer = CircleRenderer()
        self.ui_renderer = UIRenderer(font)
        self.board_renderer = GameBoardRenderer()
        self.background_color = (0, 0, 0)  # Black background

    def draw_training_stats(self, surface, training_stats):
        """
        Delegate drawing of training stats to UI renderer.

        Args:
            surface: pygame surface to draw on
            training_stats: dictionary containing training statistics
        """
        self.ui_renderer.draw_training_stats(surface, training_stats)

    def draw(self, surface, circle_system):
        """Main draw method that orchestrates all rendering."""
        surface.fill(self.background_color)

        self.original_ui.draw()

        # Draw board elements
        if DRAW_CONNECTIONS:
            circle_system.board_renderer.draw_connections(
                surface, circle_system.adjacent_connections, circle_system.is_any_circle_animating()
            )

        # Draw circles
        self.circle_renderer.draw_large_circles(surface, circle_system.circle_manager)
        self.circle_renderer.draw_medium_circles(surface, circle_system.medium_circles)
        self.circle_renderer.draw_small_circles(surface, circle_system.small_circles)

        # Draw game state elements
        valid_moves = circle_system.move_handler.get_valid_moves()
        if valid_moves:
            circle_system.board_renderer.draw_valid_moves(
                surface, valid_moves, circle_system.game_state.turn
            )

        if DRAW_TURN_AND_PHASE:
            self.ui_renderer.draw_turn_and_phase(surface, circle_system.game_state)
        if DRAW_SCORES:
            self.ui_renderer.draw_scores(surface, circle_system.small_circles)

        # Draw winner screen if game is over
        winner = circle_system.get_winner()
        if winner:
            button_rects = self.ui_renderer.draw_winner_screen(surface, winner)
            if hasattr(circle_system, "event_handler"):
                circle_system.event_handler.winner_buttons = button_rects
