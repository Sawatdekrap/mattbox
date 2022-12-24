from collections import defaultdict
from typing import Dict

from models.layout import Layout


PlayerLayouts = Dict[str, Layout]
GAME_LAYOUTS: Dict[str, PlayerLayouts] = defaultdict(dict)


def set_layout_for_player(game_id: str, player_id: str, layout: Layout) -> None:
    player_layouts = GAME_LAYOUTS[game_id]
    player_layouts[player_id] = layout


def get_layout_for_player(game_id: str, player_id: str) -> Layout:
    player_layouts = GAME_LAYOUTS[game_id]
    layout = player_layouts[player_id]

    return layout
