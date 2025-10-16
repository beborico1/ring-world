import json
from typing import Tuple
from queue import Queue

class MessageProcessor:
    def __init__(self, message_queue: Queue, incoming_moves: Queue):
        self.message_queue = message_queue
        self.incoming_moves = incoming_moves
        self.last_received_sequence = 0

    async def process_message(self, message_str: str, player_color: str, 
                            match_found: bool, logger) -> Tuple[bool, str]:
        """Process incoming messages with improved handling."""
        try:
            # Parse JSON string to dict
            message = json.loads(message_str) if isinstance(message_str, str) else message_str
            message_type = message.get("type")
            logger(f"Processing message of type: {message_type}")

            if message_type == "wait":
                if not match_found:
                    color = message.get("color")
                    logger(f"Waiting for opponent. You are {color}")
                    self.message_queue.put(("wait", color))
                    return match_found, color

            elif message_type == "start":
                color = message.get("color")
                logger(f"Game starting! You are {color}")
                self.message_queue.put(("start", color))
                return True, color

            elif message_type == "move":
                if "data" in message and "sequence" in message:
                    sequence = message["sequence"]
                    if sequence > self.last_received_sequence:
                        self.last_received_sequence = sequence
                        move_data = message["data"]
                        logger(f"Received move {sequence} from opponent: {move_data}")
                        self.incoming_moves.put(move_data)
                    else:
                        logger(f"Skipping duplicate or out-of-order move {sequence}")
                else:
                    logger(f"Invalid move message format: {message}")

            elif message_type == "opponent_disconnected":
                logger("Opponent disconnected")
                self.message_queue.put(("opponent_disconnected", None))
                return False, player_color

            return match_found, player_color

        except Exception as e:
            logger(f"Error processing message: {e}")
            logger(f"Message content: {message_str}")
            return match_found, player_color