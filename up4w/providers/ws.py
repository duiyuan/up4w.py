import asyncio
import json
import logging
import websockets

from up4w.types import Up4wRes, Up4wReq
from typing import Type, Optional, TypedDict, TypeVar, Callable
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
            self.ws = await websockets.connect(uri=self.endpoint, **self.kwargs)
        return self.ws

    async def __aexit__(self, exec_type: Type[BaseException], exec_val: BaseException,  exec_traceback: TracebackType):
        if exec_val is not None:
            try:
                await self.ws.close()
            except websockets.ConnectionClosed as err:
                pass
            except Exception:
                pass
            finally:
                self.ws = None


class WSProvider(BaseProvider):
    _loop: asyncio.AbstractEventLoop = get_thread_loop()
    _message_loop: asyncio.AbstractEventLoop = get_thread_loop()

    def __init__(self, *, endpoint: str, timeout: int = None, kwargs):
        self.endpoint = endpoint
        self.timeout = timeout
        self.kwargs = kwargs or {}

        if WSProvider._loop is None:
            WSProvider._loop = get_thread_loop()

        if WSProvider._message_loop is None:
            WSProvider._message_loop = get_thread_loop()

        self.conn = PersistentConnection(self.endpoint, self.kwargs)

        super().__init__()
        # self.receive_message()

    def receive_message(self):
        loop = asyncio.get_running_loop()
        if loop and loop.is_running():
            task = loop.create_task(self.persistent_receive_message())
            task.add_done_callback(lambda t: print(f"print {t}"))
        else:
            asyncio.run(self.persistent_receive_message())

    async def persistent_receive_message(self, callback: Callable):
        async with self.conn as conn:
            async for message in conn:
                # resp = await asyncio.wait_for(
                #     conn.recv(),
                #     30
                # )
                # data = json.loads(resp)
                callback(message)
                print(f"persistent_receive_message received message, {message}")

    def make_request(self, request_data: Up4wReq):
        future = asyncio.run_coroutine_threadsafe(
            self.coroutine_make_request(request_data),
            WSProvider._loop
        )
        data = future.result()
        return data

    async def coroutine_make_request(self, request_data: Up4wReq) -> Up4wRes:
        request_data = self._process_request_data(request_data)
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

    def can_subscribe(self) -> bool:
        return True


