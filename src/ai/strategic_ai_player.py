from ..utils.settings import (
    RED,
    BLUE,
    PHASE_ROTATION,
    AI_THINKING_TIME,
    AIThinkingState,
    AI_MAX_THINK_TIME,
)
from .animation_controller import AnimationController
from .move_evaluator import MoveEvaluator
from .move_finder import MoveFinder
from .state_manager import StateManager
import pygame
import time


class StrategicAIPlayer:
    """Main AI player class that coordinates the game playing strategy"""

    def __init__(
        self, circle_system, color=BLUE, max_think_time=AI_MAX_THINK_TIME
    ):  # 5 seconds default max
        self.system = circle_system
        self.color = color
        self.player_color = "red" if color == RED else "blue"
        self.thinking_state = AIThinkingState()
        self.max_think_time = max_think_time  # Maximum time in seconds to think
        self.search_start_time = None
        self.best_move_so_far = None
        self.best_score_so_far = float("-inf")

        # Initialize components
        self.animation_controller = AnimationController(circle_system)
        self.state_manager = None
        self.move_evaluator = MoveEvaluator(circle_system, color)

    def initialize_save_manager(self, save_manager):
        """Initialize the save manager for state management"""
        self.state_manager = StateManager(save_manager)
        self.move_finder = MoveFinder(
            self.system,
            self.color,
            self.animation_controller,
            self.state_manager,
            self.move_evaluator,
        )

    def start_thinking(self, current_time: int, phase: str = "placement"):
        """Start the thinking timer"""
        self.thinking_state.thinking_start_time = current_time
        self.thinking_state.is_thinking = True
        self.thinking_state.phase = phase
        self.system.game_state.ai_thinking = True
        self.search_start_time = time.time()  # Track real time for move search
        self.best_move_so_far = None
        self.best_score_so_far = float("-inf")

    def is_thinking_complete(self, current_time: int) -> bool:
        """Check if thinking time has elapsed"""
        if not self.thinking_state.thinking_start_time:
            return True
        return (
            current_time - self.thinking_state.thinking_start_time >= AI_THINKING_TIME
            or self.should_stop_search()
        )

    def update_best_move(self, move, score):
        """Update the best move found so far if the score is better"""
        if score > self.best_score_so_far:
            self.best_score_so_far = score
            self.best_move_so_far = move

    def should_stop_search(self) -> bool:
        """Check if we should stop the move search based on max think time"""
        # Guard against None search_start_time
        if self.search_start_time is None:
            return False
        return time.time() - self.search_start_time >= self.max_think_time

    def finish_thinking(self):
        """Reset thinking state and ensure animations are reset"""
        self.thinking_state.thinking_start_time = None
        self.thinking_state.is_thinking = False
        self.system.game_state.ai_thinking = False
        self.search_start_time = None
        # Make sure animation durations are reset when thinking finishes
        self.animation_controller.reset_animation_duration()

    def make_move(self):
        """Make a move based on the current game state."""
        current_time = pygame.time.get_ticks()

        if (
            not self.system.is_any_circle_animating()
            and self.system.game_state.turn == self.player_color
        ):
            # Start a new search - initialize timing and best move tracking
            if not self.thinking_state.is_thinking and not self.thinking_state.next_move:
                self.state_manager.save_state()
                # Set quick animation for AI thinking
                self.animation_controller.set_animation_duration(0.0)
                self.search_start_time = time.time()
                self.best_move_so_far = None
                self.best_score_so_far = float("-inf")

                if self.system.game_state.phase == PHASE_ROTATION:
                    print("[AI] Rotation phase - evaluating rotation moves only")
                    best_rotation = self.move_finder.find_best_rotation_only(
                        update_best_move_callback=self.update_best_move,
                        should_stop_callback=self.should_stop_search,
                    )
                    # Use either the final best move or the best move found so far
                    final_move = best_rotation or self.best_move_so_far
                    if final_move:
                        self.thinking_state.next_move = (
                            None,
                            final_move[1] if isinstance(final_move, tuple) else final_move,
                        )
                        self.start_thinking(current_time, "rotation")
                else:
                    best_combination = self.move_finder.find_best_move(
                        update_best_move_callback=self.update_best_move,
                        should_stop_callback=self.should_stop_search,
                    )
                    # Use either the final best move or the best move found so far
                    final_move = best_combination or self.best_move_so_far
                    if final_move:
                        self.thinking_state.next_move = final_move
                        self.start_thinking(current_time, "placement")

            # If we're thinking and the time has elapsed
            elif self.thinking_state.is_thinking and self.is_thinking_complete(current_time):
                # Reset to normal animation duration before executing moves
                # self.animation_controller.reset_animation_duration()

                if self.thinking_state.next_move:
                    placement, rotation = self.thinking_state.next_move

                    if self.thinking_state.phase == "placement" and placement:
                        if self.system.move_handler.make_placement_move(
                            placement, self.player_color
                        ):
                            self.start_thinking(current_time, "rotation")
                            return True

                    elif self.thinking_state.phase == "rotation" and rotation:
                        if hasattr(rotation, "medium_circles"):  # If it's a medium circle
                            if self.system.move_handler.make_rotation_move(
                                rotation, self.player_color, contained_circles_only=True
                            ):
                                self.thinking_state.next_move = None
                                self.finish_thinking()  # Add this line
                                return True
                        else:  # Regular medium circle rotation
                            if self.system.move_handler.make_rotation_move(
                                rotation, self.player_color
                            ):
                                self.thinking_state.next_move = None
                                self.finish_thinking()  # Add this line
                                return True

                self.thinking_state.next_move = None
                self.finish_thinking()  # Add this line
                print("[AI] No valid moves found!")

        return False
