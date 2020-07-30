import sys
import asyncio
from server import Server
from games.chat import Chat

import logging
logger = logging.getLogger('mattbox')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


async def main():
    game = Chat()
    server = Server('localhost', 8888, game)
    await server.run()


if __name__ == '__main__':
    asyncio.run(main())
