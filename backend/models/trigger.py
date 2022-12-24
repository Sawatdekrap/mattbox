from enum import Enum

from pydantic import BaseModel

from models.update import UpdateType


class Trigger(BaseModel):
    id: str
    update_type: UpdateType


class ComponentTrigger(Trigger):
    data: str
