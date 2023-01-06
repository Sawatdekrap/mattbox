from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.game.router import router as game_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_router)


@app.get("/")
async def root():
    return {"message": "Success"}
