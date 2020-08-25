import asyncio
import websockets

import logging
logger = logging.getLogger('mattbox')


FULL = 'full'


class Server:
    def __init__(self, host, port, game):
        self.host = host
        self.port = port
        self.game = game

    async def read_handler(self, websocket, path, user):
        # TODO add timeout for disconnects
        async for message in websocket:
            logger.debug(f"Incoming message ({user.uuid}): {message}")
            await self.game.add_event(user, message)

    async def write_handler(self, websocket, path, user):
        while True:
            message = await user.q.get()
            logger.debug(f"Outgoing message ({user.uuid}): {message}")
            await websocket.send(message)

    async def connection_handler(self, websocket, path):
        """Handle incoming connections"""
        logger.info("New connection...")
        if self.game.host is None:
            user = self.game.register_host()
            logger.info(f"New host: {user.uuid}")
        else:
            user = self.game.register_user()
            if user is None:
                await websocket.send(FULL)
                return
            await self.game.post_register_user(user)
            logger.info(f"New user: {user.uuid}")

        read_task = asyncio.create_task(
            self.read_handler(websocket, path, user)
        )
        write_task = asyncio.create_task(
            self.write_handler(websocket, path, user)
        )

        # Run both tasks until one exits, then tear down
        done, pending = await asyncio.wait(
            [read_task, write_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        for task in pending:
            task.cancel()

        # Handle the end of the user's connection
        if user == self.game.host:
            # Host has left - terminate the game
            # TODO
            pass
            logger.info(f"Host left: {user.uuid}")
        else:
            # Remove user from the game
            await self.game.pre_remove_user(user)
            self.game.remove_user(user)
            logger.info(f"User left: {user.uuid}")

    async def run(self):
        serve_task = websockets.serve(
            self.connection_handler, self.host, self.port
        )

        done, pending = await asyncio.wait([
            self.game.start(),
            serve_task
        ])
        for task in pending:
            task.cancel()
