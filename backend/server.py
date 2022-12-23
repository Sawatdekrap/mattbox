import asyncio as aio
from typing import List

from fastapi import FastAPI, WebSocket, BackgroundTasks, WebSocketException, status

from models.game import Game, NewGameParams
from models.update import Update, UpdateDestination, UpdateType
import stores.game as game_store
import stores.update as update_store
import stores.player as player_store
from connection_manager import Connection, ConnectionManager


app = FastAPI()
connection_manager = ConnectionManager()


@app.get("/")
async def root():
    return {"message": "Success"}


@app.get("/games", response_model=List[Game])
async def games():
    return game_store.list_games()


@app.post("/games", response_model=Game)
async def new_game(new_game_params: NewGameParams, background_tasks: BackgroundTasks):
    new_game = game_store.create_game(new_game_params.name)

    background_tasks.add_task(game_loop, new_game.id)

    return new_game


async def game_loop(game_id: str) -> None:
    while True:
        game = game_store.get_game_by_id(game_id)
        incoming_updates = update_store.get_updates(game_id)

        # TODO do something with updates
        for update in incoming_updates:
            outgoing_update = Update(
                destination=UpdateDestination.CLIENT,
                type=UpdateType.COMPONENT,
                data=f"You said {update.data}",
            )
            players = player_store.get_players_for_game(game.id)
            for player in players:
                await update_store.push_update_for_connection(
                    game.id, player.connection_id, outgoing_update
                )

        await aio.sleep(game.tick)


async def handle_incoming(connection: Connection) -> None:
    while True:
        data = await connection.ws.receive_text()
        await update_store.push_update_for_game(connection.game_id, connection.id, data)


async def handle_outgoing(connection: Connection) -> None:
    while True:
        data = await update_store.get_data(connection.game_id, connection.id)
        await connection.ws.send_text(data)


@app.websocket("/games/{game_id}")
async def join_game(ws: WebSocket, game_id: str, background_tasks: BackgroundTasks):
    game = game_store.get_game_by_id(game_id)
    if game is None:
        raise WebSocketException(status.WS_1000_NORMAL_CLOSURE)

    connection = await connection_manager.connect(ws, game.id)
    player_store.add_player_for_connection(game.id, connection.id)

    _done, pending = await aio.wait(
        [
            aio.create_task(handle_incoming(connection)),
            aio.create_task(handle_outgoing(connection)),
        ],
        return_when=aio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()

    player_store.remove_player_for_connection(game.id, connection.id)
    connection_manager.remove(connection.id)
