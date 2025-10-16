from ...utils.settings import RED, BLUE, GREY


class NeighborRuleManager:
    def apply_neighbor_color_rule(self, circles, connection_manager):
        """Apply the neighbor color rule to grey circles."""
        changes_made = False
        grey_circles = [c for c in circles if c.color == GREY]

        for circle in grey_circles:
            neighbors = connection_manager.adjacent_connections.get(circle, [])
            red_neighbors = sum(1 for n in neighbors if n.color == RED)
            blue_neighbors = sum(1 for n in neighbors if n.color == BLUE)

            if red_neighbors >= 2:
                circle.color = RED
                changes_made = True
            elif blue_neighbors >= 2:
                circle.color = BLUE
                changes_made = True

        return changes_made
