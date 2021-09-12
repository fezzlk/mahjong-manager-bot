# flake8: noqa: E999
from dataclasses import dataclass

from domain.user import User


@dataclass(frozen=True)
class Room:
    id: int
    room_id: str
    zoom_url: str
    mode: str
    users: [User]
