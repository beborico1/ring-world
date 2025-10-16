from queue import Queue
from typing import Optional, Dict, Any, Tuple

class QueueManager:
    def __init__(self):
        self.incoming_moves = Queue()
        self.outgoing_moves = Queue()
        self.message_queue = Queue()
        self.pending_moves = []

    def queue_move(self, move_data: Dict[str, Any]) -> None:
        """Queue a move to be sent."""
        self.outgoing_moves.put(move_data)

    def get_move(self) -> Optional[Dict[str, Any]]:
        """Get next available move."""
        try:
            if not self.incoming_moves.empty():
                return self.incoming_moves.get_nowait()
        except Exception:
            return None
        return None

    def get_message(self) -> Optional[Tuple]:
        """Get next available message."""
        try:
            if not self.message_queue.empty():
                return self.message_queue.get_nowait()
        except Exception:
            return None
        return None

    def add_pending_move(self, sequence: int, move_data: Dict[str, Any]) -> None:
        """Add move to pending moves list."""
        self.pending_moves.append((sequence, move_data))

    def remove_pending_move(self, sequence: int) -> None:
        """Remove move from pending moves list."""
        self.pending_moves = [move for move in self.pending_moves 
                            if move[0] != sequence]

    def get_pending_moves_count(self) -> int:
        """Get count of pending moves."""
        return len(self.pending_moves)
