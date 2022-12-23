from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UpdateDestination(Enum):
    CLIENT = "client"
    SERVER = "server"


class UpdateType(Enum):
    COMPONENT = "component"


class Update(BaseModel):
    destination: UpdateDestination
    type: UpdateType
    data: str
