from ...utils.settings import RED, BLUE, GREY, CIRCLE_MEDIUM_RADIUS
import math


class MediumCircleManager:
    @staticmethod
    def update_colors(medium_circles, get_circles_inside):
        changed = False

        # Update based on contained circles
        for medium_circle in medium_circles:
            circles_inside = get_circles_inside(medium_circle)
            red_count = sum(1 for circle in circles_inside if circle.color == RED)
            blue_count = sum(1 for circle in circles_inside if circle.color == BLUE)

            new_color = None
            if red_count > blue_count:
                new_color = RED
            elif blue_count > red_count:
                new_color = BLUE
            elif red_count == blue_count and red_count != 0:
                new_color = GREY

            if new_color is not None and medium_circle.color != new_color:
                medium_circle.color = new_color
                changed = True

        # Check intersections
        intersection_changed = MediumCircleManager._check_intersections(medium_circles)

        return changed or intersection_changed

    @staticmethod
    def _check_intersections(medium_circles):
        changed = False
        for circle in medium_circles:
            if circle.color == GREY:
                intersecting_red = 0
                intersecting_blue = 0

                for other_circle in medium_circles:
                    if other_circle != circle:
                        dx = circle.pos[0] - other_circle.pos[0]
                        dy = circle.pos[1] - other_circle.pos[1]
                        distance = math.sqrt(dx**2 + dy**2)

                        if distance < 2 * CIRCLE_MEDIUM_RADIUS:
                            if other_circle.color == RED:
                                intersecting_red += 1
                            elif other_circle.color == BLUE:
                                intersecting_blue += 1

                if intersecting_red >= 2:
                    circle.color = RED
                    changed = True
                elif intersecting_blue >= 2:
                    circle.color = BLUE
                    changed = True

        return changed
