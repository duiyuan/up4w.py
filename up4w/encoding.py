
from json import dumps, loads, encoder, decoder
from typing import Dict, Type, Optional, Any


class FriendlyJSON:
    """
    Friendly JSON serializer & deserializer

    When encoding or decoding fails, this class collects
    information on which fields failed, to show more
    helpful information in the raised error messages.
    """
    @staticmethod
    def encode(obj: Dict[Any, Any], cls: Any = None) -> str:
        try:
            encoded = dumps(obj, cls=cls)
            return encoded
        except TypeError as err:
            # if hasattr(obj, "items"):
            #     item_errors = "; ".join(self._json_mapping_errors(obj))
            #     raise TypeError(
            #         f"dict had unencodable value at keys: {{{item_errors}}}"
            #     )
            # elif is_list_like(obj):
            #     element_errors = "; ".join(self._json_list_errors(obj))
            #     raise TypeError(
            #         f"list had unencodable value at index: [{element_errors}]"
            #     )
            # else:
            raise err

    @staticmethod
    def decode(content: str) -> Dict[Any, Any]:
        try:
            decoded = loads(content)
            return decoded
        except decoder.JSONDecodeError as err:
            err_msg = f"Couldn't decode {content} because of {err}"
            raise decoder.JSONDecodeError(err_msg, err.doc, err.pos)
