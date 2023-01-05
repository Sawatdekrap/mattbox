from enum import StrEnum
from typing import Any

from pydantic import BaseModel

from models.layout import Layout


class UpdateDestination(StrEnum):
    CLIENT = "client"
    SERVER = "server"


class UpdateType(StrEnum):
    COMPONENT = "component"
    LAYOUT = "layout"


class Update(BaseModel):
    type: UpdateType
    destination: UpdateDestination


class LayoutUpdate(Update):
    type = UpdateType.LAYOUT
    layout: Layout


class ComponentUpdate(Update):
    type = UpdateType.COMPONENT
    component_id: str
    data: Any
