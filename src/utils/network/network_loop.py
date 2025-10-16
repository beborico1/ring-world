import asyncio
import websockets
from ..settings import NETWORK_CONFIG
from .logger import NetworkLogger


class NetworkLoop:
    def __init__(self, connection, game_state, message_processor, message_sender, queue_manager):
        self.connection = connection
        self.game_state = game_state
        self.message_processor = message_processor
        self.message_sender = message_sender
        self.queue_manager = queue_manager
        self.logger = NetworkLogger()

    async def run(self) -> None:
        """Main network loop implementation."""
        while not self.game_state.shutting_down:
            try:
                if not self.connection.connected and self.game_state.room_code:
                    await self._handle_connection()
                await asyncio.sleep(1)
            except Exception as e:
                self.logger.log(f"Network loop error: {e}")
                await asyncio.sleep(5)

    async def _handle_connection(self) -> None:
        """Handle connection establishment and message processing."""
        self.logger.log(
            f"Attempting to connect (attempt {self.connection.reconnect_count + 1}"
            f"/{NETWORK_CONFIG['MAX_RECONNECT_ATTEMPTS']})"
        )

        try:
            websocket = await self.connection.connect(NETWORK_CONFIG["URL"])
            self.connection.websocket = websocket
            self.connection.connected = True
            self.connection.reconnect_count = 0

            await self.connection.send_join_message(
                self.game_state.room_code,
                self.game_state.player_color,
                self.game_state.match_found,
                self.game_state.last_received_sequence,
            )

            await self._process_messages(websocket)

        except websockets.exceptions.ConnectionClosed as e:
            self.logger.log(f"Connection closed with code {e.code}: {e.reason}")
            await self._handle_connection_closed()
        except Exception as e:
            self.logger.log(f"Connection error: {e}")
            await self._handle_connection_closed()

    async def _process_messages(self, websocket) -> None:
        """Process incoming and outgoing messages."""
        try:
            await asyncio.gather(
                self._handle_incoming_messages(websocket),
                self._handle_outgoing_messages(websocket),
                self._heartbeat(websocket),
            )
        except asyncio.CancelledError:
            self.logger.log("Network tasks cancelled")
        except Exception as e:
            self.logger.log(f"Error in message handling: {e}")
            raise

    async def _handle_incoming_messages(self, websocket) -> None:
        """Handle incoming WebSocket messages."""
        try:
            while not self.game_state.shutting_down:
                message = await websocket.recv()
                self.logger.log(f"Raw message received: {message}")
                match_found, player_color = await self.message_processor.process_message(
                    message,  # Pass the raw message string
                    self.game_state.player_color,
                    self.game_state.match_found,
                    self.logger.log,
                )
                self.game_state.update_match_status(match_found, player_color)
        except Exception as e:
            self.logger.log(f"Error handling incoming messages: {e}")
            raise

    async def _handle_outgoing_messages(self, websocket) -> None:
        """Handle outgoing messages."""
        try:
            while not self.game_state.shutting_down:
                if not self.queue_manager.outgoing_moves.empty():
                    move_data = self.queue_manager.outgoing_moves.get()
                    await self.message_sender.send_move_internal(websocket, move_data)
                await asyncio.sleep(0.01)
        except Exception as e:
            self.logger.log(f"Error handling outgoing messages: {e}")
            raise

    async def _heartbeat(self, websocket) -> None:
        """Maintain connection heartbeat."""
        while not self.game_state.shutting_down:
            try:
                await websocket.ping()
                await asyncio.sleep(NETWORK_CONFIG["HEARTBEAT_INTERVAL"])
            except Exception as e:
                self.logger.log(f"Heartbeat error: {e}")
                break

    async def _handle_connection_closed(self) -> None:
        """Handle connection closure and reconnection."""
        self._handle_disconnection()
        self.connection.reconnect_count += 1

        if self.connection.reconnect_count >= NETWORK_CONFIG["MAX_RECONNECT_ATTEMPTS"]:
            self.logger.log("Max reconnection attempts reached")
            self.game_state.shutting_down = True
            return

        delay = min(NETWORK_CONFIG["RECONNECT_DELAY"] * self.connection.reconnect_count, 30)
        self.logger.log(f"Waiting {delay} seconds before reconnecting...")
        await asyncio.sleep(delay)

        if self.queue_manager.pending_moves:
            self.logger.log(
                f"Have {self.queue_manager.get_pending_moves_count()} pending moves to retry"
            )

    def _handle_disconnection(self) -> None:
        """Clean up after disconnection."""
        if self.connection.connected:
            self.connection.connected = False
            self.connection.websocket = None
            if not self.game_state.shutting_down:
                self.queue_manager.message_queue.put(("disconnected", None))
