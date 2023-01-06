from fastapi import APIRouter

import stores.game as game_store


router = APIRouter()


@router.get("/")
async def list_games():
    return game_store.list_games()
