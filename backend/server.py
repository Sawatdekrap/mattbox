import asyncio
from typing import Dict, List
from collections import deque

import websockets
from websockets.server import WebSocketServerProtocol

from connection import Connection
from game import Game
from action import Action, ActionType


class Server:
    def __init__(self, game: Game) -> None:
        self.game: Game = game
        self.connections: Dict[str, Connection] = {}
        self.action_q: asyncio.Queue[Action] = asyncio.Queue()

    async def start(self) -> None:
        actions_task = asyncio.create_task(self._handle_action_q())
        async with websockets.serve(self._on_new_connection, "", 8001):
            await actions_task

    async def _on_new_connection(self, websocket: WebSocketServerProtocol) -> None:
        new_connection = Connection(websocket, self.action_q)

        self.connections[new_connection.id] = new_connection
        self.game.add_user_for_connection_id(new_connection.id)
        try:
            _, pending = await asyncio.wait(
                [
                    asyncio.create_task(new_connection.recieve_incoming()),
                    asyncio.create_task(new_connection.send_outgoing()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                print(f"Cancelling task: '{task.get_name()}'")
                task.cancel()
        except Exception as e:
            print("Encountered exception")
        finally:
            self.game.remove_user_for_connection_id(new_connection.id)
            self.connections.pop(new_connection.id)

    async def _handle_action_q(self) -> None:
        while True:
            action = await self.action_q.get()
            pending_actions = deque([action])
            while pending_actions:
                next_action = pending_actions.popleft()
                if next_action.type == ActionType.GAME:
                    resulting_actions = self._handle_game_action(action)
                    pending_actions.extend(resulting_actions)
                elif next_action.type == ActionType.CONNECTION:
                    self._handle_connection_action(action)

    def _handle_game_action(self, action: Action) -> List[Action]:
        resulting_actions = self.game.on_action(action)

        return resulting_actions

    def _handle_connection_action(self, action: Action) -> None:
        connection = self.connections.get(action.connection_id)
        if connection is None:
            print(f"No connection with id {action.connection_id}")
            return

        connection.outgoing_q.put_nowait(action)
