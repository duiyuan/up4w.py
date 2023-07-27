import asyncio
import json
import logging
import websockets

from up4w.types import Up4wRes, Up4wReq
from typing import Type
from types import TracebackType
from threading import Thread
from up4w.providers.base import BaseProvider


def start_event_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()
    loop.close()


def get_thread_loop() -> asyncio.AbstractEventLoop:
    new_loop = asyncio.new_event_loop()
    thread = Thread(target=start_event_loop, args=(new_loop,), daemon=True)
    thread.start()
    return new_loop


class PersistentConnection:
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


class WSProvider(BaseProvider):
    _loop: asyncio.AbstractEventLoop = get_thread_loop()

    def __init__(self, *, endpoint: str, timeout: int, kwargs):
        self.endpoint = endpoint
        self.timeout = timeout
        self.kwargs = kwargs

        if WSProvider._loop is None:
            WSProvider._loop = get_thread_loop()

        self.conn = PersistentConnection(self.endpoint, self.kwargs)
        super().__init__()

    def make_request(self, request_data: Up4wReq):
        future = asyncio.run_coroutine_threadsafe(
            self.coroutine_make_request(request_data),
            WSProvider._loop
        )
        return future.result()

    async def coroutine_make_request(self, request_data: Up4wReq) -> Up4wRes:
        async with self.conn as conn:
            await asyncio.wait_for(
                conn.send(request_data),
                self.timeout
            )
            resp = await asyncio.wait_for(
                conn.recv(),
                self.timeout
            )
            return json.loads(resp)


