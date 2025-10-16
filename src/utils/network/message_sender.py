import asyncio
import websockets
from typing import Dict, Any
from .validators import validate_move_data
from .logger import NetworkLogger

class MessageSender:
    def __init__(self, connection, game_state, queue_manager):
        self.connection = connection
        self.game_state = game_state
        self.queue_manager = queue_manager
        self.logger = NetworkLogger()

    async def send_move_internal(self, websocket, move_data: Dict[str, Any]) -> None:
        """Send a move with validation and proper server format."""
        try:
            if not validate_move_data(move_data, self.logger.log):
                self.logger.log("Move validation failed, not sending")
                return

            self.game_state.send_sequence += 1
            
            try:
                await self.connection.send_move(
                    move_data, 
                    self.game_state.send_sequence, 
                    self.game_state.room_code, 
                    self.game_state.player_color
                )
                self.logger.log(f"Move sent successfully")
                
                self.queue_manager.remove_pending_move(self.game_state.send_sequence)
            except asyncio.TimeoutError:
                self.logger.log("Move send timeout, will retry on reconnection")
                return
            
        except websockets.exceptions.ConnectionClosed as e:
            self.logger.log(f"Connection closed while sending move: {e}")
            raise
        except Exception as e:
            self.logger.log(f"Error sending move: {e}")
            await asyncio.sleep(1)
