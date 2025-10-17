import threading
import asyncio
from typing import Dict, Any, Optional
from .queue_manager import QueueManager
from ...utils.game_state import GameState
from .connection_manager import ConnectionManager
from ...utils.network.message_processor import MessageProcessor
from ...utils.network.message_sender import MessageSender
from ...utils.network.network_loop import NetworkLoop
from ...utils.network.logger import NetworkLogger
from ...utils.settings import GameMode


class GameNetworkManager:
    """Main class coordinating all network components with singleton pattern."""

    _instance = None
    _initialized = False
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(GameNetworkManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize all network components (only once)."""
        if not GameNetworkManager._initialized:
            with GameNetworkManager._lock:
                if not GameNetworkManager._initialized:
                    self.queue_manager = QueueManager()
                    self.game_state = GameState()
                    self.connection = ConnectionManager()
                    self.message_processor = MessageProcessor(
                        self.queue_manager.message_queue, self.queue_manager.incoming_moves
                    )
                    self.message_sender = MessageSender(
                        self.connection, self.game_state, self.queue_manager
                    )
                    self.network_loop = NetworkLoop(
                        self.connection,
                        self.game_state,
                        self.message_processor,
                        self.message_sender,
                        self.queue_manager,
                    )

                    # Start network thread
                    self.network_thread = threading.Thread(target=self._run_async_loop, daemon=True)
                    self.network_thread.start()

                    GameNetworkManager._initialized = True

    def handle_network_messages(self, game_mode, circle_system, player_color):
        """Handle incoming network messages."""
        if game_mode != GameMode.ONLINE:
            return None, None

        message = self.get_message()
        while message:
            message_type, data = message
            NetworkLogger.log(f"Handling message: {message_type} with data: {data}")

            if message_type in ["wait", "start"]:
                if data:
                    if circle_system:
                        circle_system.color_manager.set_player_color(data)

                    if message_type == "start":
                        self.game_state.match_found = True
                        self.connection.connected = True  # Ensure we mark as connected
                        NetworkLogger.log(f"Game starting with color: {data}")
                        return GameMode.ONLINE, data

            elif message_type == "opponent_disconnected":
                NetworkLogger.log("Opponent disconnected")

            message = self.get_message()

        return None, None

    def is_ready_for_moves(self) -> bool:
        """Check if the network is ready to send/receive moves."""
        ready = (
            self.connection.connected
            and self.game_state.match_found
            and not self.game_state.shutting_down
        )
        if not ready:
            NetworkLogger.log(
                f"Network not ready: connected={self.connection.connected}, "
                f"match_found={self.game_state.match_found}, "
                f"shutting_down={self.game_state.shutting_down}"
            )
        return ready

    def handle_online_moves(self, circle_system):
        """Handle sending and receiving moves in online mode."""
        if not self.is_ready_for_moves():
            return

        if circle_system.has_new_move():
            move_data = circle_system.get_move_data()
            self.send_move(move_data)

        opponent_move = self.receive_move()
        if opponent_move:
            print("Received move: ", opponent_move)
            pass

    def join_room(self, room_code: str) -> None:
        """Join a game room."""
        self.game_state.join_room(room_code)
        NetworkLogger.log(f"Joining room: {room_code}")

    def check_match_status(self) -> Optional[str]:
        """Check if a match has been found."""
        return self.game_state.check_match_status()

    def send_move(self, move_data: Dict[str, Any]) -> None:
        """Send a move to the opponent."""
        if self.connection.connected and self.game_state.match_found:
            NetworkLogger.log(f"Queueing move: {move_data}")
            self.queue_manager.queue_move(move_data)
        else:
            NetworkLogger.log("Cannot send move: not connected or match not started")

    def receive_move(self) -> Optional[Dict[str, Any]]:
        """Check for and return any received moves."""
        return self.queue_manager.get_move()

    def get_message(self) -> Optional[tuple]:
        """Get the next message from the message queue."""
        return self.queue_manager.get_message()

    def _run_async_loop(self) -> None:
        """Run the asyncio event loop in a separate thread."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.network_loop.run())

    def shutdown(self) -> None:
        """Cleanly shut down the network manager."""
        self.game_state.shutting_down = True
        # Don't call asyncio.run() here - it causes deadlock with the network thread
        # The websocket will be closed when the network thread detects shutting_down=True
        self.connection.connected = False
        self.game_state.match_found = False
