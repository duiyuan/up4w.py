import time
import websockets
import asyncio
import json
import threading
from typing import Callable

clients = set()


async def set_interval(interval: int, func: Callable):
    async def run():
        msg = time.asctime()
        await func(msg)
        threading.Timer(interval, schedule).start()

    def schedule():
        asyncio.run(run())
    threading.Timer(interval, schedule).start()


async def echo(ws):
    clients.add(ws)
    try:
        async for message in ws:
            msg = json.loads(message)
            msg["feedback"] = time.asctime()
            await ws.send(json.dumps(msg))
    except websockets.ConnectionClosed:
        pass
    finally:
        clients.remove(ws)


async def broadcast(msg: str):
    try:
        print(f"try send message to client {msg}, {len(clients)}")
        for client in clients:
            data = json.dumps({
                "feedback": msg
            })
            print(f"send message to client {data}")
            await client.send(data)
    except websockets.ConnectionClosed:
        pass


async def main():
    async with websockets.serve(echo, "localhost", "8765"):
        await set_interval(5, broadcast)
        # run forever
        # while True:
        #     time.sleep(5)
        #     await broadcast(time.asctime())
        await asyncio.Future()

asyncio.run(main())
