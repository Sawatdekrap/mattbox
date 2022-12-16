from __future__ import annotations

from enum import Enum
import json


class ActionType(Enum):
    GAME = "game"
    CONNECTION = "connection"


class Action:
    def __init__(self, action_type: ActionType, connection_id: str, data: str) -> None:
        self.type: ActionType = action_type
        self.connection_id = connection_id
        self.data = data

    @classmethod
    def from_data(cls, connection_id: str, data_string: str) -> Action:
        data_dict = json.loads(data_string)

        return Action(
            action_type=ActionType.GAME,
            connection_id=connection_id,
            data=data_dict,
        )

    def to_data(self) -> str:
        data_string = json.dumps(self.data)

        return data_string
