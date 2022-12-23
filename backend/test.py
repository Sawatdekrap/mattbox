import asyncio
import websockets
import requests


HOST = "localhost"
PORT = "8000"


def get_url(protocol: str, *path_args) -> str:
    path = "/".join(path_args)
    return f"{protocol}://{HOST}:{PORT}/{path}"


async def main():
    new_game_url = get_url("http", "games")
    r = requests.post(new_game_url, json={"name": "test"})
    game_id = r.json()["id"]

    connect_url = get_url("ws", "games", game_id)
    async with websockets.connect(connect_url) as ws:
        while True:
            message = input("< ").strip()

            if message == "exit":
                break

            if message:
                await ws.send(message)

            response = await ws.recv()
            print(f"> {response}")


if __name__ == "__main__":
    asyncio.run(main())
