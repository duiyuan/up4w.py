
from abc import ABC, abstractmethod
from uuid import uuid4
from typing import TypeVar, Generic, Dict, Any, Callable

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

    @staticmethod
    def make_uuid() -> str:
        return uuid4().hex

    @staticmethod
    def _process_request_data(data: Dict[Any, Any]):
        # if data.get("inc") is None:
        #     data["inc"] = uuid4().hex
        return FriendlyJSON.encode(data)

    @abstractmethod
    def persistent_receive_message(self, callback: Callable) -> None:
        pass
