import asyncio
import websockets


async def main():
    async for websocket in websockets.connect("ws://localhost:8001"):
        while True:
            try:
                message = input("> ")
                if message.strip() == "exit":
                    break
                await websocket.send(message)
                data = await websocket.recv()
                print(f"< {data}")
            except websockets.ConnectionClosed:
                break


if __name__ == "__main__":
    asyncio.run(main())
