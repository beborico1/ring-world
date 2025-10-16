import pygame
from ..utils.settings import (
    CIRCLE_SMALL_RADIUS,
    CIRCLE_MEDIUM_RADIUS,
    CIRCLE_LARGE_RADIUS,
    CENTER_CLICK_RADIUS,
)
from ..utils.circle_classes import SmallCircle, MediumCircle, LargeCircle


class GameBoardRenderer:
    def __init__(self):
        self.CONNECTION_COLOR = (100, 100, 100)
        self.CENTER_COLOR = (150, 150, 150)
        self.SELECTED_COLOR = (64, 144, 96)  # New color #409060

        # Cache for guide surfaces and current turn
        self.guide_cache = {}
        self.current_turn = None
        self.selected_move = None
        self._initialize_guide_cache("red")

    def _create_guide_surface(self, guide_radius, turn, is_selected=False):
        """Create a guide surface with a proper radial gradient"""
        # Size of surface (add some padding for blur)
        padding = guide_radius // 2
        size = guide_radius * 2 + padding * 2

        # Create surface
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)

        # Set color based on turn and selection state
        if is_selected:
            guide_color = self.SELECTED_COLOR
        else:
            guide_color = (255, 0, 0) if turn == "red" else (0, 0, 255)

        # Create gradient by drawing concentric circles from outside in
        steps = 30
        for i in range(steps):
            ratio = i / steps
            current_radius = int(guide_radius * (1 - ratio))
            alpha = int(150 * (ratio**0.5))

            pygame.draw.circle(surface, (*guide_color, alpha), center, current_radius)

        # Apply a final blur for smoothness
        final_surface = self._gaussian_blur(surface, guide_radius // 8)

        return final_surface, size // 2

    def _gaussian_blur(self, surface, blur_amount):
        """Apply gaussian blur effect"""
        if blur_amount <= 0:
            return surface

        size = surface.get_size()
        blur_surface = pygame.Surface(size, pygame.SRCALPHA)

        kernel_size = max(1, blur_amount // 2)

        for x in range(kernel_size, size[0] - kernel_size):
            for y in range(kernel_size, size[1] - kernel_size):
                r, g, b, a = 0, 0, 0, 0
                count = 0

                for dx in range(-kernel_size, kernel_size + 1):
                    for dy in range(-kernel_size, kernel_size + 1):
                        px = x + dx
                        py = y + dy
                        if 0 <= px < size[0] and 0 <= py < size[1]:
                            color = surface.get_at((px, py))
                            r += color[0]
                            g += color[1]
                            b += color[2]
                            a += color[3]
                            count += 1

                if count > 0:
                    blur_surface.set_at((x, y), (r // count, g // count, b // count, a // count))

        return blur_surface

    def _initialize_guide_cache(self, turn):
        """Pre-render guide surfaces for different sizes"""
        self.current_turn = turn
        self.guide_cache.clear()

        # Create both selected and unselected versions for each size
        for radius in [CIRCLE_SMALL_RADIUS, CIRCLE_MEDIUM_RADIUS, CIRCLE_LARGE_RADIUS]:
            guide_radius = int(radius * 0.3) if radius != CIRCLE_SMALL_RADIUS else int(radius * 0.7)

            # Unselected surface
            unselected_surface, half_size = self._create_guide_surface(guide_radius, turn, False)
            self.guide_cache[(radius, False)] = (unselected_surface, half_size)

            # Selected surface
            selected_surface, half_size = self._create_guide_surface(guide_radius, turn, True)
            self.guide_cache[(radius, True)] = (selected_surface, half_size)

    def draw_valid_moves(self, surface, valid_moves, turn):
        """Draw guide indicators for valid moves"""
        # Reinitialize cache if turn has changed
        if turn != self.current_turn:
            self._initialize_guide_cache(turn)

        for move in valid_moves:
            if hasattr(move, "pos"):
                # Determine the guide radius based on move type
                if isinstance(move, SmallCircle):
                    radius = CIRCLE_SMALL_RADIUS
                    guide_radius = int(radius * 0.7)  # Small circles use 0.7
                elif isinstance(move, MediumCircle) or isinstance(move, LargeCircle):
                    radius = CIRCLE_MEDIUM_RADIUS
                    guide_radius = int(radius * 0.3)  # Medium and large circles use 0.3
                else:
                    continue

                # Check if this move is selected
                is_selected = (
                    self.selected_move
                    and hasattr(self.selected_move, "pos")
                    and self.selected_move.pos == move.pos
                )

                # Get the appropriate guide surface
                cache_key = (radius, is_selected)
                if cache_key not in self.guide_cache:
                    guide_surface, half_size = self._create_guide_surface(
                        guide_radius, turn, is_selected
                    )
                    self.guide_cache[cache_key] = (guide_surface, half_size)

                guide_surface, half_size = self.guide_cache[cache_key]
                pos = (int(move.pos[0] - half_size) + 1, int(move.pos[1] - half_size) + 1)
                surface.blit(guide_surface, pos)

    def draw_connections(self, surface, adjacent_connections, is_animating):
        """Draw connections between circles."""
        if not is_animating:
            for circle1, connected_circles in adjacent_connections.items():
                for circle2 in connected_circles:
                    pygame.draw.line(
                        surface,
                        self.CONNECTION_COLOR,
                        (int(circle1.pos[0]), int(circle1.pos[1])),
                        (int(circle2.pos[0]), int(circle2.pos[1])),
                        2,
                    )
