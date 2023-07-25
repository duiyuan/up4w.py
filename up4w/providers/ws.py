import asyncio
from typing import Type
from types import TracebackType
import logging
import websockets



class PersistentWebsocket:
    def __init__(self, endpoint: str, kwargs) -> None:
        self.ws: websockets.WebSocketClientProtocol = None
        self.endpoint = endpoint
        self.kwargs = kwargs

    async def __aenter__(self):
        if self.ws is None:
            self.ws = await websockets.connect(ursi=self.endpoint, **self.kwargs)
        return self.ws

    async def __aexit__(self, exec_type: Type[BaseException], exec_val: BaseException,  exec_traceback: TracebackType):
        if exec_val is not None:
            try:
                self.ws.close()
            except Exception:
                pass
            self.ws = None


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
