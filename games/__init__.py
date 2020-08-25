import uuid
import asyncio
from enum import Enum
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
        self.disconnected = False


class BaseHost(BaseConnection):
    pass


class SystemAction(Enum):
    TICK = 1


class BaseEvent:
    def __init__(self, user, action, system=False):
        self.user = user
        self.action = action
        self.system = system


class BaseStage:
    def handle_event(self, event, game):
        pass

    async def post_handle_event(self, event, game, handle_obj):
        pass

    def setup(self, previous_stage):
        """Setup this stage based on the state of the previous one"""
        pass

    async def post_setup(self, setup_obj):
        """Accept setup_obj returned from setup"""
        pass

    def is_complete(self):
        raise NotImplementedError

    def teardown(self):
        pass

    async def post_teardown(self, teardown_obj):
        """Accept teardown_obj returned from teardown"""
        pass


def q_post(coro):
    asyncio.get_running_loop().create_task(coro)


class BaseGame:
    HOST_CLASS = BaseHost
    USER_CLASS = BaseUser
    EVENT_CLASS = BaseEvent
    TICK = 1

    def __init__(self, capacity=None):
        self.capacity = capacity
        self.event_q = asyncio.Queue()
        self.host = None
        self.users = set()

        self.stages: deque = deque(self.build_stage_list())
        self.current_stage = self.stages.popleft()
        self.current_stage.setup(None)

    def build_stage_list(self):
        """Return a list of stages that the game will run through"""
        raise NotImplementedError

    def is_full(self):
        return self.capacity is not None and len(self.users) >= self.capacity

    def register_host(self):
        host = self.HOST_CLASS()
        self.host = host

        return host

    async def post_register_host(self):
        pass

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
        self.users.remove(user)

    async def tick(self):
        while True:
            await asyncio.sleep(self.TICK)
            await self.add_event(None, SystemAction.TICK, system=True)

    async def add_event(self, user, message, system=False):
        await self.event_q.put(self.EVENT_CLASS(user, message, system))

    def cycle_stage(self):
        # Teardown the current stage
        teardown_obj = self.current_stage.teardown()
        q_post(self.current_stage.post_teardown(teardown_obj))

        # Empty stage if finished exit stage
        if self.current_stage is self.exit_stage:
            self.current_stage = None
            return

        # Cycle stage and setup
        previous_stage = self.current_stage
        if len(self.stages) > 0:
            self.current_stage = self.stages.popleft()
        else:
            self.current_stage = self.exit_stage
        setup_obj = self.current_stage.setup(previous_stage)
        q_post(self.current_stage.post_setup(setup_obj))

    async def start(self):
        q_post(self.tick())

        while True:
            # Handle the event
            event = await self.event_q.get()
            logger.info(f"Event in loop: {event}")
            handle_obj = self.current_stage.handle_event(event, self)

            # Create a post-task if something needs to happen
            if handle_obj is not None:
                q_post(self.current_stage.post_handle_event(
                    event, self, handle_obj
                ))

            # Cycle stage if we need to
            if self.current_stage.is_complete():
                self.cycle_stage()

            # End game if stages are complete
            if self.current_stage is None:
                break

        # TODO some game teardown
        return
