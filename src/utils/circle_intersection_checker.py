# circle_intersection_checker.py
import math
from .settings import RED, BLUE, GREY, CIRCLE_MEDIUM_RADIUS


class CircleIntersectionChecker:
    @staticmethod
    def check_medium_circle_intersections(medium_circles):
        """Check for intersections between medium circles and update colors accordingly"""
        changes_made = False
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
                    changes_made = True
                elif intersecting_blue >= 2:
                    circle.color = BLUE
                    changes_made = True

        return changes_made
