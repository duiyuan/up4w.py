from up4w.exception import BadParameters
from up4w.request_manager import RequestManager
from typing import TypedDict


class Up4wSwarmMsgs(TypedDict):
    epoch: int
    ttl: int
    subband: int
    media_size: int


class Up4wSwarmDKVS(TypedDict):
    value_size: int


class Up4wSwarm(TypedDict):
    address: str
    secret: str
    msgs: Up4wSwarmMsgs
    dvs: Up4wSwarmDKVS


class Swarm:
    def __init__(self, requester: RequestManager):
        self.requester = requester

    def join(self, swarm: Up4wSwarm):
        return self.requester.make_request("swarm.join", swarm)

    def leave(self, address: str):
        return self.requester.make_request("swarm.leave", address)
