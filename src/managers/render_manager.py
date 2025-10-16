import pygame
from ..utils.settings import (
    GameMode,
    CIRCLE_SMALL_RADIUS,
    DebugSettings,
    BLUE,
    RED,
    DRAW_SAVE_LOAD_UI,
)
from ..renderers.debug_renderer import DebugRenderer
from ..renderers.game_renderer import GameRenderer
from ..renderers.save_load_ui import SaveLoadUI


class RenderManager:
    def __init__(self, screen, original_ui):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.debug_settings = DebugSettings()  # Will use singleton instance
        self.debug_renderer = DebugRenderer(self.font)
        self.game_renderer = GameRenderer(self.font, original_ui)
        self.show_debug_ui = False
        self.current_training_stats = None
        self.save_load_ui = SaveLoadUI(self.font)
        self.circle_system = None

    def set_circle_system(self, circle_system):
        """Set the circle system reference and share debug settings"""
        self.circle_system = circle_system
        # Share the debug settings instance with the circle system
        self.circle_system.debug_settings = self.debug_settings

    def update_training_stats(self, stats):
        """Update the current training statistics"""
        self.current_training_stats = stats

    def render_frame(self, game_mode, systems):
        """Render a frame of the game based on the current game mode."""
        self.screen.fill((255, 255, 255))  # White background

        if game_mode in [GameMode.MENU, GameMode.WAITING]:
            systems["menu"].draw(self.screen)
        else:
            if systems["circle"]:
                # First draw the game
                self.game_renderer.draw(self.screen, systems["circle"])

                # Draw debug UI if enabled
                if self.show_debug_ui:
                    # Draw connection preview if showing connections
                    if self.debug_settings.showing_connections:
                        self.debug_renderer.draw_connection_preview(
                            self.screen,
                            systems["circle"].small_circles,
                            self.debug_settings.connection_distance_multiplier,
                            CIRCLE_SMALL_RADIUS,
                        )
                    # Draw the debug UI controls
                    self.debug_renderer.draw_debug_ui(self.screen, self.debug_settings)

                # Draw save/load UI only in offline mode
                # if game_mode == GameMode.OFFLINE and DRAW_SAVE_LOAD_UI:
                #     self.save_load_ui.draw(self.screen, systems["circle"].save_load_manager)

                # if game_mode == GameMode.TRAINING:
                #     if self.current_training_stats:
                #         self.draw_training_stats(self.screen, self.current_training_stats)
                #         self.game_renderer.draw_training_stats(
                #             self.screen, self.current_training_stats
                #         )

        pygame.display.flip()

    def draw_training_stats(self, surface, stats):
        """Draw training statistics for both players"""
        if not stats:
            return

        y_offset = 240
        x_offset = 10
        line_height = 25

        # Blue Player Stats
        blue_stats = stats.get("blue_player", {})
        texts = [
            f"Wins: {blue_stats.get('wins', {}).get('blue', 0)}",
        ]

        for text in texts:
            text_surface = self.font.render(text, True, BLUE)
            surface.blit(text_surface, (x_offset, y_offset))
            y_offset += line_height

        y_offset += 10  # Add spacing between players

        # Red Player Stats
        red_stats = stats.get("red_player", {})
        texts = [
            f"Wins: {red_stats.get('wins', {}).get('red', 0)}",
        ]

        for text in texts:
            text_surface = self.font.render(text, True, RED)
            surface.blit(text_surface, (x_offset, y_offset))
            y_offset += line_height

    def handle_debug_events(self, event):
        """Handle debug-related events."""
        if self.debug_renderer.handle_debug_events(event, self.debug_settings):
            if self.circle_system:
                print("\nRenderManager handling debug event")
                print(
                    f"Debug settings multiplier: {self.debug_settings.connection_distance_multiplier}"
                )
                self.circle_system.update_adjacent_connections()
            return True
        return False
