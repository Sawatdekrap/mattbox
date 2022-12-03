from dataclasses import dataclass


@dataclass
class User:
    connection_id: str

    @property
    def id(self) -> str:
        return self.connection_id
