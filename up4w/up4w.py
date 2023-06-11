
from core import Core
from service import UP4wServer


class UP4W:
    def __init__(self):
        self.requester = self.__make_requester()
        self.core = Core(self.requester)

    def get_ver(self):
        return self.core.get_version()

    @staticmethod
    def __make_requester():
        return 1
