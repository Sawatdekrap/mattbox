from asyncio import Queue
from collections import deque, defaultdict
from typing import Dict, List

from models.update import Update, UpdateDestination, UpdateType


UpdateQueue = Queue[Update]
ConnectionQueues = Dict[str, UpdateQueue]
GameConnectionQueues = Dict[str, ConnectionQueues]

INCOMING_UPDATES: GameConnectionQueues = defaultdict(lambda: defaultdict(Queue))
OUTGOING_UPDATES: GameConnectionQueues = defaultdict(lambda: defaultdict(Queue))


async def push_update_for_game(game_id: str, connection_id: str, data: str) -> None:
    game_connection_queues = INCOMING_UPDATES[game_id]
    connection_queue = game_connection_queues[connection_id]
    update = Update(
        destination=UpdateDestination.SERVER,
        type=UpdateType.COMPONENT,
        data=data,
    )

    await connection_queue.put(update)


async def push_update_for_connection(
    game_id: str, connection_id: str, update: Update
) -> None:
    game_connection_queues = OUTGOING_UPDATES[game_id]
    connection_queue = game_connection_queues[connection_id]

    await connection_queue.put(update)


def get_updates(game_id: str) -> List[Update]:
    all_updates = []

    game_connection_queues = INCOMING_UPDATES[game_id]
    for connection_queue in game_connection_queues.values():
        while not connection_queue.empty():
            next_update = connection_queue.get_nowait()
            all_updates.append(next_update)

    all_updates.reverse()
    return all_updates


async def get_data(game_id: str, connection_id: str) -> str:
    game_connection_queues = OUTGOING_UPDATES[game_id]
    connection_queue = game_connection_queues[connection_id]

    update = await connection_queue.get()
    data = update.data

    return data
