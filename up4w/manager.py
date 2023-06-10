from providers import http, ws
import re


class RequestManager:
    providers = {
        "http": http.HTTPProvider,
        "ws": ws.WSProvider
    }

    def __init__(self, *, endpoint):
        self.endpoint = endpoint
        self.subscriptions = dict()
        self.__current_provider = None

        self.set_provider()

    @property
    def current_provider(self):
        return self.__current_provider

    @current_provider.setter
    def current_provider(self, provider):
        self.__current_provider = provider

    def set_provider(self):
        if not isinstance(self.endpoint, str):
            raise Exception("Invalid endpoint")

        if self.endpoint.startswith("http://"):
            providers = self.providers["http"]
            self.current_provider = providers(endpoint=self.endpoint)
        elif re.match(b"wss?://", self.endpoint):
            providers = self.providers["ws"]
            self.current_provider = providers(endpoint=self.endpoint)
        else:
            raise Exception(f"Can't autodetect provider for {str(self.endpoint)}")

    @staticmethod
    def should_drop():
        return True

    def send(self):
        pass


