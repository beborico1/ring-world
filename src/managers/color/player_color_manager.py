from ...utils.settings import RED, BLUE


class PlayerColorManager:
    def __init__(self):
        self.turn = "red"
        self.player_color = None

    def set_player_color(self, color: str):
        """Set the player's assigned color from the server."""
        if color == "red":
            self.player_color = RED
        elif color == "blue":
            self.player_color = BLUE
        elif color is None:  # For offline mode
            self.player_color = None
