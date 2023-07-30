
from typing import TypedDict, List, Optional, Any, Dict, Tuple, Dict
from up4w.request_manager import RequestManager
from up4w.types import Up4wReq, Up4wRes


class MRCConfig(TypedDict):
    msgs_dir: Optional[str]
    media_dir: Optional[str]
    default_swarm: Optional[str]
    flags: Optional[List[str]]


class DVSConfig(TypedDict):
    kv_dir: str
    flags: List[str]


class Up4wCoreInitReq(TypedDict):
    app_name: str
    mrc: MRCConfig
    dvs: DVSConfig
    hob: dict
    lsm: dict
    mlt: dict
    gdp: dict
    pbc: dict


class Up4wStatus(TypedDict):
    dht_nodes: List[int]
    initialized: bool
    internet: str
    modules: List[str]
    net_time: Tuple[int, int, bool, bool]
    swarms: Dict[str, str]


class Up4wCore:
    def __init__(self, requester: RequestManager):
        self.requester = requester

    def version(self) -> Up4wRes[str]:
        return self.requester.make_request({
            "req": "core.ver",
            "arg": None,
        })

    def initialize(self, params: Up4wCoreInitReq) -> Up4wRes[Dict[str, bool]]:
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

    def status(self) -> Up4wRes[Up4wStatus]:
        return self.requester.make_request({
            "req": "core.status",
            "arg": None
        })