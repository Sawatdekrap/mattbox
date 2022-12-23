from pydantic import BaseModel


class Game(BaseModel):
    id: str
    name: str
    type: str
    tick: float


class NewGameParams(BaseModel):
    name: str
