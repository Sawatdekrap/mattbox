from pydantic import BaseModel

from constants.component import ComponentType


class ComponentBase(BaseModel):
    id: str
    type: ComponentType


class ComponentUpdateBase(BaseModel):
    type: str
