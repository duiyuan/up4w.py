from typing import Optional, TypeVar, Callable
from re import match


from up4w.providers.ws import WSProvider
from up4w.providers.http import HTTPProvider
from up4w.providers.base import BaseProvider
from up4w.types import Up4wRes, Up4wReq
from up4w.exception import BadParameters, ProviderError

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
            raise ProviderError(f"No matched provider for endpoint: {self.endpoint}")

    def can_subscribe(self) -> bool:
        return self.__provider.can_subscribe()

    def make_request(self, req: str, arg: T = None) -> Up4wRes[K]:
        if not isinstance(req, str):
            raise BadParameters(f"parameter `req` need be string, got {req}")
        return self.current_provider.make_request({
            "req": req,
            "arg": arg,
            "inc": None
        })

    def receive_message(self, callback: Callable):
        if not self.can_subscribe():
            raise ProviderError("The provider does not support subscription")
        self.current_provider.receive_message(callback)




