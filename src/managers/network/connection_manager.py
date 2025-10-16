"""WebSocket connection management."""

import json
import websockets
from typing import Dict, Any, Optional
from ...utils.settings import NETWORK_CONFIG, MESSAGE_TYPES


class ConnectionManager:
    def __init__(self, websocket: Optional[websockets.WebSocketClientProtocol] = None):
        self.websocket = websocket
        self.reconnect_count = 0
        self.connected = False

    async def connect(self, url: str) -> websockets.WebSocketClientProtocol:
        """Establish WebSocket connection."""
        return await websockets.connect(
            url,
            ping_interval=NETWORK_CONFIG["HEARTBEAT_INTERVAL"],
            ping_timeout=20,
            close_timeout=10,
        )

    async def send_join_message(
        self, room_code: str, color: str, match_found: bool, last_sequence: int
    ) -> None:
        """Send join message to server."""
        join_message = {
            "type": MESSAGE_TYPES["JOIN"],
            "room_code": room_code,
            "color": color,
            "reconnecting": bool(match_found),
            "last_sequence": last_sequence,
        }
        await self.websocket.send(json.dumps(join_message))

    async def send_move(
        self, move_data: Dict[str, Any], sequence: int, room_code: str, player_color: str
    ) -> None:
        """Send move to server."""
        normalized_position = [int(round(float(x))) for x in move_data["position"]]

        message = {
            "type": "move",
            "data": {
                "type": move_data["type"],
                "position": normalized_position,
                "color": player_color,
                "phase": move_data["phase"],
            },
            "room_code": room_code,
            "sequence": sequence,
        }

        await self.websocket.send(json.dumps(message))
