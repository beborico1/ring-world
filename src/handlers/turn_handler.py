from ..utils.settings import RED, BLUE


class TurnHandler:
    def __init__(self, circle_system):
        self.circle_system = circle_system

    def get_winner(self):
        """Check if either player has won by controlling 5 large circles."""
        if not hasattr(self.circle_system, "circle_manager"):
            return None

        large_circles = self.circle_system.circle_manager.large_circles

        # Count large circles of each color
        red_large_circles = sum(1 for sc in large_circles if sc.color == RED)
        blue_large_circles = sum(1 for sc in large_circles if sc.color == BLUE)

        if red_large_circles >= 5:
            return "red"
        elif blue_large_circles >= 5:
            return "blue"

        return None
