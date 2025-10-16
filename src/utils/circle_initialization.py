import math
from typing import List, Tuple
from ..utils.geometry import get_regular_polygon_vertices, calculate_distance


class FractalCircleInitializer:
    """Initializes circles following fractal mathematical principles"""

    def __init__(
        self,
        center: Tuple[float, float],
        radius: float,
        distance_threshold: float = 0.1,
        reduced_version: bool = False,
    ):
        print("Initializing FractalCircleInitializer", reduced_version)
        """
        Initialize the FractalCircleInitializer.

        Args:
            center: Center point for the entire fractal pattern
            radius: Base radius for the mediumst circles
            distance_threshold: Minimum distance between circles to be considered unique
            reduced_version: If True, creates a simplified version with only one large circle
        """
        self.center = center
        self.base_radius = radius
        self.level_radius_ratio = math.sqrt(2) - 1
        self.distance_threshold = distance_threshold
        self.reduced_version = reduced_version
        # Track total statistics
        self.total_initial_small_circles = 0
        self.total_final_small_circles = 0

    def deduplicate_circles(self, circles: List[dict]) -> tuple[List[dict], int]:
        """Remove duplicate circles based on position proximity"""
        unique_circles = []
        duplicates_found = 0

        for circle in circles:
            is_duplicate = False
            for unique_circle in unique_circles:
                if (
                    calculate_distance(circle["position"], unique_circle["position"])
                    < self.distance_threshold
                ):
                    is_duplicate = True
                    duplicates_found += 1
                    break
            if not is_duplicate:
                unique_circles.append(circle)

        return unique_circles, duplicates_found

    def initialize_large_circles(self, num_large_circles: int = 8) -> List[dict]:
        """Initialize large circles following the fractal pattern with deduplication"""
        large_circles = []
        self.total_initial_small_circles = 0

        # If reduced version, only create one large circle at the center
        if self.reduced_version:
            num_large_circles = 1
            large_circle_positions = [self.center]
        else:
            # Calculate large circle positions
            large_circle_positions = get_regular_polygon_vertices(
                self.center,
                self.base_radius,
                num_large_circles,
                rotation=math.pi / num_large_circles,
            )

        # Initialize large circles
        for i, pos in enumerate(large_circle_positions):
            large_circle = {
                "id": i,
                "position": pos,
                "medium_circles": self.initialize_medium_circles(pos),
            }
            large_circles.append(large_circle)

        # Print initial counts
        initial_medium_count = sum(len(sc["medium_circles"]) for sc in large_circles)

        # Deduplicate medium circles across all large circles
        total_medium_deduped = self.deduplicate_medium_circles(large_circles)
        final_medium_count = sum(len(sc["medium_circles"]) for sc in large_circles)

        # Deduplicate all small circles across all medium circles
        all_small_circles = []
        for large_circle in large_circles:
            for medium_circle in large_circle["medium_circles"]:
                all_small_circles.extend(medium_circle["small_circles"])

        deduped_small_circles, total_small_deduped = self.deduplicate_circles(all_small_circles)

        # Create a dictionary to look up unique small circles by position
        unique_small_circles_dict = {
            str(circle["position"]): circle for circle in deduped_small_circles
        }

        # Update small circles in each medium circle to reference only unique circles
        for large_circle in large_circles:
            for medium_circle in large_circle["medium_circles"]:
                unique_small_circles = []
                for small_circle in medium_circle["small_circles"]:
                    pos_key = str(small_circle["position"])
                    if pos_key in unique_small_circles_dict:
                        unique_small_circles.append(unique_small_circles_dict[pos_key])
                medium_circle["small_circles"] = unique_small_circles

        print(f"medium circles:")
        print(f"  Initial count: {initial_medium_count}")
        print(f"  Duplicates removed: {total_medium_deduped}")
        print(f"  Final count: {final_medium_count}")
        print(f"Small circles:")
        print(f"  Initial count: {self.total_initial_small_circles}")
        print(
            f"  Duplicates removed: {self.total_initial_small_circles - len(deduped_small_circles)}"
        )
        print(f"  Final count: {len(deduped_small_circles)}")

        return large_circles

    def deduplicate_medium_circles(self, large_circles: List[dict]) -> int:
        """Deduplicate medium circles across all large circles"""
        all_medium_circles = []
        total_deduped = 0

        for large_circle in large_circles:
            medium_circles = large_circle["medium_circles"]
            deduped_medium_circles = []

            for medium_circle in medium_circles:
                is_duplicate = False
                # Check against all previously seen medium circles
                for existing_circle in all_medium_circles:
                    if (
                        calculate_distance(medium_circle["position"], existing_circle["position"])
                        < self.distance_threshold
                    ):
                        is_duplicate = True
                        total_deduped += 1
                        break

                if not is_duplicate:
                    deduped_medium_circles.append(medium_circle)
                    all_medium_circles.append(medium_circle)

            large_circle["medium_circles"] = deduped_medium_circles

        return total_deduped

    def initialize_medium_circles(self, center: Tuple[float, float]) -> List[dict]:
        """Initialize all 8 medium circles in an octagonal pattern"""
        medium_circles = []
        medium_circle_radius = self.base_radius * self.level_radius_ratio

        # Always create 8 medium circles in octagonal arrangement
        positions = get_regular_polygon_vertices(
            center, medium_circle_radius, 8, rotation=math.pi / 8
        )

        # Create all 8 circles
        for i, pos in enumerate(positions):
            medium_circle = {
                "id": i,
                "position": pos,
                "small_circles": self.initialize_small_circles(pos),
            }
            medium_circles.append(medium_circle)

        return medium_circles

    def initialize_small_circles(self, center: Tuple[float, float]) -> List[dict]:
        """Initialize small circles within a medium circle"""
        small_circles = []
        small_circle_radius = self.base_radius * self.level_radius_ratio * self.level_radius_ratio

        positions = get_regular_polygon_vertices(
            center, small_circle_radius, 8, rotation=math.pi / 8
        )

        for i, pos in enumerate(positions):
            small_circle = {"id": i, "position": pos}
            small_circles.append(small_circle)

        self.total_initial_small_circles += len(small_circles)
        return small_circles
