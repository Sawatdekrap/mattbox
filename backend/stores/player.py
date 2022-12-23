from collections import defaultdict
from typing import Dict, Optional, List
from uuid import uuid1

from models.player import Player


PlayerDict = Dict[str, Player]
GAME_PLAYERS: Dict[str, PlayerDict] = defaultdict(dict)


def add_player_for_connection(
    game_id: str, connection_id: str, alias: Optional[str] = None
) -> Player:
    new_player_id = str(uuid1())
    new_player = Player(
        id=new_player_id, connection_id=connection_id, alias=alias or new_player_id
    )

    game_players_dict = GAME_PLAYERS[game_id]
    game_players_dict[new_player.id] = new_player

    return new_player


def get_players_for_game(game_id: str) -> List[Player]:
    game_players_dict = GAME_PLAYERS[game_id]
    players = list(game_players_dict.values())

    return players


def remove_player_for_connection(game_id: str, connection_id: str) -> None:
    game_players_dict = GAME_PLAYERS[game_id]
    matching_players = [
        player
        for player in game_players_dict.values()
        if player.connection_id == connection_id
    ]
    for player in matching_players:
        player.connection_id = None
