
from typing import TypedDict, List, Optional, Any, Dict
from up4w.request_manager import RequestManager


class MRCConfig(TypedDict):
    msgs_dir: Optional[str]
    media_dir: Optional[str]
    default_swarm: Optional[str]
    flags: Optional[List[str]]


class DVSConfig(TypedDict):
    kv_dir: str
    flags: List[str]


class Up4wjsCoreInitReq(TypedDict):
    app_name: str
    mrc: MRCConfig
    dvs: DVSConfig
    hob: dict
    lsm: dict
    mlt: dict
    gdp: dict
    pbc: dict


class Up4wCore:
    def __init__(self, requester: RequestManager):
        self.requester = requester

    def version(self):
        return self.requester.make_request({
            "req": "core.ver",
            "arg": None,
        })

    def initialize(self, params: Up4wjsCoreInitReq):
        return self.requester.make_request({
            "req": "core.init",
            "arg": params,
        })

    def term(self):
        return self.requester.make_request({
            "req": "core.term",
            "arg": None
        })

    def shutdown(self):
        return self.requester.make_request({
            "req": "core.shutdown",
            "arg": None
        })

    def load_delayed(self):
        return self.requester.make_request({
            "req": "core.load_delayed",
            "arg": None
        })