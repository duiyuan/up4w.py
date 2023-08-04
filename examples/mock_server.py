import time
import websockets
import asyncio
import json
import threading

clients = set()


async def set_interval(interval: int, func):
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
            msg["current_time"] = time.asctime()
            # send message back
            data = json.dumps(msg)
            await ws.send(json.dumps(msg))
            print(f"Server feedback {data}`")
    except websockets.ConnectionClosed:
        pass
    finally:
        clients.remove(ws)


async def broadcast(msg: str):
    try:
        print(f"Server check before broadcast, {len(clients)}")
        for client in clients:
            data = json.dumps({
                "current_time": msg
            })
            print(f"Server side broadcast message to client {msg}")
            await client.send(data)
    except websockets.ConnectionClosed:
        pass


async def main():
    async with websockets.serve(echo, "localhost", "9801"):
        print("websocket server wake up")
        # run forever, broadcast time to every client per 5 seconds
        await set_interval(5, broadcast)
        await asyncio.Future()

asyncio.run(main())
