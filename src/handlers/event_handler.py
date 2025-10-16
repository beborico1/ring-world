import pygame
from ..utils.settings import (
    CIRCLE_MEDIUM_RADIUS,
    CIRCLE_LARGE_RADIUS,
    CIRCLE_SMALL_RADIUS,
    RED,
    BLUE,
    PHASE_PLACEMENT,
    GREY,
    GameMode,
)
from ..utils.geometry import calculate_distance, get_completely_contained_circles
import random


class EventHandler:
    def __init__(self, circle_system, game_controller, original_ui):
        self.original_ui = original_ui
        self.system = circle_system
        self.game_controller = game_controller
        self.training_manager = None
        self.winner_buttons = None
        self.selected_move = None

    def _select_random_move(self):
        """Select and execute a random valid move from available moves."""
        if not self.system or self.system.is_any_circle_animating():
            return False

        valid_moves = self.system.move_handler.get_valid_moves()
        if not valid_moves:
            return False

        random_move = random.choice(valid_moves)
        current_color = self.system.game_state.turn

        if self.system.game_state.phase == PHASE_PLACEMENT:
            return self.system.move_handler.make_placement_move(random_move, current_color)
        else:
            # For rotation moves, we need to handle both medium and large circles
            if hasattr(random_move, "small_circles"):  # medium circle
                return self.system.move_handler.make_rotation_move(random_move, current_color)
            elif hasattr(random_move, "medium_circles"):  # large circle
                # Check if we should use contained circles only
                contained_circles = get_completely_contained_circles(
                    random_move.pos,
                    CIRCLE_LARGE_RADIUS,
                    self.system.medium_circles,
                    CIRCLE_MEDIUM_RADIUS,
                )
                current_color_rgb = RED if current_color == "red" else BLUE
                if self._validate_large_circle_click(contained_circles, current_color_rgb):
                    return self.system.move_handler.make_rotation_move(
                        random_move, current_color, contained_circles_only=True
                    )
        return False

    def _count_valid_moves_by_type(self, mouse_pos, valid_moves):
        """Count how many valid move areas of each type contain this point."""
        large_count = 0
        medium_count = 0
        placement_count = 0

        for move in valid_moves:
            # Always use CIRCLE_MEDIUM_RADIUS + 4 for rotation moves (both large and medium)
            # as that's the radius of the green contour shown to the player
            if hasattr(move, "medium_circles"):  # large circle
                if calculate_distance(mouse_pos, move.pos) <= CIRCLE_MEDIUM_RADIUS + 4:
                    large_count += 1
            elif hasattr(move, "small_circles"):  # medium circle
                if calculate_distance(mouse_pos, move.pos) <= CIRCLE_MEDIUM_RADIUS + 4:
                    medium_count += 1
            else:  # small circle (placement)
                if calculate_distance(mouse_pos, move.pos) <= CIRCLE_SMALL_RADIUS + 4:
                    placement_count += 1

        total_count = large_count + medium_count + placement_count

        return total_count, large_count, medium_count, placement_count

    def _get_valid_move_at_point(self, mouse_pos, valid_moves):
        """Get the valid move at this point if it's in exactly one valid move area."""
        total, large_count, medium_count, placement_count = self._count_valid_moves_by_type(
            mouse_pos, valid_moves
        )

        # If point is in multiple valid move areas, return None
        if total != 1:
            return None

        # Return the one valid move containing this point
        for move in valid_moves:
            # Use the same radius as the green contour
            radius = (
                CIRCLE_SMALL_RADIUS + 4
                if not hasattr(move, "medium_circles") and not hasattr(move, "small_circles")
                else CIRCLE_MEDIUM_RADIUS + 4
            )

            if calculate_distance(mouse_pos, move.pos) <= radius:
                return move

        return None

    def _handle_rotation_click(self, mouse_pos):
        """Handle clicks during rotation phase."""
        valid_moves = self.system.move_handler.get_valid_moves()
        clicked_move = self._get_valid_move_at_point(mouse_pos, valid_moves)

        if clicked_move:
            # Toggle selection
            if self.selected_move == clicked_move:
                self.selected_move = None
                self.system.board_renderer.selected_move = None
            else:
                self.selected_move = clicked_move
                self.system.board_renderer.selected_move = clicked_move
            return True

        return False

    def _handle_placement_click(self, mouse_pos):
        """Handle clicks during placement phase."""
        valid_moves = self.system.move_handler.get_valid_moves()
        clicked_move = self._get_valid_move_at_point(mouse_pos, valid_moves)

        if clicked_move and clicked_move.color == GREY:
            # Toggle selection
            if self.selected_move == clicked_move:
                self.selected_move = None
                self.system.board_renderer.selected_move = None
            else:
                self.selected_move = clicked_move
                self.system.board_renderer.selected_move = clicked_move
            return True
        return False

    def _validate_large_circle_click(self, contained_circles, current_color):
        """Validate if a large circle click should trigger rotation."""
        for medium_circle in contained_circles:
            circles_inside = self.system.circle_manager.get_circles_inside(medium_circle)
            if any(circle.color == current_color for circle in circles_inside):
                return True
        return False

    def handle_events(self, event):
        if not self.system:
            return False

        self.original_ui.handle_events(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check for prev/next button clicks
            prev_button = next(
                (button for button in self.original_ui.buttons if button.text == "Prev"), None
            )
            next_button = next(
                (button for button in self.original_ui.buttons if button.text == "Next"), None
            )

            if prev_button and prev_button.rect.collidepoint(mouse_pos):
                return self._handle_prev_click()
            elif next_button and next_button.rect.collidepoint(mouse_pos):
                return self._handle_next_click()

            # Check for quit button click
            quit_button = next(
                (button for button in self.original_ui.buttons if button.text == "Quit"), None
            )
            if quit_button and quit_button.rect.collidepoint(mouse_pos):
                return self._handle_quit()

            # Check for resign button click
            resign_button = next(
                (button for button in self.original_ui.buttons if button.text == "Resign"), None
            )
            if resign_button and resign_button.rect.collidepoint(mouse_pos):
                return self._handle_resign()

            # Check for submit button click
            submit_button = next(
                (button for button in self.original_ui.buttons if button.text == "Submit"), None
            )

            # Check for cancel button click
            cancel_button = next(
                (button for button in self.original_ui.buttons if button.text == "Cancel"), None
            )

            if submit_button and submit_button.rect.collidepoint(mouse_pos):
                return self._handle_submit_click()
            elif cancel_button and cancel_button.rect.collidepoint(mouse_pos):
                self._clear_selection()
                return True

            # Check for winner screen button clicks if game is over
            if self.winner_buttons:
                replay_rect, menu_rect = self.winner_buttons
                if replay_rect.collidepoint(mouse_pos):
                    self.system.reset_game()
                    self.winner_buttons = None
                    print("Game reset")
                elif menu_rect.collidepoint(mouse_pos):
                    self.game_controller.game_mode = GameMode.MENU
                    self.winner_buttons = None
                    print("Returning to menu")
                return True

            # Handle regular game clicks if game is not over
            if not self.system.is_any_circle_animating() and not self.system.game_state.winner:
                return self._handle_game_click(event, mouse_pos)

        return False

    def _handle_resign(self):
        print("Resign button clicked")
        """Handle resign button click by setting the opposite player as winner"""
        if not self.system or self.system.game_state.winner:
            print("Game is already over")
            return False

        # Set the opposite player as winner
        current_turn = self.system.game_state.turn
        winner = "blue" if current_turn == "red" else "red"
        self.system.game_state.winner = winner
        print(f"{winner.capitalize()} wins!")
        return True

    def _clear_selection(self):
        """Helper method to clear the current selection"""
        self.selected_move = None
        self.system.board_renderer.selected_move = None

    def _handle_game_click(self, event, mouse_pos):
        """Handle regular gameplay clicks."""
        current_color = self.system.color_manager.player_color
        if current_color is not None:
            if (current_color == RED and self.system.game_state.turn != "red") or (
                current_color == BLUE and self.system.game_state.turn != "blue"
            ):
                return False

        if self.system.game_state.phase == PHASE_PLACEMENT:
            return self._handle_placement_click(mouse_pos)
        else:
            return self._handle_rotation_click(mouse_pos)

    def _handle_submit_click(self):
        """Handle submit button click"""
        if not self.selected_move:
            return False

        # Save the game state before making the move
        self.system.save_load_manager.save_game()

        if self.system.game_state.phase == PHASE_PLACEMENT:
            success = self.system.move_handler.make_placement_move(
                self.selected_move, self.system.game_state.turn
            )
        else:
            if hasattr(self.selected_move, "small_circles"):  # medium circle
                success = self.system.move_handler.make_rotation_move(
                    self.selected_move, self.system.game_state.turn
                )
            elif hasattr(self.selected_move, "medium_circles"):  # large circle
                contained_circles = get_completely_contained_circles(
                    self.selected_move.pos,
                    CIRCLE_LARGE_RADIUS,
                    self.system.medium_circles,
                    CIRCLE_MEDIUM_RADIUS,
                )
                current_color = RED if self.system.game_state.turn == "red" else BLUE
                if self._validate_large_circle_click(contained_circles, current_color):
                    success = self.system.move_handler.make_rotation_move(
                        self.selected_move, self.system.game_state.turn, contained_circles_only=True
                    )
                else:
                    success = False
            else:
                success = False

        if success:
            self.selected_move = None
            self.system.board_renderer.selected_move = None

        return success

    def _handle_quit(self):
        """Handle quit button click by returning to menu"""
        self.game_controller.game_mode = GameMode.MENU
        return True

    def _handle_prev_click(self):
        """Handle prev button click"""
        if not self.system.is_any_circle_animating():
            return self.system.save_load_manager.load_previous_state()
        return False

    def _handle_next_click(self):
        """Handle next button click"""
        if not self.system.is_any_circle_animating():
            return self.system.save_load_manager.load_next_state()
        return False
