import pygame
from ..utils.settings import WIDTH, HEIGHT


# debug_renderer.py
class DebugRenderer:
    def __init__(self, font):
        self.font = font
        self.slider_rect = pygame.Rect(20, HEIGHT - 40, 200, 20)
        self.slider_button_rect = pygame.Rect(20, HEIGHT - 45, 10, 30)
        self.dragging_slider = False

    def draw_connection_preview(
        self, surface, small_circles, connection_distance_multiplier, circle_radius
    ):
        """Draw preview circles showing connection ranges for each small circle"""

        # Create a transparent overlay surface
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # Calculate the radius for the connection preview circles
        connection_radius = circle_radius * connection_distance_multiplier

        # Draw a semi-transparent circle around each small circle
        for circle in small_circles:
            pygame.draw.circle(
                overlay,
                (255, 0, 0, 64),  # Semi-transparent red
                (int(circle.pos[0]), int(circle.pos[1])),
                int(connection_radius),
            )

        # Blit the overlay onto the main surface
        surface.blit(overlay, (0, 0))

    def handle_debug_events(self, event, debug_settings):
        """Handle debug-related mouse events"""

        # Handle mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.slider_button_rect.collidepoint(event.pos):
                self.dragging_slider = True
                debug_settings.showing_connections = True
                return True
            elif self.slider_rect.collidepoint(event.pos):
                self.dragging_slider = True
                debug_settings.showing_connections = True
                self._update_slider_position(event.pos[0], debug_settings)
                return True

        # Handle mouse button up
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging_slider:
                self.dragging_slider = False
                debug_settings.showing_connections = False
                return True

        # Handle mouse motion while dragging
        elif event.type == pygame.MOUSEMOTION and self.dragging_slider:
            self._update_slider_position(event.pos[0], debug_settings)
            return True

        return False

    def _update_slider_position(self, mouse_x, debug_settings):
        """Update slider position and debug settings based on mouse position"""
        # Calculate relative position on slider (0 to 1)
        relative_x = max(0, min(1, (mouse_x - self.slider_rect.x) / self.slider_rect.width))

        # Calculate new multiplier value
        new_multiplier = (
            debug_settings.min_multiplier
            + (debug_settings.max_multiplier - debug_settings.min_multiplier) * relative_x
        )

        print(f"Updating slider - relative_x: {relative_x}, new_multiplier: {new_multiplier:.2f}")

        # Update the debug settings
        if abs(new_multiplier - debug_settings.connection_distance_multiplier) > 0.01:
            debug_settings.connection_distance_multiplier = new_multiplier
            print(f"Multiplier updated to: {debug_settings.connection_distance_multiplier:.2f}")

    def draw_debug_ui(self, surface, debug_settings):
        """Draw the debug UI including slider and current value"""
        # Draw slider background
        pygame.draw.rect(surface, (200, 200, 200), self.slider_rect)

        # Calculate and draw slider button position
        relative_x = (
            debug_settings.connection_distance_multiplier - debug_settings.min_multiplier
        ) / (debug_settings.max_multiplier - debug_settings.min_multiplier)
        button_x = self.slider_rect.x + (self.slider_rect.width * relative_x)
        self.slider_button_rect.centerx = button_x
        pygame.draw.rect(surface, (100, 100, 100), self.slider_button_rect)

        # Draw value text
        text = f"Connection Distance: {debug_settings.connection_distance_multiplier:.1f}"
        text_surface = self.font.render(text, True, (255, 255, 255))
        surface.blit(text_surface, (self.slider_rect.right + 10, self.slider_rect.centery - 10))
