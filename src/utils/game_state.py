from typing import Optional
from .settings import PHASE_PLACEMENT, PHASE_ROTATION, VALID_COLORS


class GameState:
    def __init__(self):
        # Game logic state
        self.turn = VALID_COLORS[0]  # "red" or "blue"
        self.phase = PHASE_PLACEMENT  # "placement" or "rotation"
        self.winner = None
        self.ai_thinking = False

        # Network state
        self.room_code: Optional[str] = None
        self.player_color: Optional[str] = None
        self.match_found: bool = False
        self.shutting_down: bool = False
        self.last_received_sequence: int = 0
        self.send_sequence: int = 0

    def switch_turn(self) -> None:
        """Switch the current turn between players."""
        self.turn = VALID_COLORS[1] if self.turn == VALID_COLORS[0] else VALID_COLORS[0]
        self.phase = PHASE_PLACEMENT  # Reset phase when switching turns

    def switch_phase(self) -> None:
        """Switch the current game phase."""
        self.phase = PHASE_ROTATION if self.phase == PHASE_PLACEMENT else PHASE_PLACEMENT
        if self.phase == PHASE_PLACEMENT:  # If we're back to placement, switch turns
            self.switch_turn()

    # Network-related methods
    def join_room(self, room_code: str) -> None:
        """Update state when joining a room."""
        self.room_code = room_code
        self.match_found = False

    def check_match_status(self) -> Optional[str]:
        """Check if a match has been found and return the player's color."""
        if self.match_found:
            return self.player_color
        return None

    def update_match_status(self, match_found: bool, player_color: Optional[str]) -> None:
        """Update match status and player color."""
        self.match_found = match_found
        if player_color:
            self.player_color = player_color

    @property
    def is_online(self) -> bool:
        """Check if the game is in online mode."""
        return self.room_code is not None and self.match_found

    def set_ai_thinking(self, thinking: bool) -> None:
        """Set the AI thinking state."""
        self.ai_thinking = thinking

    def reset(self):
        """Reset game state to initial values."""
        self.turn = "red"  # Always start with red
        self.phase = "placement"
        self.winner = None
        self.ai_thinking = False  # Reset thinking state
