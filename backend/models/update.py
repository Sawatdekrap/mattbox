from typing import Any

from pydantic import BaseModel

from constants.update import UpdateType, UpdateDestination
from models.layout import Layout


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
