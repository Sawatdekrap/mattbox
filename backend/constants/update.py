from enum import StrEnum


class UpdateDestination(StrEnum):
    CLIENT = "client"
    SERVER = "server"


class UpdateType(StrEnum):
    SET_COMPONENTS = "setcomponents"
    UPDATE_COMPONENT = "updatecomponent"
