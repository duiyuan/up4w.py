
from abc import ABC, abstractmethod
from uuid import uuid4
from typing import TypeVar, Generic, Dict, Any, Callable, Optional

from up4w.types import Up4wReq, Up4wRes
from up4w.encoding import FriendlyJSON

T = TypeVar("T")


class BaseProvider(ABC, Generic[T]):
    # @property
    # @abstractmethod
    # def endpoint(self) -> str:
    #     pass

    @abstractmethod
    def make_request(self, request_data: Up4wReq) -> Up4wRes:
        pass

    @abstractmethod
    def can_subscribe(self) -> bool:
        pass

    @abstractmethod
    def receive_message(self, callback: Callable):
        pass

    @staticmethod
    def make_uuid() -> str:
        return uuid4().hex

    @staticmethod
    def _process_request_data(params):
        if params.get("inc") is None:
            params["inc"] = uuid4().hex

        # remove key if value is None in params
        for m, n in params.copy().items():
            if n is None:
                del params[m]

        # remove key if value is None in params.arg
        is_dict = isinstance(params.get("arg"), dict)
        if is_dict:
            copy = params["arg"].copy()
            for k, v in copy.items():
                if v is None:
                    del params["arg"][k]
        return FriendlyJSON.encode(params)

    @staticmethod
    def _process_response_data(data: str):
        return FriendlyJSON.decode(data)

