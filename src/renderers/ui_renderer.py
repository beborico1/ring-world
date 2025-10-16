import pygame
from ..utils.settings import WIDTH, HEIGHT, WHITE, BLUE, RED


class UIRenderer:
    """Renders UI elements for the game interface."""

    def __init__(self, font):
        """
        Initialize the UI renderer.

        Args:
            font: pygame.font.Font object for rendering text
        """
        self.font = font
        self.ff_font = pygame.font.Font(None, 48)  # Larger font for fast forward button

        # Button dimensions and properties
        self.button_width = 200
        self.button_height = 50
        self.button_padding = 20

        # Button states and styles
        self.button_states = {
            "normal": {"color": WHITE, "text_color": (0, 0, 0), "symbol": "N"},
            "pause": {"color": RED, "text_color": WHITE, "symbol": "P"},
            "fast_forward": {"color": BLUE, "text_color": WHITE, "symbol": "FF"},
        }

    def draw_turn_and_phase(self, surface, game_state):
        """Draw the current turn and phase indicators."""
        # Draw turn indicator
        turn_text = f"Turn: {'Red' if game_state.turn == 'red' else 'Blue'}"
        self._draw_text(surface, turn_text, (10, 10))

        # Draw phase indicator
        phase_text = f"Phase: {'Placement' if game_state.phase == 'placement' else 'Rotation'}"
        self._draw_text(surface, phase_text, (10, 50))

        # Draw AI thinking indicator if applicable
        if hasattr(game_state, "ai_thinking") and game_state.ai_thinking:
            self._draw_text(surface, "Thinking...", (10, HEIGHT - 50))

    def draw_scores(self, surface, small_circles):
        """Draw the score counters for both players."""
        # Count circles by color
        blue_count = sum(1 for circle in small_circles if circle.color == BLUE)
        red_count = sum(1 for circle in small_circles if circle.color == RED)

        # Draw scores with appropriate colors
        self._draw_text(surface, f"Blue: {blue_count}", (10, 130), BLUE)
        self._draw_text(surface, f"Red: {red_count}", (10, 170), RED)

    def draw_winner_screen(self, surface, winner):
        """
        Draw the winner announcement overlay with colored background and buttons.

        Args:
            surface: pygame surface to draw on
            winner: string indicating the winning color ("red" or "blue")
        """
        # Create semi-transparent colored overlay based on winner
        overlay = pygame.Surface((WIDTH, HEIGHT))
        winner_color = RED if winner == "red" else BLUE
        overlay.fill(winner_color)
        overlay.set_alpha(64)  # Adjust transparency
        surface.blit(overlay, (0, 0))

        # Create winner text
        winner_text = f"{winner.capitalize()} Wins!"
        winner_surface = self.font.render(winner_text, True, (255, 255, 255))
        text_rect = winner_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        surface.blit(winner_surface, text_rect)

        # Draw buttons
        replay_rect = self._create_button(surface, "Play Again", HEIGHT // 2 + 30)
        menu_rect = self._create_button(surface, "Main Menu", HEIGHT // 2 + 100)

        return replay_rect, menu_rect

    def draw_training_stats(self, surface, training_stats):
        """
        Draw training statistics on the screen.

        Args:
            surface: pygame surface to draw on
            training_stats: dictionary containing training statistics
        """
        if not training_stats:
            return

        # Draw speed state button using the actual state
        # speed_state = training_stats.get("speed_state", "normal")
        # self.draw_fast_forward_button(surface, speed_state)

        # Draw games played counter
        # games_played = training_stats.get("games_played", 0)
        # stats_text = f"Games Played: {games_played}"
        # self._draw_text(surface, stats_text, (10, 90))

    def _create_button(self, surface, text, y_pos):
        """Helper method to create and draw a button."""
        button_rect = pygame.Rect(
            (WIDTH - self.button_width) // 2, y_pos, self.button_width, self.button_height
        )

        # Draw button background
        pygame.draw.rect(surface, WHITE, button_rect)
        pygame.draw.rect(surface, (100, 100, 100), button_rect, 2)  # Border

        # Draw button text
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)

        return button_rect

    def draw_fast_forward_button(self, surface, state):
        """Draw the speed control button with current state."""
        # Define button dimensions
        button_rect = pygame.Rect(WIDTH - 60, 10, 50, 50)

        # Get current state settings or default to normal
        current_state = state if isinstance(state, str) else "normal"
        settings = self.button_states[current_state]

        # Draw the button
        self._draw_button(surface, button_rect, settings)

    def _draw_text(self, surface, text, position, color=(255, 255, 255)):
        """Helper method to draw text on the surface."""
        text_surface = self.font.render(text, True, color)
        surface.blit(text_surface, position)

    def _draw_button(self, surface, button_rect, settings):
        """Helper method to draw a button with specified settings."""
        # Draw button background
        pygame.draw.rect(surface, settings["color"], button_rect)

        # Draw button border
        pygame.draw.rect(surface, (0, 0, 0), button_rect, 2)

        # Draw button symbol
        ff_text = self.ff_font.render(settings["symbol"], True, settings["text_color"])
        ff_rect = ff_text.get_rect(center=button_rect.center)
        surface.blit(ff_text, ff_rect)

    def get_button_rect(self):
        """Get the rectangle defining the fast forward button's position and size."""
        return pygame.Rect(WIDTH - 60, 10, 50, 50)
