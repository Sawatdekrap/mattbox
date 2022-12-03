import asyncio
import websockets


async def main():
    async for websocket in websockets.connect("ws://localhost:8001"):
        try:
            message = input("> ")
            await websocket.send(message)
            data = await websocket.recv()
            print(f"< {data}")
        except websockets.ConnectionClosed:
            continue


if __name__ == "__main__":
    asyncio.run(main())
