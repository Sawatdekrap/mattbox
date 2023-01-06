import asyncio

from constants.update import UpdateDestination, UpdateType
from models.update import UpdateComponentUpdate
import stores


async def game_loop(game_id: str) -> None:
    while True:
        game = stores.game.get_game_by_id(game_id)
        incoming_updates = stores.update.get_updates(game_id)

        # TODO do something with updates with triggers
        for update in incoming_updates:
            outgoing_update = UpdateComponentUpdate(
                destination=UpdateDestination.CLIENT,
                type=UpdateType.UPDATE_COMPONENT,
                component_id="chat",
                data=f"You said {update.data}",
            )
            players = stores.player.get_players_for_game(game.id)
            for player in players:
                await stores.update.push_update_for_connection(
                    game.id, player.connection_id, outgoing_update
                )

        await asyncio.sleep(game.tick)
