import requests


class HTTPProvider:
    def __init__(self, *, endpoint: str):
        self.endpoint = endpoint
        self.start()

    async def __connect(self):
        pass

    def start(self):
        pass

    @staticmethod
    def support_subscription():
        return True

    @staticmethod
    def on(event, payload):
        pass

    @staticmethod
    def emit(event, payload):
        pass

    @staticmethod
    def reset():
        pass
