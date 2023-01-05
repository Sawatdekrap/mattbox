from typing import List
from enum import StrEnum

from pydantic import BaseModel


class ComponentType(StrEnum):
    CHAT = "chat"


class Component(BaseModel):
    id: str
    type: ComponentType


class ChatComponent(Component):
    lines: List[str] = []
