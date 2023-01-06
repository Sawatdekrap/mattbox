from typing import Optional

from constants.component import ComponentType
from constants.update import UpdateDestination, UpdateType
from models.player import Player
from models.component import ChatComponent
from models.update import SetComponentsUpdate
import stores.player as player_store
import stores.update as update_store
import stores.component as component_store


async def add_player_to_game(
    game_id: str, connection_id: str, alias: Optional[str] = None
) -> Player:
    player = player_store.add_player_for_connection(game_id, connection_id, alias)

    # TODO generic
    chat_component = ChatComponent(id="chat", type=ComponentType.CHAT)
    components = [chat_component]
    component_store.set_components_for_player(game_id, player.id, components)

    # TODO generic
    set_components_update = SetComponentsUpdate(components=components)
    await update_store.push_update_for_connection(
        game_id, connection_id, set_components_update
    )

    return player
