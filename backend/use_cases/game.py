from typing import Optional

from models.player import Player
from models.layout import Layout
from models.component import ChatComponent, ComponentType
from models.update import UpdateDestination, UpdateType, LayoutUpdate
import stores.player as player_store
import stores.layout as layout_store
import stores.update as update_store


async def add_player_to_game(
    game_id: str, connection_id: str, alias: Optional[str] = None
) -> Player:
    player = player_store.add_player_for_connection(game_id, connection_id, alias)

    # TODO generic
    layout = Layout(game_id=game_id, player_id=player.id)
    chat_component = ChatComponent(id="chat", type=ComponentType.CHAT)
    layout.add_component(chat_component)
    layout_store.set_layout_for_player(game_id, player.id, layout)

    # TODO generic
    layout_update = LayoutUpdate(
        destination=UpdateDestination.CLIENT,
        type=UpdateType.LAYOUT,
        layout=layout,
    )
    await update_store.push_update_for_connection(game_id, connection_id, layout_update)

    return player
