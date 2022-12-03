from abc import ABC, abstractmethod
from typing import Dict

from ..user import User
from ..action import Action


class Game(ABC):
    def __init__(self) -> None:
        self.users: Dict[str, User] = {}

    def add_user_for_connection_id(self, connection_id: str) -> None:
        new_user = User(connection_id)
        self.users[new_user.id] = new_user

    def remove_user_for_connection_id(self, connection_id: str) -> None:
        matching_user_index = None
        for user_idx, user in enumerate(self.users.values()):
            if user.connection_id == connection_id:
                matching_user_index = user_idx
                break

        if matching_user_index is not None:
            self.users.pop(matching_user_index)

    @abstractmethod
    def on_action(self, action: Action) -> None:
        ...
