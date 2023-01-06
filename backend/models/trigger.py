from pydantic import BaseModel

from constants.update import UpdateType


class Trigger(BaseModel):
    id: str
    update_type: UpdateType


class ComponentTrigger(Trigger):
    data: str
