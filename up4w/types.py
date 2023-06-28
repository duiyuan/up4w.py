# https://docs.python.org/zh-cn/3.10/library/typing.html?highlight=typing#module-typing
from typing import Any, Union, Callable, TypeVar, Generic, TypedDict, Optional

T = TypeVar("T")
K = TypeVar("K")


class Up4wReq:
    def __init__(self, req: str, arg: Optional[T] = None, inc: Optional[str] = None):
        self.req = req
        self.arg = arg
        self.inc = inc


class Up4wRes:
    def __init__(self, rsp: str,  ret: K,  err: Optional[int] = None, inc: Optional[str] = None, fin: Optional[bool] = None):
        self.rsp = rsp
        self.ret = ret
        self.err = err
        self.inc = inc
        self.fin = fin
