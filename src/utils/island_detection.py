from .settings import RED, BLUE, GREY


class IslandDetector:
    @staticmethod
    def find_islands(small_circles, connection_manager):
        red_islands = []
        blue_islands = []
        visited = set()

        for circle in small_circles:
            if circle not in visited:
                if circle.color == RED:
                    island = IslandDetector._find_connected_component(
                        circle, RED, visited, connection_manager
                    )
                    if island:
                        red_islands.append(island)
                elif circle.color == BLUE:
                    island = IslandDetector._find_connected_component(
                        circle, BLUE, visited, connection_manager
                    )
                    if island:
                        blue_islands.append(island)

        return red_islands, blue_islands

    @staticmethod
    def _find_connected_component(start_circle, color, visited, connection_manager):
        if start_circle in visited:
            return None

        component = []
        queue = [start_circle]
        local_visited = set()

        while queue:
            current = queue.pop(0)
            if current in local_visited:
                continue

            local_visited.add(current)
            visited.add(current)

            if current.color == color:
                component.append(current)
                adjacent_circles = connection_manager.adjacent_connections.get(current, [])
                for adjacent in adjacent_circles:
                    if adjacent.color == color and adjacent not in local_visited:
                        queue.append(adjacent)

        if component:
            is_surrounded = IslandDetector._is_surrounded_by_opposite_color(
                component, color, connection_manager
            )
            return component if is_surrounded else None
        return None

    @staticmethod
    def _is_surrounded_by_opposite_color(island, color, connection_manager):
        border_circles = set()
        for circle in island:
            border_circles.update(connection_manager.adjacent_connections.get(circle, []))

        border_circles = border_circles - set(island)
        opposite_color = BLUE if color == RED else RED

        is_surrounded = (
            all(c.color == opposite_color for c in border_circles) and len(border_circles) > 0
        )

        return is_surrounded
