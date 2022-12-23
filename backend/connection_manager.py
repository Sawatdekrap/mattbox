from typing import Dict
from uuid import uuid1

from fastapi import WebSocket


class Connection:
    def __init__(self, ws: WebSocket, game_id: str) -> None:
        self.id = str(uuid1())
        self.ws = ws
        self.game_id = game_id


class ConnectionManager:
    def __init__(self) -> None:
        self.connections: Dict[str, Connection] = {}

    async def connect(self, ws: WebSocket, game_id: str) -> Connection:
        await ws.accept()

        new_connection = Connection(ws, game_id)
        self.connections[new_connection.id] = new_connection

        return new_connection

    def remove(self, connection_id: str) -> None:
        self.connections.pop(connection_id, None)
