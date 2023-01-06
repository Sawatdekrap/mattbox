import asyncio
from fastapi import APIRouter, WebSocket, WebSocketException, status
from typing import Optional

import stores.game as game_store
import stores.update as update_store
import stores.player as player_store
from use_cases.add_player_to_game import add_player_to_game
from connection_manager import Connection, ConnectionManager


router = APIRouter()


connection_manager = ConnectionManager()


async def handle_incoming(connection: Connection) -> None:
    while True:
        data = await connection.ws.receive_json()
        await update_store.push_update_for_game(connection.game_id, connection.id, data)


async def handle_outgoing(connection: Connection) -> None:
    while True:
        data = await update_store.get_data(connection.game_id, connection.id)
        await connection.ws.send_json(data)


@router.websocket("/{game_id}")
async def join_game(ws: WebSocket, game_id: str, alias: Optional[str] = None):
    game = game_store.get_game_by_id(game_id)
    if game is None:
        raise WebSocketException(status.WS_1000_NORMAL_CLOSURE)

    connection = await connection_manager.connect(ws, game.id)
    await add_player_to_game(game.id, connection.id, alias)

    _done, pending = await asyncio.wait(
        [
            asyncio.create_task(handle_incoming(connection)),
            asyncio.create_task(handle_outgoing(connection)),
        ],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()

    player_store.remove_player_for_connection(game.id, connection.id)
    connection_manager.remove(connection.id)
