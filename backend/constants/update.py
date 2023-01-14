from enum import StrEnum


class UpdateDestination(StrEnum):
    CLIENT = "client"
    SERVER = "server"


class UpdateType(StrEnum):
    SET_SCENE = "setscene"
    UPDATE_COMPONENT = "updatecomponent"
