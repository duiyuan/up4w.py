
from typing import Optional, Callable
from up4w.request_manager import RequestManager

from .types import MessageText


class Message:
    def __init__(self, requester: RequestManager):
        self.requester = requester

    @property
    def provider(self):
        return self.requester.current_provider

    def enable_received_push(self, *, conversation: Optional[str] = None, app: Optional[str] = None):
        self.requester.make_request("msg.receive_push", {
            "conversation": conversation,
            "app": app
        })

    def send_text(self, params: MessageText):
        return self.requester.make_request("msg.text", {
            **params,
            "content_type": 13
        })

    def receive_message(self, callback: Callable, *, conversation: Optional[str] = None, app: Optional[str] = None):
        self.enable_received_push(conversation=conversation, app=app)
        self.requester.receive_message(callback=callback)

