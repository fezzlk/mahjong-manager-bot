# flake8: noqa: E999
from dataclasses import dataclass

from domains.user import User


@dataclass(frozen=True)
class Room:
    id: int
    room_id: str # -> line_room_id
    zoom_url: str
    mode: str
    users: [User]

# TODO: 値オブジェクト化
# line_room_id は LINE Room ID, Rから始まる

# zoom_url: url

# mode: Enum

# users: その LINE Room の参加者(不要)