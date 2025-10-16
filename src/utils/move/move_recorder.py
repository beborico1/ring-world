class MoveRecorder:
    def __init__(self):
        self.current_move = None
        self.new_move = False

    def record_placement_move(self, position, player_color):
        self.current_move = {
            "type": "move",
            "position": self._format_position(position),
            "color": player_color,
            "phase": "placement",
        }
        self.new_move = True

    def record_rotation_move(self, position, player_color, rotation_type):
        self.current_move = {
            "type": "move",
            "position": self._format_position(position),
            "color": player_color,
            "phase": "rotation",
            "rotation_type": rotation_type,
        }
        self.new_move = True

    def has_new_move(self):
        return self.new_move

    def get_move_data(self):
        if self.current_move:
            move_data = self.current_move
            self.new_move = False
            return move_data
        return None

    def _format_position(self, pos):
        return [round(float(pos[0]), 2), round(float(pos[1]), 2)]
