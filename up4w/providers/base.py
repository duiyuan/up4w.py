
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
    def _process_request_data(data: Dict[Any, Any]):
        if data.get("inc") is None:
            data["inc"] = uuid4().hex
        return FriendlyJSON.encode(data)

    @staticmethod
    def _process_response_data(data: str):
        return FriendlyJSON.decode(data)

