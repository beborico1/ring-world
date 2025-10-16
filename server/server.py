import asyncio
import websockets
import json
import os
from dataclasses import dataclass
from typing import Dict, Set


@dataclass
class GameRoom:
    players: Set[websockets.WebSocketServerProtocol] = None
    player_colors: Dict[websockets.WebSocketServerProtocol, str] = None
    last_sequence: Dict[websockets.WebSocketServerProtocol, int] = None

    def __init__(self):
        self.players = set()
        self.player_colors = {}
        self.last_sequence = {}

class GameServer:
    def __init__(self):
        self.rooms: Dict[str, GameRoom] = {}

    async def register(self, websocket: websockets.WebSocketServerProtocol, room_code: str):
        if room_code not in self.rooms:
            self.rooms[room_code] = GameRoom()

        room = self.rooms[room_code]

        # Add player to room
        room.players.add(websocket)
        room.last_sequence[websocket] = 0  # Initialize sequence tracking

        # Assign color based on join order
        if len(room.players) == 1:
            room.player_colors[websocket] = "red"
            await websocket.send(
                json.dumps({"type": "wait", "message": "Waiting for opponent", "color": "red"})
            )
        elif len(room.players) == 2:
            room.player_colors[websocket] = "blue"
            # Notify both players that game can start
            for player in room.players:
                await player.send(
                    json.dumps(
                        {
                            "type": "start",
                            "message": "Game starting",
                            "color": room.player_colors[player],
                        }
                    )
                )
        else:
            await websocket.send(json.dumps({"type": "error", "message": "Room is full"}))
            return False

        return True

    async def unregister(self, websocket: websockets.WebSocketServerProtocol):
        for room_code, room in list(self.rooms.items()):
            if websocket in room.players:
                room.players.remove(websocket)
                room.player_colors.pop(websocket, None)
                room.last_sequence.pop(websocket, None)

                # Notify other player if they exist
                if room.players:
                    other_player = next(iter(room.players))
                    await other_player.send(
                        json.dumps(
                            {"type": "opponent_disconnected", "message": "Opponent disconnected"}
                        )
                    )

                # Remove empty rooms
                if not room.players:
                    del self.rooms[room_code]
                break

    async def broadcast_move(self, websocket: websockets.WebSocketServerProtocol, message: dict):
        """Handle move broadcasting with proper message structure."""
        try:
            # Find the room containing the player
            for room in self.rooms.values():
                if websocket in room.players:
                    # Update sequence number for the sender
                    sequence = message.get("sequence", room.last_sequence[websocket] + 1)
                    room.last_sequence[websocket] = sequence

                    # Get the move data
                    move_data = message.get("data", {})

                    # Create the outgoing message
                    outgoing_message = {
                        "type": "move",
                        "data": move_data,
                        "sequence": sequence,
                        "color": room.player_colors[websocket]
                    }

                    # Send the move to the other player
                    for player in room.players:
                        if player != websocket:
                            try:
                                await player.send(json.dumps(outgoing_message))
                            except Exception as e:
                                print(f"Error sending move to player: {e}")
                    break

        except Exception as e:
            print(f"Error broadcasting move: {e}")

    async def handle_connection(self, websocket: websockets.WebSocketServerProtocol):
        try:
            # Wait for messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    message_type = data.get("type")

                    if message_type == "join":
                        success = await self.register(websocket, data["room_code"])
                        if not success:
                            break

                    elif message_type == "move":
                        # The move message is already properly structured, just broadcast it
                        await self.broadcast_move(websocket, data)

                except json.JSONDecodeError:
                    print("Error: Invalid JSON message received")
                except Exception as e:
                    print(f"Error handling message: {e}")

        except websockets.exceptions.ConnectionClosed:
            print("Client connection closed unexpectedly")
        finally:
            await self.unregister(websocket)

async def main():
    game_server = GameServer()

    # Get port from environment variable (Railway sets this automatically)
    port = int(os.getenv("PORT", "8765"))

    # Use 0.0.0.0 to listen on all available network interfaces
    async with websockets.serve(
        game_server.handle_connection, "0.0.0.0", port, ping_interval=None
    ):
        print(f"Server started on port {port}")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
