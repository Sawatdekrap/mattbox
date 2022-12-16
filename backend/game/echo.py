from typing import List

from .game import Game
from action import Action, ActionType


class EchoGame(Game):
    def on_action(self, action: Action) -> List[Action]:
        echo_action = Action(
            action_type=ActionType.CONNECTION,
            connection_id=action.connection_id,
            data=action.data,
        )
        return [echo_action]
