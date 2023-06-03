import asyncio
import websockets


class Websocket:
    def __init__(self, *, endpoint):
        self.endpoint = endpoint
        self.start()

    async def __connect(self):
        async with websockets.connect(self.endpoint) as ws:
            await ws.recv()

    def start(self):
        asyncio.run(self.__connect())
