

class Up4wBaseError(Exception):
    def __init__(self, msg, *reason):
        super.__init__(msg)
        self.msg = msg
        self.reason = reason
        self.code = None


class Up4wConnectionError(Up4wBaseError):
    def __init__(self, msg, *reason):
        super().__init__(msg, reason)
        self.code = None


