# game.py
import pygame
from .controllers.game_controller import GameController
from .utils.settings import GameMode, ROTATION_DURATIONS, RED, DEFAULT_ROTATION_DURATION
from .systems.circle_system import CircleSystem
from .ai.strategic_ai_player import StrategicAIPlayer  # AIPlayer
from .managers.save_load_manager import SaveLoadManager


class Game:
    """
    Main game class that coordinates all game systems and manages the game lifecycle.
    Delegates specific functionality to specialized managers through GameController.
    """

    def __init__(self):
        """Initialize the game and all its controllers and managers."""
        pygame.init()  # Ensure pygame is initialized
        pygame.mixer.init()

        self.controller = GameController()  # GameController now handles screen initialization

        # Verify initialization
        if not self.controller.managers["render"].screen:
            raise RuntimeError("Screen not properly initialized in RenderManager")

    def _handle_events(self):
        """Process all game events and return whether the game should continue."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Handle debug events first if in gameplay modes
            if self.controller.game_mode not in [GameMode.MENU, GameMode.WAITING]:
                if self.controller.managers["render"].handle_debug_events(event):
                    # If the debug event caused a connection update, refresh connections
                    if self.controller.systems["circle"]:
                        self.controller.systems["circle"].update_adjacent_connections()
                    continue

            self._process_game_event(event)
        return True

    def _process_game_event(self, event):
        """Process a single game event based on current game mode."""
        if self.controller.game_mode in [GameMode.MENU, GameMode.WAITING]:
            result = self.controller.systems["menu"].handle_events(event)
            if result is not None:
                if len(result) == 2:
                    new_mode, color = result
                    reduced_version = False
                else:
                    new_mode, color, reduced_version = result

                if new_mode:
                    self.set_game_mode(new_mode, reduced_version)
                    self.controller.player_color = color

        elif self.controller.game_mode == GameMode.TRAINING:
            if self.controller.systems["circle"] and self.controller.event_handler:
                self.controller.event_handler.handle_events(event)

        elif self.controller.game_mode in [GameMode.OFFLINE, GameMode.ONLINE, GameMode.AI]:
            self._handle_gameplay_event(event)

    def _handle_gameplay_event(self, event):
        """Handle events during active gameplay."""
        if not self.controller.systems["circle"]:
            return

        can_move = (
            self.controller.game_mode == GameMode.OFFLINE
            or (
                self.controller.game_mode == GameMode.ONLINE
                and self.controller.player_color
                == self.controller.systems["circle"].game_state.turn
            )
            or (
                self.controller.game_mode == GameMode.AI
                and self.controller.systems["circle"].game_state.turn == "red"
            )
        )

        if can_move:
            self.controller.systems["circle"].handle_events(event)

    def _update(self):
        """Update game state based on current mode."""
        if self.controller.game_mode in [GameMode.ONLINE, GameMode.WAITING]:
            self._handle_network_update()
        elif self.controller.game_mode == GameMode.AI and self.controller.ai_player:
            self.controller.ai_player.make_move()
        elif self.controller.game_mode == GameMode.TRAINING:
            # Update AI players in training mode
            self.controller.update_ai_players()

        # Update circle system if it exists
        if self.controller.systems["circle"]:
            self.controller.systems["circle"].update()

            if self.controller.game_mode == GameMode.ONLINE:
                self.controller.managers["network"].handle_online_moves(
                    self.controller.systems["circle"]
                )

    def _handle_network_update(self):
        """Handle network-related updates."""
        new_mode, new_color = self.controller.managers["network"].handle_network_messages(
            self.controller.game_mode,
            self.controller.systems["circle"],
            self.controller.player_color,
        )

        if new_mode:
            self.controller.game_mode = new_mode
            self.controller.player_color = new_color

    def set_game_mode(self, new_mode, reduced_version=False):
        """Set up the game for a new mode."""
        self.controller.game_mode = new_mode

        if hasattr(self.controller, "event_handler"):
            self.controller.event_handler.game_mode = new_mode

        rotation_duration = ROTATION_DURATIONS.get(new_mode, DEFAULT_ROTATION_DURATION)

        if new_mode in [GameMode.OFFLINE, GameMode.ONLINE, GameMode.AI, GameMode.TRAINING]:
            self._initialize_circle_system(new_mode, rotation_duration, reduced_version)

    def _initialize_circle_system(self, mode, rotation_duration, reduced_version=False):
        print("Initializing circle system", reduced_version)
        """Initialize the circle system for the given game mode."""
        self.controller.systems["circle"] = CircleSystem(
            original_ui=self.controller.original_ui,
            board_renderer=self.controller.managers["render"].game_renderer.board_renderer,
            rotation_duration=rotation_duration,
            event_handler=self.controller.event_handler,
            screen=self.controller.managers["render"].screen,
            reduced_version=reduced_version,
        )
        self.controller.event_handler.system = self.controller.systems["circle"]

        if mode == GameMode.OFFLINE:
            self.controller.systems["circle"].color_manager.set_player_color(None)
        elif mode == GameMode.AI:
            self.controller.systems["circle"].color_manager.set_player_color(RED)
            self.controller.ai_player = StrategicAIPlayer(self.controller.systems["circle"])
            save_manager = SaveLoadManager(self.controller.systems["circle"])
            self.controller.ai_player.initialize_save_manager(save_manager)
        elif mode == GameMode.TRAINING:
            self.controller.systems["circle"].color_manager.set_player_color(None)
            self.controller.initialize_ai_players(self.controller.systems["circle"])
        elif mode == GameMode.ONLINE and self.controller.player_color:
            self.controller.systems["circle"].color_manager.set_player_color(
                self.controller.player_color
            )

    def run(self):
        """Main game loop."""
        running = True
        while running:
            self.controller.current_time = pygame.time.get_ticks()

            if not self._handle_events():
                running = False
                continue

            self._update()

            # Update training stats before rendering
            self.controller.update_training_stats()

            # Render frame
            self.controller.managers["render"].render_frame(
                self.controller.game_mode,
                self.controller.systems,
            )

            self.controller.clock.tick(60)

        # Cleanup
        if self.controller.game_mode == GameMode.ONLINE:
            self.controller.managers["network"].network_manager.shutdown()
        pygame.quit()
