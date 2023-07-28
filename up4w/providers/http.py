import requests
from up4w.providers.base import BaseProvider
from up4w.types import Up4wRes, Up4wReq


class HTTPProvider(BaseProvider):
    def __init__(self, *, endpoint: str, kwargs):
        self.endpoint = endpoint

    def make_request(self, request_data: Up4wReq):
        raise Exception("Not implement for now")

    def can_subscribe(self):
        return False

