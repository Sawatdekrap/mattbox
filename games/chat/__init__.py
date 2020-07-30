from games import BaseGame, BaseUser, BaseStage

import logging
logger = logging.getLogger('mattbox')


class ChatUser(BaseUser):
    def __str__(self):
        return self.alias or str(self.uuid)


class ChatStage(BaseStage):
    async def handle_event(self, event, game):
        logger.info(f"New event: {event.user}: {event.action}")
        await game.host.q.put(f"{event.user}: {event.action}")


class Chat(BaseGame):
    USER_CLASS = ChatUser

    def build_stage_list(self):
        return [ChatStage(timeout=None)]

    async def post_register_user(self, user):
        await self.host.q.put(f"User {user} has joined")

    async def pre_remove_user(self, user):
        await self.host.q.put(f"User {user} has left")           
