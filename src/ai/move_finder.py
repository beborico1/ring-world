from ..utils.settings import RED, PHASE_ROTATION
from .neural_network import NeuralNetwork
import random
import numpy as np


class MoveFinder:
    """Finds and evaluates possible moves"""

    def __init__(self, circle_system, color, animation_controller, state_manager, move_evaluator):
        self.system = circle_system
        self.color = color
        self.animation_controller = animation_controller
        self.state_manager = state_manager
        self.move_evaluator = move_evaluator
        self.player_color = "red" if color == RED else "blue"
        self.neural_network = NeuralNetwork()
        self.neural_network.load_model()

    def find_best_rotation_only(self, update_best_move_callback=None, should_stop_callback=None):
        """Evaluate all valid rotation moves when no placement is possible"""
        valid_rotations = self.system.move_handler.get_valid_moves()
        random.shuffle(valid_rotations)

        print(f"[AI] Evaluating {len(valid_rotations)} possible rotation moves")

        best_rotation = None
        best_score = float("-inf")

        for rotation in valid_rotations:
            # Check if we should stop searching
            if should_stop_callback and should_stop_callback():
                break

            if self.system.move_handler.make_rotation_move(rotation, self.player_color):
                self.animation_controller.wait_for_animations()
                score = self.move_evaluator.evaluate_position()

                if score > best_score:
                    best_score = score
                    best_rotation = rotation
                    # Update the best move found so far
                    if update_best_move_callback:
                        update_best_move_callback((None, rotation), score)

            self.state_manager.load_state()
            self.animation_controller.wait_for_animations()

        print(f"[AI] Rotation analysis complete. Best score: {best_score}")
        return best_rotation

    def find_best_move(self, update_best_move_callback=None, should_stop_callback=None):
        """Evaluate all valid combinations of placement and rotation moves"""
        unvisited_placements = self.system.move_handler.get_valid_moves()
        small_circles = self.system.circle_manager.small_circles
        input_layer = []
        for small_circle in small_circles:
            if small_circle.color == self.color:
                input_layer.append(1)
            elif small_circle.color == [128, 128, 128]:
                input_layer.append(0)
            else:
                input_layer.append(-1)

        # as input has to be 272 nodes, we need to add 272 - len(small_circles) nodes
        added_nodes = 0
        for _ in range(272 - len(small_circles)):
            input_layer.append(0)
            added_nodes += 1

        print("added nodes: ", added_nodes)

        output_layer = self.neural_network.evaluate(
            input_layer
        )  # Output layer is a list of scores for each placement from 0 to 1, 1 being the best possible move to play

        dict_of_circle_scores = {}  # Key will be circle id, value will be score

        for i, score in enumerate(output_layer):
            if i < len(unvisited_placements):
                dict_of_circle_scores[unvisited_placements[i]] = score

        sorted_unvisited_placements = sorted(
            dict_of_circle_scores.items(), key=lambda x: x[1], reverse=True
        )

        unvisited_placements = [x[0] for x in sorted_unvisited_placements]

        print(
            "Best move placing on circle: ",
            unvisited_placements[0].id,
            ", with score: ",
            sorted_unvisited_placements[0][1],
        )

        if self.system.game_state.phase == PHASE_ROTATION:
            print("[AI] No valid placement moves available, switching to rotation phase")
            return None

        best_combination = None
        best_score = float("-inf")
        rewards = []
        prev_score = self.move_evaluator.evaluate_position()
        placement_rotations = {}

        while unvisited_placements:
            # Check if we should stop searching
            if should_stop_callback and should_stop_callback():
                print(f"[AI] Max think time reached, returning best move found so far:", best_score)
                break

            current_placement = unvisited_placements[0]

            if current_placement not in placement_rotations:
                if not self.system.move_handler.make_placement_move(
                    current_placement, self.player_color
                ):
                    unvisited_placements.remove(current_placement)
                    continue

                self.animation_controller.wait_for_animations()
                placement_rotations[current_placement] = (
                    self.system.move_handler.get_valid_moves().copy()
                )

                self.state_manager.load_state()
                self.animation_controller.wait_for_animations()

            if not placement_rotations[current_placement]:
                unvisited_placements.remove(current_placement)
                continue

            current_rotation = placement_rotations[current_placement][0]

            if self.system.move_handler.make_placement_move(current_placement, self.player_color):
                self.animation_controller.wait_for_animations()

                if self.system.move_handler.make_rotation_move(current_rotation, self.player_color):
                    self.animation_controller.wait_for_animations()
                    score = self.move_evaluator.evaluate_position()
                    # print(
                    #     "Score: ",
                    #     score,
                    #     "Prev score: ",
                    #     prev_score,
                    #     "Having place in circle with id: ",
                    #     current_placement.id,
                    #     "And rotation: ",
                    #     current_rotation.id,
                    # )
                    score_difference = score - prev_score
                    reward = self.neural_network.learn(input_layer, output_layer, score_difference)
                    rewards.append(reward)
                    if score > best_score:
                        best_score = score
                        best_combination = (current_placement, current_rotation)
                        # Update the best move found so far
                        if update_best_move_callback:
                            update_best_move_callback(best_combination, score)

            placement_rotations[current_placement].remove(current_rotation)

            self.state_manager.load_state()
            self.animation_controller.wait_for_animations()

        print(
            f"Sample of 3 rewards [min, median, max]: {[float(min(rewards)), float(np.median(rewards)), float(max(rewards))]}"
        )
        return best_combination
