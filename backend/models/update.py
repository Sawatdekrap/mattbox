from typing import List, Union

from pydantic import BaseModel

from constants.update import UpdateType, UpdateDestination
from components import Component, ComponentUpdate


class UpdateBase(BaseModel):
    type: UpdateType
    destination: UpdateDestination


class SceneUpdateDetails(BaseModel):
    components: List[Component]


class SetSceneUpdate(UpdateBase):
    type = UpdateType.SET_SCENE
    destination = UpdateDestination.CLIENT
    details: SceneUpdateDetails


class ComponentUpdateDetails(BaseModel):
    component_id: str
    component_update: ComponentUpdate


class UpdateComponentUpdate(UpdateBase):
    type = UpdateType.UPDATE_COMPONENT
    details: ComponentUpdateDetails


Update = Union[SetSceneUpdate, UpdateComponentUpdate]
