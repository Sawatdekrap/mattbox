import uuid
import asyncio
import websockets
from collections import deque

import logging
logger = logging.getLogger('mattbox')


class BaseConnection:
    def __init__(self):
        self.uuid = uuid.uuid1()
        self.q = asyncio.Queue()


class BaseUser(BaseConnection):
    def __init__(self):
        super().__init__()
        self.alias = None


class BaseHost(BaseConnection):
    pass


class BaseEvent:
    def __init__(self, user, action):
        self.user = user
        self.action = action


class BaseStage:
    def __init__(self, timeout):
        self.timeout = timeout

    async def handle_event(self, event):
        raise NotImplementedError

    def setup(self, previous_stage):
        """Setup this stage based on the state of the previous one"""
        pass

    async def post_setup(self):
        pass

    def stage_complete(self):
        """For some other condition than the timeout"""
        return False

    async def teardown(self):
        pass


class BaseGame:
    HOST_CLASS = BaseHost
    USER_CLASS = BaseUser
    EVENT_CLASS = BaseEvent

    def __init__(self, capacity=None):
        self.capacity = capacity
        self.event_q = asyncio.Queue()
        self.host = None
        self.users = set()
        self.stages = deque(self.build_stage_list())
        self.current_stage = None

    def build_stage_list(self):
        """Return a list of stages that the game will run through"""
        raise NotImplementedError

    def is_full(self):
        return self.capacity is not None and len(users) >= self.capacity

    def register_host(self):
        host = self.HOST_CLASS()
        self.host = host

        return host

    def register_user(self):
        if self.is_full():
            return None

        user = self.USER_CLASS()
        self.users.add(user)

        return user

    async def post_register_user(self, user):
        pass

    async def pre_remove_user(self, user):
        pass

    def remove_user(self, user):
        pass

    async def cycle_stages(self):
        while len(self.stages) != 0:
            # Setup the next stage
            previous_stage = self.current_stage
            self.current_stage = self.stages.popleft()
            self.current_stage.setup(previous_stage)
            await self.current_stage.post_setup()

            # Wait until stage complete or timeout expired
            s = 0
            while not self.current_stage.stage_complete():
                if self.current_stage.timeout is not None and s > self.current_stage.timeout:
                    break
                s += 1
                await asyncio.sleep(1)

            await self.current_stage.teardown()

    async def add_event(self, user, message):
        await self.event_q.put(self.EVENT_CLASS(user, message))

    async def start(self):
        # TODO might need to change into non-async state change and async post-change
        while True:
            event = await self.event_q.get()
            await self.current_stage.handle_event(event, self)
