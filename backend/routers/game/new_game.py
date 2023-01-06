from fastapi import BackgroundTasks

from fastapi import APIRouter

from models.game import Game, NewGameParams
import stores
from use_cases.game_loop import game_loop


router = APIRouter()


@router.post("/", response_model=Game)
async def new_game(new_game_params: NewGameParams, background_tasks: BackgroundTasks):
    new_game = stores.game.create_game(new_game_params.name)

    background_tasks.add_task(game_loop, new_game.id)

    return new_game
