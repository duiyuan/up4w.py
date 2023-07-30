
from typing import Optional, Any
from up4w.request_manager import RequestManager

from .types import MessageText


class Message:
    def __init__(self, requester: RequestManager):
        self.requester = requester

    @property
    def provider(self):
        return self.requester.current_provider

    def enable_received_push(self, *, conversation: Optional[str], app: Optional[str]):
        return self.requester.make_request({
            "req": "msg.receive_push",
            "arg": {
                "conversation": conversation,
                "app": app
            }
        })

    def send_text(self, params: MessageText):
        return self.requester.make_request({
            "req": "msg.text",
            "arg": {
                **params,
                "content_type": 13
            }
        })
