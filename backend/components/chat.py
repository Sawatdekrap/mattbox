from enum import StrEnum
from typing import List, Union

from models.component import ComponentBase, ComponentUpdateBase


class ChatComponent(ComponentBase):
    lines: List[str] = []


class ChatUpdateTypes(StrEnum):
    NEW_LINE = "newline"
    CLEAR = "clear"
    SUBMIT = "submit"


class ChatUpdateBase(ComponentUpdateBase):
    type: ChatUpdateTypes


class ChatNewLine(ChatUpdateBase):
    type = ChatUpdateTypes.NEW_LINE
    line: str


class ChatClear(ChatUpdateBase):
    type = ChatUpdateTypes.CLEAR


class ChatSubmit(ChatUpdateBase):
    type = ChatUpdateTypes.SUBMIT
    line: str


ChatUpdate = Union[ChatNewLine, ChatClear, ChatSubmit]
