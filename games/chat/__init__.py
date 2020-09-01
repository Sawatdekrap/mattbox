from games import BaseGame, BaseUser, BaseStage

import logging
logger = logging.getLogger('mattbox')


class ChatUser(BaseUser):
    def __str__(self):
        return self.alias or str(self.uuid)


class ChatStage(BaseStage):
    def handle_event(self, event, game):
        return True

    async def post_handle_event(self, event, game, handle_obj):
        if event.user is None:
            logger.info("tick")
        else:
            logger.info(f"New event: {event.user}: {event.action}")
            await game.host.q.put(f"{event.user}: {event.action}")

    def is_complete(self):
        return False


class Chat(BaseGame):
    USER_CLASS = ChatUser

    def build_stage_list(self):
        return [ChatStage()]

    async def post_register_user(self, user):
        await self.host.q.put(f"User {user} has joined")

    async def pre_remove_user(self, user):
        await self.host.q.put(f"User {user} has left")
