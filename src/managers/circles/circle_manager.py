from typing import List, Tuple, Dict, Set
from ...utils.settings import WIDTH, HEIGHT, GREY, RED, BLUE, CIRCLE_MEDIUM_RADIUS
from ...utils.circle_initialization import FractalCircleInitializer
from ...utils.circle_classes import MediumCircle, SmallCircle, LargeCircle
from ...utils.geometry import get_circles_inside_at_position
from ...utils.island_detection import IslandDetector


class CircleManager:
    def __init__(self, reduced_version=False):
        print("Initializing CircleManager", reduced_version)
        self.large_circles: List[LargeCircle] = []
        self.medium_circles: List[MediumCircle] = []
        self.small_circles: List[SmallCircle] = []
        self.center = (WIDTH // 2, HEIGHT // 2)
        self.fractal_initializer = FractalCircleInitializer(
            self.center, CIRCLE_MEDIUM_RADIUS * 4, reduced_version=reduced_version
        )

    def _initialize_system(self):
        """Initialize all circles in the system using fractal mathematics."""

        raw_large_circles = self.fractal_initializer.initialize_large_circles(8)

        small_id = 0
        medium_id = 0
        large_id = 0

        seen_small_circles: Set[Tuple[float, float]] = set()
        seen_medium_circles: Set[Tuple[float, float]] = set()

        for raw_large in raw_large_circles:
            medium_circles_for_large = []

            for raw_medium in raw_large["medium_circles"]:
                # Process medium circle first
                medium_pos = raw_medium["position"]
                medium_pos_key = (round(medium_pos[0], 3), round(medium_pos[1], 3))

                if medium_pos_key not in seen_medium_circles:
                    seen_medium_circles.add(medium_pos_key)
                    medium_circle = MediumCircle(medium_id, medium_pos, [])
                    medium_circle.color = GREY
                    self.medium_circles.append(medium_circle)
                    medium_circles_for_large.append(medium_circle)
                    medium_id += 1

                # Process small circles
                for raw_small in raw_medium["small_circles"]:
                    pos = raw_small["position"]
                    pos_key = (round(pos[0], 3), round(pos[1], 3))

                    if pos_key not in seen_small_circles:
                        seen_small_circles.add(pos_key)
                        small_circle = SmallCircle(small_id, pos)
                        small_circle.color = GREY
                        self.small_circles.append(small_circle)
                        small_id += 1

            # Create large circle
            large_circle = LargeCircle(large_id, raw_large["position"], medium_circles_for_large)
            large_circle.color = GREY
            self.large_circles.append(large_circle)
            large_id += 1

        # Verify initialization
        for medium_circle in self.medium_circles:
            contained = self.get_circles_inside(medium_circle)
            if len(contained) != 8:
                print("WARNING: Should contain exactly 8 small circles!")

    def get_circles_inside(self, medium_circle: MediumCircle) -> List[SmallCircle]:
        """Dynamically get all small circles that are inside this medium circle"""
        return get_circles_inside_at_position(
            medium_circle.pos, CIRCLE_MEDIUM_RADIUS, self.small_circles
        )

    def find_and_neutralize_islands(self, connection_manager):
        """Find and neutralize isolated groups of small circles"""
        red_islands, blue_islands = IslandDetector.find_islands(
            self.small_circles, connection_manager
        )
        neutralized = []

        # Process all islands regardless of size
        for island in red_islands + blue_islands:
            for circle in island:
                circle.set_color(GREY)
                neutralized.append(circle)

        return neutralized

    def print_neutralized_circles(self, neutralized):
        """Print information about neutralized circles"""
        if neutralized:
            print("\nNeutralized circles:")
            print(f"IDs: {[circle.id for circle in neutralized]}")
        else:
            print("\nNo circles were neutralized this turn.")

    def update_medium_circle_colors(self):
        """Update the colors of medium circles based on their contained circles"""
        changes = []

        # Update medium circles
        for medium_circle in self.medium_circles:
            # Dynamically get contained circles based on current positions
            small_circles = self.get_circles_inside(medium_circle)

            # Count colors
            red_count = sum(1 for circle in small_circles if circle.color == RED)
            blue_count = sum(1 for circle in small_circles if circle.color == BLUE)

            # Determine new color based on contained circles
            new_color = None
            if red_count >= 5:
                new_color = RED  # RED
            elif blue_count >= 5:
                new_color = BLUE  # BLUE
            else:
                new_color = GREY  # GREY

            # Record change if color is different
            if new_color != medium_circle.color:
                changes.append((medium_circle, new_color))
                medium_circle.color = new_color

        return changes

    def reset_circles(self):
        """Reset all circles to their initial state."""
        for circle in self.small_circles:
            circle.set_color(GREY)  # Reset to grey

        for circle in self.medium_circles:
            circle.color = None
            circle.angle = 0

        for circle in self.large_circles:
            circle.color = None
            circle.angle = 0

    def get_next_medium_circle(self, current_circle: MediumCircle) -> MediumCircle:
        """Get the next medium circle in sequence, considering large circle organization"""
        # First try to find the next circle within the same large circle
        for large_circle in self.large_circles:
            if current_circle in large_circle.medium_circles:
                idx = large_circle.medium_circles.index(current_circle)
                return large_circle.medium_circles[(idx + 1) % len(large_circle.medium_circles)]

        # Fallback to global list if not found in large circles
        idx = self.medium_circles.index(current_circle)
        return self.medium_circles[(idx + 1) % len(self.medium_circles)]
