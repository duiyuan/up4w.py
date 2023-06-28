import asyncio
import websockets


class WSProvider:
    def __init__(self, *, endpoint: str):
        self.endpoint = endpoint
        self.start()

    async def __connect(self):
        async with websockets.connect(self.endpoint) as ws:
            await ws.recv()

    def start(self):
        asyncio.run(self.__connect())

    @staticmethod
    def support_subscription():
        return True

    @staticmethod
    def on(event, payload):
        pass

    @staticmethod
    def emit(event, payload):
        pass

    @staticmethod
    def reset():
        pass
