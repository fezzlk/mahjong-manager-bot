from dataclasses import dataclass

from domain.user import User


@dataclass(frozen=True)
class Room:
    id: int
    room_id: str
    zoom_url: str
    mode: Column
    users: [User]
