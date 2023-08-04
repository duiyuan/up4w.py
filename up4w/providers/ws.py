import asyncio
import time
import websockets

from typing import Type, Callable, Dict
from up4w.encoding import FriendlyJSON
from types import TracebackType
from threading import Thread
from up4w.providers.base import BaseProvider
from uuid import uuid4
from up4w.types import Up4wRes, Up4wReq


def start_event_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()
    loop.close()


def get_thread_loop(name: str) -> asyncio.AbstractEventLoop:
    new_loop = asyncio.new_event_loop()
    thread = Thread(target=start_event_loop, name=name, args=(new_loop,), daemon=True)
    thread.start()
    return new_loop


class PersistentConnection:
    def __init__(self, endpoint: str, kwargs) -> None:
        self.ws: websockets.WebSocketClientProtocol = None
        self.endpoint = endpoint
        self.kwargs = kwargs

    async def __aenter__(self):
        if self.ws is None:
            self.ws = await websockets.connect(uri=self.endpoint, **self.kwargs)
        return self.ws

    async def __aexit__(self, exec_type: Type[BaseException], exec_val: BaseException,  exec_traceback: TracebackType):
        if exec_val is not None:
            try:
                await self.ws.close()
            except websockets.ConnectionClosed:
                pass
            finally:
                self.ws = None


class WSProvider(BaseProvider):
    _loop: asyncio.AbstractEventLoop = None

    def __init__(self, *, endpoint: str, timeout: int = None, kwargs):
        self.endpoint = endpoint
        self.timeout = timeout
        self.kwargs = kwargs or {}
        self.cached: Dict[str, str] = {}
        self.waiters: Dict[str, asyncio.Future] = {}
        self.process_message_callback = None

        if not WSProvider._loop:
            WSProvider._loop = get_thread_loop("loop_for_request")

        self.conn = PersistentConnection(self.endpoint, self.kwargs)

        asyncio.run_coroutine_threadsafe(
            self.process_message(),
            WSProvider._loop
        )
        # Sleep for 1 second for the eventloop is ready in specified thread
        # asyncio.run_coroutine_threadsafe didn't guarantee that
        time.sleep(1)

        super().__init__()

    def receive_message(self, callback: Callable):
        self.process_message_callback = callback

    async def process_message(self):
        try:
            async with self.conn as conn:
                async for message in conn:
                    callback = self.process_message_callback
                    data = FriendlyJSON.decode(message)
                    uid = data.get("inc")
                    if uid:
                        self.cached[uid] = message
                        if self.waiters.get(uid):
                            self.waiters[uid].set_result(message)
                            del self.waiters[uid]
                    elif callback:
                        callback(message)
        except websockets.ConnectionClosed:
            pass

    def make_request(self, request_data: Up4wReq):
        future = asyncio.run_coroutine_threadsafe(
            self.coroutine_make_request(request_data),
            WSProvider._loop
        )
        data = future.result()
        return data

    async def coroutine_make_request(self, request_data: Up4wReq) -> Up4wRes:
        if not request_data.get("inc"):
            request_data["inc"] = self.make_uuid()

        data = FriendlyJSON.encode(request_data)
        async with self.conn as conn:
            await asyncio.wait_for(
                conn.send(data),
                self.timeout
            )
        future = asyncio.Future()
        self.waiters[request_data["inc"]] = future
        # await asyncio.sleep(0)
        await future
        result = future.result()
        return self._process_response_data(result)

    def can_subscribe(self) -> bool:
        return True


