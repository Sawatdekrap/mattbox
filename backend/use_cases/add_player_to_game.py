from typing import Optional

from constants.component import ComponentType
from models.player import Player
from components.chat import ChatComponent
from models.update import SetSceneUpdate, SceneUpdateDetails
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
    scene_details = SceneUpdateDetails(components=components)
    set_components_update = SetSceneUpdate(details=scene_details)
    await update_store.push_update_for_connection(
        game_id, connection_id, set_components_update
    )

    return player
