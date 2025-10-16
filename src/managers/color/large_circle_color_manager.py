from ...utils.settings import RED, BLUE, GREY, CIRCLE_LARGE_RADIUS, CIRCLE_MEDIUM_RADIUS
from ...utils.geometry import get_completely_contained_circles, calculate_distance


class LargeCircleColorManager:
    """Manages color updates for large circles based on their medium circle children."""

    def __init__(self, circle_system):
        """Initialize with circle system reference."""
        self.circle_system = circle_system

    def update_colors(self, large_circles):
        """Update large circle colors based on their contained medium circles."""
        if not self.circle_system:
            print("Warning: No circle system set!")
            return False

        changes_made = False

        for large_circle in large_circles:
            # Get completely contained medium circles
            contained_circles = get_completely_contained_circles(
                large_circle.pos,
                CIRCLE_LARGE_RADIUS,
                self.circle_system.medium_circles,
                CIRCLE_MEDIUM_RADIUS,
            )

            # Count medium circles of each color
            red_count = sum(1 for mc in contained_circles if mc.color == RED)
            blue_count = sum(1 for mc in contained_circles if mc.color == BLUE)

            # Determine new color based on contained circle counts
            new_color = GREY
            if red_count >= 5:
                new_color = RED
            elif blue_count >= 5:
                new_color = BLUE

            # Update color if changed
            if new_color != large_circle.color:
                large_circle.color = new_color
                changes_made = True

        return changes_made
