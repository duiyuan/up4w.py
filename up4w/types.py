# https://docs.python.org/zh-cn/3.10/library/typing.html?highlight=typing#module-typing
from typing import Any, Union, Callable, TypeVar, Generic, TypedDict, Optional

T = TypeVar("T")
K = TypeVar("K")


class Up4wReq(TypedDict):
    req: str
    arg: Optional[T]
    # inc: Optional[str]


class Up4wRes(Generic[K]):
    def __init__(self, rsp: str,  ret: K,  err: Optional[int] = None, inc: Optional[str] = None, fin: Optional[bool] = None):
        self.rsp = rsp
        self.ret = ret
        self.err = err
        self.inc = inc
        self.fin = fin


class AvailableEndpoints(TypedDict):
    http: str
    ws: str


class Up4wServiceRes(TypedDict):
    available_endpoints: AvailableEndpoints
