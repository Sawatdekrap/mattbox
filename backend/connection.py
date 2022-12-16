import asyncio
from websockets.server import WebSocketServerProtocol
from uuid import uuid1

from action import Action, ActionType


class Connection:
    def __init__(
        self,
        websocket: WebSocketServerProtocol,
        server_q: asyncio.Queue[Action],
    ) -> None:
        self.id = str(uuid1())
        self.websocket = websocket
        self.server_q = server_q
        self.outgoing_q: asyncio.Queue[Action] = asyncio.Queue()

    async def send_outgoing(self) -> None:
        while True:
            action = await self.outgoing_q.get()
            data = action.data
            await self.websocket.send(data)

    async def recieve_incoming(self) -> None:
        while True:
            data = await self.websocket.recv()
            print(f"Received: '{data}'")
            action = Action(
                action_type=ActionType.GAME, connection_id=self.id, data=data
            )
            await self.server_q.put(action)
