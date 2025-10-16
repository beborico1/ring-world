import pygame
from ..utils.settings import WIDTH


class SaveLoadUI:
    """Handles UI elements for save/load functionality"""

    def __init__(self, font):
        self.font = font
        self.button_font = pygame.font.Font(None, 36)
        self.save_button = pygame.Rect(WIDTH - 140, 10, 100, 40)
        self.load_button = pygame.Rect(WIDTH - 140, 60, 100, 40)
        self.save_feedback_time = 0
        self.save_feedback_duration = 2000  # 2 seconds

    def draw(self, surface, save_load_manager):
        """Draw save/load UI elements"""
        # Draw save button
        pygame.draw.rect(surface, (200, 200, 200), self.save_button)
        save_text = self.button_font.render("Save", True, (0, 0, 0))
        save_text_rect = save_text.get_rect(center=self.save_button.center)
        surface.blit(save_text, save_text_rect)

        # Draw load button
        pygame.draw.rect(surface, (200, 200, 200), self.load_button)
        load_text = self.button_font.render("Load", True, (0, 0, 0))
        load_text_rect = load_text.get_rect(center=self.load_button.center)
        surface.blit(load_text, load_text_rect)

        # Draw save feedback if active
        current_time = pygame.time.get_ticks()
        if current_time < self.save_feedback_time + self.save_feedback_duration:
            feedback = self.button_font.render("Game Saved!", True, (0, 150, 0))
            feedback_rect = feedback.get_rect(center=(WIDTH - 90, 110))
            surface.blit(feedback, feedback_rect)

    def handle_events(self, event, save_load_manager):
        """Handle save/load related events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Handle save button click
            if self.save_button.collidepoint(mouse_pos):
                save_load_manager.save_game()
                self.save_feedback_time = pygame.time.get_ticks()
                return True

            # Handle load button click
            if self.load_button.collidepoint(mouse_pos):
                save_load_manager.load_game()
                return True

        return False
