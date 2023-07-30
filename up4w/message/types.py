from typing import Optional,TypedDict, List, Any


class Message(TypedDict):
    swarm: str
    id: str
    timestamp: int
    sender: str
    app: int
    recipient: str
    action: int
    content: str
    content_type: int
    media: List[str]


class MessageText(TypedDict):
    swarm: Optional[str]
    recipient: str
    app: int
    action: int
    content: Any
    content_type: Optional[int]