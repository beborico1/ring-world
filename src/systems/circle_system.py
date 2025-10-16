from pygame import font
from ..utils.settings import FONT_SIZE, RESET_GAME_DELAY, DEFAULT_ROTATION_DURATION
from ..managers.circles.circle_manager import CircleManager
from ..managers.color.color_manager import GameColorManager
from ..managers.connection_manager import ConnectionManager
from ..managers.render_manager import RenderManager
from ..managers.save_load_manager import SaveLoadManager
from ..utils.game_state import GameState
from ..handlers.event_handler import EventHandler
from ..handlers.move_handler import MoveHandler
from ..handlers.animation_handler import AnimationHandler
from ..handlers.turn_handler import TurnHandler
import pygame


class CircleSystem:
    def __init__(
        self,
        original_ui,
        board_renderer,
        rotation_duration: float = 1.0,
        event_handler: EventHandler = None,
        screen=None,
        reduced_version=False,
    ):
        print("Initializing circle system", reduced_version)
        # Initialize managers
        self.circle_manager = CircleManager(reduced_version)
        self.connection_manager = ConnectionManager()
        self.color_manager = GameColorManager(self)
        self.render_manager = RenderManager(screen, original_ui)
        self.render_manager.set_circle_system(self)
        self.debug_settings = self.render_manager.debug_settings  # Share the same instance
        self.game_state = GameState()
        self.save_load_manager = SaveLoadManager(self)

        # Add board renderer instance
        self.board_renderer = board_renderer

        # Initialize handlers
        self.event_handler = event_handler
        self.move_handler = MoveHandler(self)
        self.animation_handler = AnimationHandler(self, rotation_duration)
        self.turn_handler = TurnHandler(self)

        # Initialize font
        font.init()
        self.font = pygame.font.Font(None, FONT_SIZE)

        # Initialize system
        self._initialize_system()

        self.reset_delay = RESET_GAME_DELAY
        self.winner_time = None
        self.last_update_time = 0
        self.connection_update_interval = 1000

    def reset_game(self):
        """Reset the game state and board."""
        self.circle_manager.reset_circles()
        self.game_state.reset()
        self.animation_handler.reset()
        self.winner_time = None
        # Reset the selected move in board renderer
        self.board_renderer.selected_move = None

        self.update_adjacent_connections()

    def _initialize_system(self):
        """Initialize the circle system components."""
        self.circle_manager._initialize_system()  # This will initialize large circles, medium circles, and small circles
        self.connection_manager.initialize_connections(self.circle_manager.small_circles)
        self.update_adjacent_connections()

    # Property getters
    @property
    def center(self):
        return list(self.circle_manager.center)

    @property
    def large_circles(self):
        return self.circle_manager.large_circles

    @property
    def medium_circles(self):
        return self.circle_manager.medium_circles

    @property
    def small_circles(self):
        return self.circle_manager.small_circles

    @property
    def adjacent_connections(self):
        return self.connection_manager.adjacent_connections

    @property
    def turn(self):
        return self.color_manager.turn

    @property
    def is_center_rotating(self):
        return self.animation_handler.is_center_rotating

    @property
    def center_rotation_start(self):
        return self.animation_handler.center_rotation_start

    @property
    def center_initial_angles(self):
        return self.animation_handler.center_initial_angles

    def update_adjacent_connections(self):
        """Update the connections between adjacent circles."""
        if self.debug_settings:
            multiplier = self.debug_settings.connection_distance_multiplier
            self.connection_manager.update_connection_distances(multiplier)
            self.connection_manager.update_adjacent_connections(self.small_circles)
        else:
            print("Warning: No debug settings available in CircleSystem")

    def is_any_circle_animating(self) -> bool:
        """Check if any circles are currently animating."""
        return self.animation_handler.is_any_circle_animating() or any(
            sc.is_animating for sc in self.circle_manager.large_circles
        )

    def draw(self, surface):
        """Draw the current state to the surface."""
        self.render_manager.draw(surface, self)

    def handle_events(self, event):
        """Handle incoming events."""
        # Check for save/load events first
        # if self.render_manager.save_load_ui.handle_events(event, self.save_load_manager):
        #     return True

        # If not handled by save/load UI, process normal events
        return self.event_handler.handle_events(event)

    def update(self):
        """Update the game state including animations and colors."""
        if hasattr(self, "ai_player") and self.ai_player:
            self.game_state.set_ai_thinking(self.ai_player.is_thinking())

        # Update animations
        self.animation_handler.update()

        # Update circle colors if not animating
        if not self.is_any_circle_animating():
            # Update colors for all circles
            self.circle_manager.update_medium_circle_colors()

            # Update connections periodically
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time >= self.connection_update_interval:
                self.update_adjacent_connections()
                self.last_update_time = current_time

    def get_winner(self):
        """Get the current winner if any and track the win time."""
        if self.game_state.winner:
            return self.game_state.winner

        winner = self.turn_handler.get_winner()
        if winner and self.winner_time is None:
            self.winner_time = pygame.time.get_ticks()
        return winner

    def should_reset(self, current_time):
        """Check if enough time has passed since win to reset."""
        if self.winner_time and current_time - self.winner_time >= self.reset_delay:
            return True
        return False

    def has_new_move(self):
        """Check if there's a new move available."""
        return self.move_handler.has_new_move()

    def get_move_data(self):
        """Get data for the current move."""
        return self.move_handler.get_move_data()

    def format_position(self, pos):
        """Format a position tuple to standardized format."""
        return self.move_handler.format_position(pos)
