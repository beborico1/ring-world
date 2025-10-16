import json
import os
from datetime import datetime
import glob


class SaveLoadManager:
    """Manages saving and loading game states with timestamped backups and history navigation"""

    def __init__(self, game_system):
        self.game_system = game_system
        self.save_directory = "saves"
        self.save_file = "game_state.json"
        self.backup_pattern = "game_state_{}.json"
        self.max_backups = 10
        self.current_history_index = -1  # -1 means we're at the latest state
        self._ensure_save_directory(clear_existing=True)  # New parameter to clear directory

    def _ensure_save_directory(self, clear_existing=False):
        """Create saves directory if it doesn't exist and optionally clear it"""
        # Create directory if it doesn't exist
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
        # Clear directory if requested
        elif clear_existing:
            for file in os.listdir(self.save_directory):
                if file.endswith(".json"):
                    os.remove(os.path.join(self.save_directory, file))

    def _get_sorted_backup_files(self):
        """Get list of backup files sorted by timestamp"""
        backup_files = glob.glob(os.path.join(self.save_directory, "game_state_*.json"))
        backup_files.sort(key=os.path.getmtime)  # Sort by modification time
        return backup_files

    def _cleanup_old_backups(self):
        """Keep only the most recent max_backups backup files"""
        backup_files = self._get_sorted_backup_files()

        # Remove oldest files if we have more than max_backups
        while len(backup_files) > self.max_backups:
            os.remove(backup_files[0])
            backup_files.pop(0)

    def load_previous_state(self):
        """Load the previous game state if available"""
        # If we're at the latest state, save current state before going back
        if self.current_history_index == -1:
            self.save_game()
            # Get fresh list of backups after saving
            backup_files = self._get_sorted_backup_files()

            if len(backup_files) >= 2:
                # Skip the most recent save (which we just made) and go to the one before
                self.current_history_index = len(backup_files) - 2
                return self._load_from_file(backup_files[self.current_history_index])
            else:
                print("No previous states available")
                return False
        else:
            backup_files = self._get_sorted_backup_files()
            if not backup_files:
                print("No previous states available")
                return False

            # Move to previous state if available
            self.current_history_index = max(0, self.current_history_index - 1)
            return self._load_from_file(backup_files[self.current_history_index])

    def load_next_state(self):
        """Load the next game state if available"""
        backup_files = self._get_sorted_backup_files()

        if not backup_files or self.current_history_index == -1:
            print("Already at latest state")
            return False

        # Move to next state if available
        if self.current_history_index < len(backup_files) - 1:
            self.current_history_index += 1
            return self._load_from_file(backup_files[self.current_history_index])
        else:
            # If we're at the last backup, load the current game state
            self.current_history_index = -1
            return self.load_game()

    def _load_from_file(self, filepath):
        """Load game state from specified file"""
        try:
            with open(filepath, "r") as f:
                state = json.load(f)

            # Reset current game state
            self.game_system.reset_game()

            # Restore small circles
            for saved_circle in state["small_circles"]:
                for circle in self.game_system.small_circles:
                    if circle.id == saved_circle["id"]:
                        circle.pos = saved_circle["pos"]
                        circle.set_color(saved_circle["color"])

            # Restore medium circles
            for i, saved_circle in enumerate(state["medium_circles"]):
                circle = self.game_system.medium_circles[i]
                circle.pos = saved_circle["pos"]
                circle.color = saved_circle["color"]

            # Restore game state
            self.game_system.game_state.turn = state["turn"]
            self.game_system.game_state.phase = state["phase"]

            # Update connections
            self.game_system.update_adjacent_connections()

            return True

        except Exception as e:
            print(f"Error loading game state: {e}")
            return False

    def save_game(self):
        """Save current game state and create timestamped backup"""
        state = self.serialize_game_state()

        # Save current state to main save file
        main_filepath = os.path.join(self.save_directory, self.save_file)
        with open(main_filepath, "w") as f:
            json.dump(state, f, indent=2)

        # Create timestamped backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = self.backup_pattern.format(timestamp)
        backup_filepath = os.path.join(self.save_directory, backup_filename)

        with open(backup_filepath, "w") as f:
            json.dump(state, f, indent=2)

        # Reset history index since we're adding a new state
        self.current_history_index = -1

        # Clean up old backups
        self._cleanup_old_backups()

    def load_game(self):
        """Load the current saved game state"""
        filepath = os.path.join(self.save_directory, self.save_file)
        return self._load_from_file(filepath)

    def serialize_game_state(self):
        """Convert current game state to serializable format"""
        small_circles = []
        for circle in sorted(self.game_system.small_circles, key=lambda c: c.id):
            small_circles.append(
                {
                    "id": circle.id,
                    "pos": [float(circle.pos[0]), float(circle.pos[1])],
                    "color": circle.color,
                }
            )

        medium_circles = []
        for i, circle in enumerate(self.game_system.medium_circles):
            medium_circles.append(
                {
                    "id": i,
                    "pos": [float(circle.pos[0]), float(circle.pos[1])],
                    "color": circle.color,
                }
            )

        return {
            "turn": self.game_system.game_state.turn,
            "phase": self.game_system.game_state.phase,
            "small_circles": small_circles,
            "medium_circles": medium_circles,
        }
