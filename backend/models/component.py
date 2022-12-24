from typing import List
from enum import Enum

from pydantic import BaseModel


class ComponentType(Enum):
    CHAT = "chat"


class Component(BaseModel):
    id: str
    type: ComponentType


class ChatComponent(Component):
    lines: List[str] = []
