import asyncio
from websockets.server import WebSocketServerProtocol


class Connection:
    def __init__(
        self,
        websocket: WebSocketServerProtocol,
        server_incoming_queue: asyncio.Queue[str],
    ) -> None:
        self.websocket = websocket
        self.server_incoming_queue = server_incoming_queue
        self.outgoing_messages: asyncio.Queue[str] = asyncio.Queue()

    @property
    def id(self) -> str:
        return self.websocket.id

    async def send_outgoing(self) -> None:
        while True:
            item = await self.outgoing_messages.get()
            await self.websocket.send(item)

    async def recieve_incoming(self) -> None:
        while True:
            data = await self.websocket.recv()
            item = str(data)
            self.server_incoming_queue.put_nowait(item)
