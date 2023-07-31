# https://docs.python.org/zh-cn/3.10/library/typing.html?highlight=typing#module-typing
from typing import Any, Union, Callable, TypeVar, Generic, TypedDict, Optional

T = TypeVar("T")
K = TypeVar("K")


class Up4wReq(TypedDict):
    req: str
    arg: Optional[T]
    # inc: Optional[str]


class Up4wRes(TypedDict):
    rsp: str
    ret: K
    err: Optional[int]
    inc: Optional[str]
    fin: Optional[bool]


class AvailableEndpoints(TypedDict):
    http: str
    ws: str


class Up4wServiceRes(TypedDict):
    available_endpoints: AvailableEndpoints


class SwarmNodes(TypedDict):
    backward_peers: int
    default: bool
    forward_peers: int
