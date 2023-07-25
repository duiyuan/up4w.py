
from abc import ABC, abstractmethod


class Provider(ABC):
    @property
    def endpoint(self) -> str:
        pass

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def can_subscribe(self) -> bool:
        pass
   