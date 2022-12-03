import asyncio
from typing import Dict

import websockets
from websockets.server import WebSocketServerProtocol

from connection import Connection
from game_manager import GameManager


class Server:
    def __init__(self) -> None:
        self.connections: Dict[str, Connection] = {}
        self.game_managers: Dict[str, GameManager] = {}
        self.server_incoming_queue: asyncio.Queue[str] = asyncio.Queue()
        self.server_outgoing_queue: asyncio.Queue[str] = asyncio.Queue()

    async def _on_new_connection(self, websocket: WebSocketServerProtocol) -> None:
        new_connection = Connection(websocket, self.server_incoming_queue)

        self.connections[new_connection.id] = new_connection
        game_manager = self._get_game_for_connection(new_connection)
        game_manager.game.add_user_for_connection_id(new_connection.id)
        try:
            _, pending = asyncio.wait(
                [
                    new_connection.recieve_incoming(),
                    new_connection.send_outgoing(),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
        finally:
            game_manager.game.remove_user_for_connection_id(new_connection.id)
            self.connections.pop(new_connection.id)

    async def start(self) -> None:
        with websockets.serve(self._on_new_connection, "", 8001):
            await asyncio.Future()

    def _get_game_manager_for_connection(self, connection: Connection) -> GameManager:
        """TODO this will need to be updated"""
        if not self.game_managers:
            game_manager = GameManager(self.server_outgoing_queue)
            gm_id = 1
            self.game_managers[gm_id] = game_manager
        else:
            gm_id = list(self.game_manager.keys())[0]
            game_manager = self.game_managers[gm_id]

        return game_manager
