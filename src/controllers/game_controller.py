import pygame
from ..systems.menu_system import MenuSystem
from ..utils.settings import HEIGHT, WIDTH, GameMode, RED, BLUE
from ..handlers.event_handler import EventHandler
from ..managers.network.network_manager import GameNetworkManager
from ..managers.render_manager import RenderManager
from ..ai.strategic_ai_player import StrategicAIPlayer
from ..renderers.original_ui_renderer import GameUI


class GameController:
    def __init__(self):
        # Load the icon image
        icon = pygame.image.load("assets/icon.png")

        # Optional: scale the icon if needed
        icon = pygame.transform.scale(icon, (32, 32))  # Common icon size

        # Set the window icon
        pygame.display.set_icon(icon)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("The Ring World")

        self.menu_system = MenuSystem()
        self.game_mode = GameMode.MENU
        self.current_time = 0
        self.player_color = None
        self.original_ui = GameUI(self)

        self.systems = {"circle": None, "menu": self.menu_system}

        # Initialize managers with screen
        self.managers = {
            "network": GameNetworkManager(),
            "render": RenderManager(self.screen, self.original_ui),
        }

        # AI players for training mode
        self.red_ai = None
        self.blue_ai = None

        self.event_handler = EventHandler(self.systems["circle"], self, self.original_ui)
        self.clock = pygame.time.Clock()

    def update_ai_players(self):
        """Update AI players in training mode"""
        if self.game_mode == GameMode.TRAINING and self.systems["circle"]:
            if self.systems["circle"].game_state.turn == "red":
                self.red_ai.make_move()
            else:
                self.blue_ai.make_move()

    def update_training_stats(self):
        """Update training stats in render manager"""
        if self.game_mode == GameMode.TRAINING and self.systems["circle"]:
            stats = {
                "speed_state": "normal",  # Default state, could be modified if needed
                "games_played": 0,  # Could keep track if needed
            }
            self.managers["render"].update_training_stats(stats)

    def initialize_ai_players(self, circle_system):
        """Initialize both AI players for training mode"""
        from ..managers.save_load_manager import SaveLoadManager

        save_manager = SaveLoadManager(circle_system)

        # Initialize Red AI
        self.red_ai = StrategicAIPlayer(circle_system, color=RED)
        self.red_ai.initialize_save_manager(save_manager)

        # Initialize Blue AI
        self.blue_ai = StrategicAIPlayer(circle_system, color=BLUE)
        self.blue_ai.initialize_save_manager(save_manager)
