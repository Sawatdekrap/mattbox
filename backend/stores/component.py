from collections import defaultdict
from typing import Dict, List

from models.component import Component


ComponentById = Dict[str, Component]
PlayerComponents = Dict[str, ComponentById]
GAME_COMPONENTS: Dict[str, PlayerComponents] = defaultdict(lambda: defaultdict(dict))


def set_components_for_player(
    game_id: str, player_id: str, components: List[Component]
) -> None:
    components_by_player = GAME_COMPONENTS[game_id]
    player_components = components_by_player[player_id]
    for component in components:
        player_components[component.id] = component


def get_components_for_player(game_id: str, player_id: str) -> List[Component]:
    components_by_player = GAME_COMPONENTS[game_id]
    player_components = components_by_player[player_id]
    components = [component for component in player_components.values()]

    return components
