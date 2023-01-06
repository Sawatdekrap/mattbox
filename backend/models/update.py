from typing import Any, List

from pydantic import BaseModel

from constants.update import UpdateType, UpdateDestination
from models.component import Component


class Update(BaseModel):
    destination: UpdateDestination
    type: UpdateType


class SetComponentsUpdate(Update):
    destination = UpdateDestination.CLIENT
    type = UpdateType.SET_COMPONENTS
    components: List[Component]


class UpdateComponentUpdate(Update):
    type = UpdateType.UPDATE_COMPONENT
    component_id: str
    data: Any
