from typing import Dict, List, Optional
from uuid import uuid1

from models.game import Game


GAMES: Dict[str, Game] = {}


def list_games() -> List[Game]:
    return list(GAMES.values())


def create_game(name: str) -> Game:
    game = Game(
        id=str(uuid1()),
        name=name,
        type="test",
        tick=1.0,
    )
    GAMES[game.id] = game

    return game


def get_game_by_id(game_id: str) -> Optional[Game]:
    game = GAMES.get(game_id)

    return game
