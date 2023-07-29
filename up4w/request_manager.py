from typing import Optional, TypeVar, Callable
from re import match
import asyncio


from up4w.providers.ws import WSProvider
from up4w.providers.http import HTTPProvider
from up4w.providers.base import BaseProvider
from up4w.types import Up4wRes, Up4wReq

T = TypeVar("T")
K = TypeVar("K")


class RequestManager:
    __provider: BaseProvider = None

    @property
    def current_provider(self):
        return self.__provider

    def __init__(self, *, endpoint: str, kwargs):
        self.endpoint = endpoint
        self.kwargs = kwargs
        if match(r"https?://", self.endpoint):
            self.__provider = HTTPProvider(endpoint=self.endpoint, kwargs=self.kwargs)
        elif match(r"wss?://", self.endpoint):
            self.__provider = WSProvider(endpoint=self.endpoint, kwargs=self.kwargs)
        else:
            raise Exception(f"No matched provider for endpoint: {self.endpoint}")

    def can_subscribe(self) -> bool:
        return self.__provider.can_subscribe()

    def make_request(self, request_data: Up4wReq[T]) -> Up4wRes[K]:
        return self.current_provider.make_request(request_data)

    def receive_message(self, callback: Callable):
        if not self.can_subscribe():
            raise Exception("The provider does not support subscribe")

        async def schedule():
            if self.current_provider.persistent_receive_message is not None:
                await self.current_provider.persistent_receive_message(
                    callback=callback
                )
        loop = asyncio.get_running_loop()

        if loop and loop.is_running():
            task = loop.create_task(schedule())
            task.add_done_callback(lambda t: print(t))
        else:
            asyncio.run(schedule())




