import math
from .settings import CIRCLE_MEDIUM_RADIUS, CIRCLE_SMALL_RADIUS
from typing import List, Tuple, Union
from ..utils.circle_classes import SmallCircle, MediumCircle, LargeCircle
from ..utils.settings import CIRCLE_MEDIUM_RADIUS, CIRCLE_LARGE_RADIUS
import math


@staticmethod
def get_regular_polygon_vertices(
    center: Tuple[float, float], radius: float, n_vertices: int, rotation: float = 0
) -> List[Tuple[float, float]]:
    """Get vertices of a regular polygon with n vertices"""
    vertices = []
    for i in range(n_vertices):
        angle = rotation + (2 * math.pi * i) / n_vertices
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices


def is_point_inside_circle(point: List[float], circle_center: List[float], radius: float) -> bool:
    """Check if a point is inside a circle."""
    dx = point[0] - circle_center[0]
    dy = point[1] - circle_center[1]
    return dx * dx + dy * dy <= radius * radius


def get_circles_inside_at_position(center_pos, radius, circles):
    """
    Get all circles that are within radius of center_pos.
    Uses proper distance calculation from center of medium circle to center of small circle.
    """
    inside_circles = []
    max_distance = radius  # This is CIRCLE_MEDIUM_RADIUS when used for medium circles

    for circle in circles:
        dx = circle.pos[0] - center_pos[0]
        dy = circle.pos[1] - center_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)

        # A small circle is considered inside if its center is within the medium circle's radius
        if distance <= max_distance:
            inside_circles.append(circle)

    return inside_circles


def calculate_circle_intersections(
    circle1_center: List[float],
    circle2_center: List[float],
    circle1_radius: float,
    circle2_radius: float,
) -> bool:
    """Check if two circles intersect."""
    dx = circle1_center[0] - circle2_center[0]
    dy = circle1_center[1] - circle2_center[1]
    distance = math.sqrt(dx * dx + dy * dy)
    return distance <= (circle1_radius + circle2_radius)


def calculate_distance(p1: List[float], p2: List[float]) -> float:
    """Calculate the distance between two points."""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)


def is_circle_completely_inside(
    inner_circle_pos: List[float],
    outer_circle_pos: List[float],
    inner_radius: float,
    outer_radius: float,
) -> bool:
    """
    Check if one circle is completely inside another circle.
    Returns True only if the inner circle (including its border) is completely within the outer circle.
    """
    center_distance = calculate_distance(inner_circle_pos, outer_circle_pos)
    # The inner circle must be far enough from the edge of the outer circle that its entire
    # radius fits within the outer circle
    return center_distance + inner_radius <= outer_radius


def is_circle_inside(circle_pos, medium_circle_pos):
    distance = calculate_distance(circle_pos, medium_circle_pos)
    return distance <= CIRCLE_MEDIUM_RADIUS - CIRCLE_SMALL_RADIUS


def is_point_in_multiple_circles(point, medium_circles):
    count = 0
    for lc in medium_circles:
        distance = calculate_distance(point, lc.pos)
        if distance <= CIRCLE_MEDIUM_RADIUS:
            count += 1
    return count >= 2


def is_point_in_circle_intersection(
    point: List[float], circles: List[Union[MediumCircle, LargeCircle]], radius: float
) -> bool:
    """
    Check if a point is in the intersection of any two circles of the same type.
    Returns True if the point is in an intersection area.
    """
    intersections = []

    # Check each pair of circles
    for i, circle1 in enumerate(circles):
        for circle2 in circles[i + 1 :]:
            # Calculate distance between circle centers
            distance = calculate_distance(circle1.pos, circle2.pos)

            # If circles overlap
            if distance < 2 * radius:
                # Check if point is inside both circles
                if is_point_inside_circle(point, circle1.pos, radius) and is_point_inside_circle(
                    point, circle2.pos, radius
                ):
                    return True

    return False


def get_completely_contained_circles(center_pos, radius, circles, small_radius):
    """
    Get all circles that are completely inside a given position's radius,
    accounting for the size of the circles being checked.
    """
    contained_circles = []

    for circle in circles:
        if is_circle_completely_inside(circle.pos, center_pos, small_radius, radius):
            contained_circles.append(circle)

    return contained_circles
