import asyncio

from constants.update import UpdateDestination, UpdateType
from models.update import UpdateComponentUpdate, ComponentUpdateDetails
from components.chat import ChatNewLine, ChatSubmit
import stores.game as game_store
import stores.player as player_store
import stores.update as update_store


async def game_loop(game_id: str) -> None:
    while True:
        game = game_store.get_game_by_id(game_id)
        incoming_updates = update_store.get_updates(game_id)

        # TODO do something with updates with triggers
        for update in incoming_updates:
            update_component_update: UpdateComponentUpdate = update
            component_update_details: ComponentUpdateDetails = (
                update_component_update.details
            )
            chat_update: ChatSubmit = component_update_details.component_update
            chat_new_line = ChatNewLine(line=f"You said: '{chat_update.line}'")
            update_details = ComponentUpdateDetails(
                component_id="chat",
                component_update=chat_new_line,
            )
            outgoing_update = UpdateComponentUpdate(
                destination=UpdateDestination.CLIENT,
                type=UpdateType.UPDATE_COMPONENT,
                details=update_details,
            )
            players = player_store.get_players_for_game(game.id)
            for player in players:
                await update_store.push_update_for_connection(
                    game.id, player.connection_id, outgoing_update
                )

        await asyncio.sleep(game.tick)
