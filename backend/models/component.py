from typing import List

from pydantic import BaseModel

from constants.component import ComponentType


class Component(BaseModel):
    id: str
    type: ComponentType


class ChatComponent(Component):
    lines: List[str] = []
