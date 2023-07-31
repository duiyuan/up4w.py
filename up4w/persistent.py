from up4w.request_manager import RequestManager


class Persistent:
    def __init__(self, requester: RequestManager):
        self.requester = requester

    def set(self, *, key: str, slot: int, ttl: int = None, value: str, secret: str = None):
        return self.requester.make_request("netkv.set", {
            "key": key,
            "ttl": ttl,
            "slot": slot,
            "value": value,
            "secret": secret
        })

    def get(self, key: str):
        return self.requester.make_request("netkv.get", key)