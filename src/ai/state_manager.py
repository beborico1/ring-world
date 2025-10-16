class StateManager:
    """Manages game state operations"""

    def __init__(self, save_manager):
        self.save_manager = save_manager

    def save_state(self):
        """Save current game state"""
        self.save_manager.save_game()

    def load_state(self):
        """Load previous game state"""
        self.save_manager.load_game()
