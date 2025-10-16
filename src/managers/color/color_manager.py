from ...utils.circle_intersection_checker import CircleIntersectionChecker
from .medium_circle_color_manager import MediumCircleColorManager
from .large_circle_color_manager import LargeCircleColorManager
from .player_color_manager import PlayerColorManager


class GameColorManager:
    def __init__(self, circle_system):
        self.intersection_checker = CircleIntersectionChecker()
        self.medium_circle_manager = MediumCircleColorManager(self.intersection_checker)
        self.large_circle_manager = LargeCircleColorManager(circle_system)
        self._player_manager = PlayerColorManager()
        self.turn = self._player_manager.turn
        self.player_color = self._player_manager.player_color

    def set_player_color(self, color: str):
        self._player_manager.set_player_color(color)
        self.player_color = self._player_manager.player_color

    def check_medium_circle_intersections(self, medium_circles):
        return self.intersection_checker.check_medium_circle_intersections(medium_circles)

    def update_medium_circle_colors(
        self, medium_circles, get_circles_inside_func, connection_manager, after_rotation=False
    ):
        """Original method signature maintained"""
        medium_circle_changes = self.medium_circle_manager.update_colors(
            medium_circles, get_circles_inside_func, connection_manager, after_rotation
        )

        return medium_circle_changes

    def update_large_circle_colors(self, large_circles):
        """Original method for updating large circles"""
        return self.large_circle_manager.update_colors(large_circles)

    def update_all_colors(
        self,
        medium_circles,
        large_circles,
        get_circles_inside_func,
        connection_manager,
        after_rotation=False,
    ):
        """Combined update method"""
        medium_circle_changes = self.update_medium_circle_colors(
            medium_circles, get_circles_inside_func, connection_manager, after_rotation
        )

        large_circle_changes = self.update_large_circle_colors(large_circles)

        return medium_circle_changes or large_circle_changes
