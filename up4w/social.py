from up4w.exception import BadParameters
from up4w.request_manager import RequestManager
from typing import Optional, TypedDict
from up4w.exception import BadParameters


class Profile(TypedDict):
    name: Optional[str]
    gender: Optional[str]
    geolocation: Optional[int]
    greeting_secret: Optional[str]


class NewUser(Profile):
    pk: str


class Social:
    def __init__(self, requester: RequestManager):
        self.requester = requester

    def signin_with_seed(self, seed, *, name: str = None, gender: int = None,
                         geolocation: int = None, greeting_secret: str = None):
        return self.signin(seed=seed, name=name, gender=gender, geolocation=geolocation,
                           greeting_secret=greeting_secret)

    def signin(self, *, seed: str = None, mnemonic: str = None, name: str = None, gender: int = None,
               geolocation: int = None, greeting_secret: str = None):
        if seed is None and mnemonic is None:
            raise BadParameters("You should provide at least one of the two parameters, 'seed' and 'mnemonic")
        return self.requester.make_request("social.signin", {
            "name": name,
            "gender": gender,
            "geolocation": geolocation,
            "greeting_secret": greeting_secret
        })

    def signin_with_mnemonic(self, mnemonic: str, *, name: str = None, gender: int = None,
                             geolocation: int = None, greeting_secret: str = None):
        return self.signin(mnemonic=mnemonic, name=name, gender=gender, geolocation=geolocation,
                           greeting_secret=greeting_secret)

    def add_user(self, pk: str, *, name: str = None, gender: int = None,
                 geolocation: int = None, greeting_secret: str = None):
        if not pk:
            raise BadParameters("add_user: the parameter `pk` is mandatory and can't absent")

        return self.requester.make_request("social.add_user", {
            "pk": pk,
            "name": name,
            "gender": gender,
            "geolocation": geolocation,
            "greeting_secret": greeting_secret
        })

    def remove_user(self, pk: str):
        return self.requester.make_request("social.remove_user", pk)



