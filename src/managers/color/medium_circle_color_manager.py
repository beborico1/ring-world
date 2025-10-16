from ...utils.settings import RED, BLUE, GREY
from .neighbor_rule_manager import NeighborRuleManager


class MediumCircleColorManager:
    def __init__(self, intersection_checker):
        self.intersection_checker = intersection_checker

    def update_colors(
        self, medium_circles, get_circles_inside_func, connection_manager, after_rotation=False
    ):
        """Update medium circle colors based on contained circles and intersections."""
        changes_made = False

        # Update based on contained circles
        changes_made = self._update_based_on_contained_circles(
            medium_circles, get_circles_inside_func
        )

        # Check for intersections
        intersection_changes = self.intersection_checker.check_medium_circle_intersections(
            medium_circles
        )
        changes_made = changes_made or intersection_changes

        # Apply neighbor rule after rotation if needed
        if after_rotation:
            changes_made = self._apply_post_rotation_updates(
                medium_circles, get_circles_inside_func, connection_manager
            )

        return changes_made

    def _update_based_on_contained_circles(self, medium_circles, get_circles_inside_func):
        changes_made = False
        for medium_circle in medium_circles:
            circles_inside = get_circles_inside_func(medium_circle)
            if not circles_inside:
                continue

            red_count = sum(1 for circle in circles_inside if circle.color == RED)
            blue_count = sum(1 for circle in circles_inside if circle.color == BLUE)

            new_color = GREY
            if red_count >= 5:
                new_color = RED
            elif blue_count >= 5:
                new_color = BLUE

            if new_color != medium_circle.color:
                changes_made = True
                medium_circle.color = new_color

        return changes_made

    def _apply_post_rotation_updates(
        self, medium_circles, get_circles_inside_func, connection_manager
    ):
        changes_made = False
        neighbor_rule_manager = NeighborRuleManager()

        all_circles = []
        for medium_circle in medium_circles:
            all_circles.extend(get_circles_inside_func(medium_circle))

        while neighbor_rule_manager.apply_neighbor_color_rule(all_circles, connection_manager):
            changes_made = True
            self._update_based_on_contained_circles(medium_circles, get_circles_inside_func)

        return changes_made
