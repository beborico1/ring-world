from ..utils.settings import RED, BLUE


class MoveEvaluator:
    """Evaluates potential moves and positions"""

    def __init__(self, circle_system, color):
        self.system = circle_system
        self.color = color

    def evaluate_position(self):
        """Evaluate the current position based on circle count difference"""
        blue_count = sum(1 for circle in self.system.small_circles if circle.color == BLUE)
        red_count = sum(1 for circle in self.system.small_circles if circle.color == RED)
        if self.color == RED:
            return red_count - blue_count
        return blue_count - red_count
