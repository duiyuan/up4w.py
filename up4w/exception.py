from typing import Optional, Any, Dict, Union


class Up4wException(Exception):
    """
    Exception mixed inherited by all exceptions to UP4W.py
    It means that you can do like:
    try:
        # do your stuff
    except Up4wExcept:
        # deal with UP4W exception
    except:
        # deal with other exception
    """


class ProviderFailToCloseError(Up4wException):
    """
    Raise when fail to close connection
    """
    pass


class ProviderConnectionError(Up4wException):
    """
    Raised when unable to connect to UP4W provider
    """
    pass


class ProviderError(Up4wException):
    """
    Raised when unable create Provider
    """
    pass


class BadResponseFormat(Up4wException):
    """
    Raised when a response comes back in an unexpected format
    """
    pass


class BadParameters(Up4wException):
    """
    Raised when parameters do not match the function signature
    """
    def __init__(self, msg: str):
        message = f"Bad parameters: {msg}"
        super().__init__(message)


