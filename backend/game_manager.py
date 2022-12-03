import asyncio
from queue import Queue

from game.echo import EchoGame
from action import Action


class GameManager:
    def __init__(self, server_outgoing_queue: asyncio.Queue[str]) -> None:
        self.game = EchoGame()
        self.incoming: asyncio.Queue[str] = asyncio.Queue()
        self.server_outgoing_queue = server_outgoing_queue

    async def handle_actions(self) -> None:
        while True:
            data = await self.incoming.get()
            action = self.data_to_action(data)
            current_actions = Queue([action])
            while current_actions:
                next_action = current_actions.get_nowait()
                new_actions = self.game.on_action(next_action)
                for new_action in new_actions:
                    if new_action == "broadcast":
                        self.server_outgoing_queue.put_nowait(new_action)
                    else:
                        current_actions.put_nowait(new_action)

    def data_to_action(self, data: str) -> Action:
        return Action(str)

    def action_to_data(self, action: Action) -> str:
        return str(action)
