import pygame
from ..utils.settings import (
    CIRCLE_SMALL_RADIUS,
    CIRCLE_MEDIUM_RADIUS,
    CIRCLE_LARGE_RADIUS,
    WIDTH,
    HEIGHT,
    RED,
    BLUE,
    SHOW_IDS,
)
from ..utils.geometry import calculate_distance


class CircleRenderer:
    def __init__(self):
        self.circle_font = pygame.font.Font(None, 12)
        self.show_ids = SHOW_IDS
        self.REDUCED_CIRCLE_MEDIUM_RADIUS = int(CIRCLE_MEDIUM_RADIUS * 0.7)
        self.REDUCED_CIRCLE_LARGE_RADIUS = int(CIRCLE_LARGE_RADIUS * 0.55)
        self.INCREASED_CIRCLE_SMALL_RADIUS = int(CIRCLE_SMALL_RADIUS * 1.5)

        # Tracking original positions and IDs for each circle type
        self.small_circle_coords = []
        self.medium_circle_coords = []
        self.large_circle_coords = []
        self.initialized = {"small": False, "medium": False, "large": False}

        # Color schemes
        self.COLORS = {
            "neutral": {
                "small": self._hex_to_rgb("0xe0e0e0"),
                "medium": self._hex_to_rgb("0xa0a0b0"),
                "large": self._hex_to_rgb("0x7070a0"),
            },
            "red": {
                "small": self._hex_to_rgb("0xe01010"),
                "medium": self._hex_to_rgb("0xc01010"),
                "large": self._hex_to_rgb("0xa01010"),
            },
            "blue": {
                "small": self._hex_to_rgb("0x1010e0"),
                "medium": self._hex_to_rgb("0x1010c0"),
                "large": self._hex_to_rgb("0x1010a0"),
            },
        }

        # Set base colors
        self.BASE_SMALL_COLOR = self.COLORS["neutral"]["small"]
        self.BASE_MEDIUM_COLOR = self.COLORS["neutral"]["medium"]
        self.BASE_LARGE_COLOR = self.COLORS["neutral"]["large"]

        self.SMALL_ALPHA = int(0.780 * 255)
        self.MEDIUM_ALPHA = int(0.390 * 255)
        self.LARGE_ALPHA = int(0.260 * 255)

        # Cache for circle surfaces
        self.circle_cache = {}
        self._initialize_surface_cache()

        # Batch rendering surfaces
        self.small_circles_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.medium_circles_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def _hex_to_rgb(self, hex_color):
        """Convert hex color string to RGB tuple"""
        hex_color = hex_color.replace("0x", "")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def _get_circle_color(self, circle, size):
        """Get the appropriate color based on circle's color property and size"""
        if circle.color == RED:
            return self.COLORS["red"][size]
        elif circle.color == BLUE:
            return self.COLORS["blue"][size]
        return self.COLORS["neutral"][size]

    def _initialize_positions(self, circles, circle_type):
        """Initialize positions for a specific circle type."""
        if circle_type == "small":
            coords_list = self.small_circle_coords
        elif circle_type == "medium":
            coords_list = self.medium_circle_coords
        else:  # large
            coords_list = self.large_circle_coords

        for circle in circles:
            pos_tuple = (float(circle.pos[0]), float(circle.pos[1]))
            coords_list.append(pos_tuple)
            circle.original_pos = pos_tuple
            circle.original_id = len(coords_list) - 1
            circle.id = circle.original_id

        self.initialized[circle_type] = True

    def _update_id(self, circle, current_pos, circle_type):
        """Update circle ID based on its type and position."""
        if circle_type == "small":
            coords_list = self.small_circle_coords
        elif circle_type == "medium":
            coords_list = self.medium_circle_coords
        else:  # large
            coords_list = self.large_circle_coords

        for idx, orig_pos in enumerate(coords_list):
            if calculate_distance(current_pos, orig_pos) <= 5:
                circle.id = idx
                break

    def _initialize_surface_cache(self):
        """Pre-render common circle surfaces"""
        for radius in [self.INCREASED_CIRCLE_SMALL_RADIUS, self.REDUCED_CIRCLE_MEDIUM_RADIUS]:
            size = (radius * 2 + 2, radius * 2 + 2)

            # Cache surfaces for all color schemes
            for scheme in ["neutral", "red", "blue"]:
                for circle_size in ["small", "medium"]:
                    if (
                        radius == self.INCREASED_CIRCLE_SMALL_RADIUS and circle_size == "small"
                    ) or (radius == self.REDUCED_CIRCLE_MEDIUM_RADIUS and circle_size == "medium"):
                        color = self.COLORS[scheme][circle_size]
                        alpha = self.SMALL_ALPHA if circle_size == "small" else self.MEDIUM_ALPHA
                        surface = pygame.Surface(size, pygame.SRCALPHA)
                        pygame.draw.circle(
                            surface, (*color, alpha), (radius + 1, radius + 1), radius
                        )
                        self.circle_cache[f"{radius}_{scheme}_{circle_size}"] = surface

    def draw_small_circles(self, surface, small_circles):
        """Draw small circles with batched rendering"""
        if not self.initialized["small"]:
            self._initialize_positions(small_circles, "small")

        self.small_circles_surface.fill((0, 0, 0, 0))

        for circle in small_circles:
            current_pos = (float(circle.pos[0]), float(circle.pos[1]))
            self._update_id(circle, current_pos, "small")

            color = self._get_circle_color(circle, "small")
            circle_surface = self._get_cached_circle(
                self.INCREASED_CIRCLE_SMALL_RADIUS, color, self.SMALL_ALPHA, "small"
            )
            pos = (
                int(circle.pos[0] - self.INCREASED_CIRCLE_SMALL_RADIUS),
                int(circle.pos[1] - self.INCREASED_CIRCLE_SMALL_RADIUS),
            )
            self.small_circles_surface.blit(circle_surface, pos)

            if self.show_ids:
                self._draw_id(self.small_circles_surface, circle)

        surface.blit(self.small_circles_surface, (0, 0))

    def draw_medium_circles(self, surface, medium_circles):
        """Draw medium circles with batched rendering"""
        if not self.initialized["medium"]:
            self._initialize_positions(medium_circles, "medium")

        self.medium_circles_surface.fill((0, 0, 0, 0))

        for circle in medium_circles:
            current_pos = (float(circle.pos[0]), float(circle.pos[1]))
            self._update_id(circle, current_pos, "medium")

            color = self._get_circle_color(circle, "medium")
            circle_surface = self._get_cached_circle(
                self.REDUCED_CIRCLE_MEDIUM_RADIUS, color, self.MEDIUM_ALPHA, "medium"
            )
            pos = (
                int(circle.pos[0] - self.REDUCED_CIRCLE_MEDIUM_RADIUS),
                int(circle.pos[1] - self.REDUCED_CIRCLE_MEDIUM_RADIUS),
            )
            self.medium_circles_surface.blit(circle_surface, pos)

            if self.show_ids:
                self._draw_id(self.medium_circles_surface, circle)

        surface.blit(self.medium_circles_surface, (0, 0))

    def draw_large_circles(self, surface, circle_manager):
        """Draw the large background circles."""
        if not hasattr(circle_manager, "large_circles"):
            return

        for large_circle in circle_manager.large_circles:
            current_pos = (float(large_circle.pos[0]), float(large_circle.pos[1]))
            self._update_id(large_circle, current_pos, "large")

            circle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            color = self._get_circle_color(large_circle, "large")

            pygame.draw.circle(
                circle_surface,
                (*color, self.LARGE_ALPHA),
                (int(large_circle.pos[0]), int(large_circle.pos[1])),
                self.REDUCED_CIRCLE_LARGE_RADIUS,
            )
            surface.blit(circle_surface, (0, 0))

            if self.show_ids:
                self._draw_id(surface, large_circle)

    def _get_cached_circle(self, radius, color, alpha, size):
        """Get a cached circle surface or create new one"""
        # Determine which color scheme this color belongs to
        for scheme in ["neutral", "red", "blue"]:
            if color == self.COLORS[scheme][size]:
                key = f"{radius}_{scheme}_{size}"
                if key in self.circle_cache:
                    return self.circle_cache[key]

        # If not found in cache, create new surface
        size = (radius * 2 + 2, radius * 2 + 2)
        surface = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(surface, (*color, alpha), (radius + 1, radius + 1), radius)
        return surface

    def _draw_id(self, surface, circle):
        """Draw circle ID with caching"""
        id_text = self.circle_font.render(str(circle.id), True, (0, 0, 0))
        text_rect = id_text.get_rect(center=(int(circle.pos[0]), int(circle.pos[1])))
        surface.blit(id_text, text_rect)
