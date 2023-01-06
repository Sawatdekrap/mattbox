from enum import StrEnum


class UpdateDestination(StrEnum):
    CLIENT = "client"
    SERVER = "server"


class UpdateType(StrEnum):
    COMPONENT = "component"
    LAYOUT = "layout"
