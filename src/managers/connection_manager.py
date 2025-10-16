from ..utils.settings import CIRCLE_SMALL_RADIUS
from ..utils.geometry import calculate_distance


class ConnectionManager:
    def __init__(self):
        self.adjacent_connections = {}
        self.current_multiplier = 3.2
        self.expected_distance = CIRCLE_SMALL_RADIUS * self.current_multiplier
        self.distance_tolerance = 0.1
        self.forbidden_connections = set(
            (
                # OUTTER SQUARES
                (213, 238),
                (248, 265),
                (46, 253),
                (10, 53),
                (62, 82),
                (96, 116),
                (131, 156),
                (172, 197),
                # INNER SQUARES
                (192, 234),
                (232, 260),
                (29, 258),
                (27, 81),
                (79, 115),
                (113, 146),
                (148, 151),
                (155, 194),
            )
        )

    def initialize_connections(self, small_circles):
        """Initialize empty connection sets for all circles."""
        self.adjacent_connections = {circle: set() for circle in small_circles}

    def update_connection_distances(self, multiplier):
        """Update the expected distance based on the multiplier."""
        multiplier = float(multiplier)
        if abs(self.current_multiplier - multiplier) > 0.01:
            self.current_multiplier = multiplier
            self.expected_distance = CIRCLE_SMALL_RADIUS * multiplier

    def update_adjacent_connections(self, small_circles):
        """Create connections between circles that are at the expected distance."""

        self.initialize_connections(small_circles)
        min_distance = self.expected_distance * (1 - self.distance_tolerance)
        max_distance = self.expected_distance * (1 + self.distance_tolerance)

        connection_count = 0
        checked_pairs = set()

        for i, circle1 in enumerate(small_circles):
            pos1 = circle1.pos
            for j, circle2 in enumerate(small_circles[i + 1 :], i + 1):
                pair_id = tuple(sorted([circle1.id, circle2.id]))
                if pair_id in self.forbidden_connections:
                    continue
                checked_pairs.add(pair_id)

                pos2 = circle2.pos
                distance = ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2) ** 0.5

                if min_distance <= distance <= max_distance:
                    self.adjacent_connections[circle1].add(circle2)
                    self.adjacent_connections[circle2].add(circle1)
                    connection_count += 1
