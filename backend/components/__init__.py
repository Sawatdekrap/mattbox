from typing import Union

from .chat import ChatComponent, ChatUpdate

Component = Union[ChatComponent, None]

ComponentUpdate = Union[ChatUpdate, None]
