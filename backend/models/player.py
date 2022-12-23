from typing import Optional

from pydantic import BaseModel


class Player(BaseModel):
    id: str
    connection_id: Optional[str]
    alias: str
