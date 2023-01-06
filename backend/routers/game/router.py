from fastapi import APIRouter

from .join_game import router as join_game_router
from .list_games import router as list_games_router
from .new_game import router as new_game_router


router = APIRouter(
    prefix="/games",
    tags=["games"],
)
router.include_router(list_games_router)
router.include_router(new_game_router)
router.include_router(join_game_router)
