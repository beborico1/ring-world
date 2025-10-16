import pygame
from enum import Enum
from typing import Dict, Any, Optional


# Window configuration
WIDTH = 600
HEIGHT = 600
FONT_SIZE = 32
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Circle System")

DRAW_CONNECTIONS = False
DRAW_TURN_AND_PHASE = False
DRAW_SAVE_LOAD_UI = False
DRAW_SCORES = False

# Colors
WHITE = (255, 255, 255)
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREY = [128, 128, 128]
LIGHT_GREY = (200, 200, 200)
GREEN = (0, 255, 0, 128)  # Semi-transparent green for valid move indicators

# Circle properties
CIRCLE_SMALL_RADIUS = 5
CIRCLE_MEDIUM_RADIUS = 30
CIRCLE_LARGE_RADIUS = 90

CENTER_CLICK_RADIUS = 40  # Was 100

# Game phases
PHASE_PLACEMENT = "placement"
PHASE_ROTATION = "rotation"


# Game constants
MOVE_PHASES = [PHASE_PLACEMENT, PHASE_ROTATION]
VALID_COLORS = ["red", "blue"]


AI_THINKING_TIME = 2000  # 2000  # AI thinking time in milliseconds
AI_MAX_THINK_TIME = 2.0  # Maximum AI thinking time in seconds
RESET_GAME_DELAY = 2000  # Delay before resetting the game in milliseconds

SHOW_IDS = False  # Show circle IDs for debugging


class GameMode(Enum):
    MENU = "menu"
    OFFLINE = "offline"
    ONLINE = "online"
    WAITING = "waiting"
    AI = "ai"
    TRAINING = "training"  # New mode for AI vs AI


DEFAULT_ROTATION_DURATION = 1.0

# Mode-specific rotation durations
ROTATION_DURATIONS = {
    GameMode.OFFLINE: 1.0,
    GameMode.ONLINE: 1.0,
    GameMode.AI: 1.0,
    GameMode.TRAINING: 1.0,
}

# Message types
MESSAGE_TYPES = {
    "JOIN": "join",
    "WAIT": "wait",
    "START": "start",
    "MOVE": "move",
    "OPPONENT_DISCONNECTED": "opponent_disconnected",
}

# Network configuration
NETWORK_CONFIG: Dict[str, Any] = {
    "URL": "wss://ring-world-production.up.railway.app",
    "RECONNECT_DELAY": 5,
    "MAX_RECONNECT_ATTEMPTS": 5,
    "HEARTBEAT_INTERVAL": 30,
}


class TrainingConfig:
    # Neural network architecture
    INPUT_SIZE = 48 + 8
    # HIDDEN_LAYERS = [112, 224, 112]  # Double input size then back
    HIDDEN_LAYERS = [224, 448, 224]  # Double input size then back
    OUTPUT_SIZE = 48 + 8

    # Training hyperparameters
    LEARNING_RATE = 0.003
    GAMMA = 0.95

    # Game settings
    DEFAULT_THINKING_TIME = 1000

    @classmethod
    def get_network_architecture(cls):
        return [cls.INPUT_SIZE] + cls.HIDDEN_LAYERS + [cls.OUTPUT_SIZE]


RED_TEMPERATURE = 1.0
RED_TEMPERATURE_DECAY = 1.0  # 0.995

BLUE_TEMPERATURE = 1.0
BLUE_TEMPERATURE_DECAY = 0.995

TEMPERATURE_MIN = 0.01


class DebugSettings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DebugSettings, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.showing_connections = False
            self._connection_distance_multiplier = 3.2
            self.min_multiplier = 2.0
            self.max_multiplier = 6.0
            self._initialized = True

    @property
    def connection_distance_multiplier(self):
        # print(f"Getting multiplier from DebugSettings: {self._connection_distance_multiplier}")
        return float(self._connection_distance_multiplier)

    @connection_distance_multiplier.setter
    def connection_distance_multiplier(self, value):
        value = float(value)
        self._connection_distance_multiplier = max(
            self.min_multiplier, min(self.max_multiplier, value)
        )


class AIThinkingState:
    """Manages AI thinking state and timing"""

    def __init__(self):
        self.thinking_start_time: Optional[int] = None
        self.is_thinking: bool = False
        self.next_move: Optional[tuple] = None
        self.phase: str = "placement"  # placement or rotation
