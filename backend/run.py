import asyncio

from server import Server
from game.echo import EchoGame

if __name__ == "__main__":
    echo_game = EchoGame()
    server = Server(echo_game)
    asyncio.run(server.start())
