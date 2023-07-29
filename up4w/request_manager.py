from typing import Optional, TypeVar
from re import match

from up4w.providers.ws import WSProvider
from up4w.providers.http import HTTPProvider
from up4w.providers.base import BaseProvider
from up4w.types import Up4wRes, Up4wReq

T = TypeVar("T")
K = TypeVar("K")


class RequestManager(BaseProvider):
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

    def handle_message_received(self):


    def receive_message(self):
        if self.can_subscribe():
            self.persistent_receive_message



