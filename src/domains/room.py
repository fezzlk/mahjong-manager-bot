# flake8: noqa: E999
from enum import Enum
from dataclasses import dataclass


class RoomMode(Enum):
    wait = 'wait'
    input = 'input'


@dataclass()
class Room:
    _id: int
    line_room_id: str # unique
    zoom_url: str
    mode: RoomMode
    users: list

    def __init__(
        self,
        line_room_id: str,
        zoom_url: str,
        mode: str,
        users: list,
        _id = None,
    ):
        self._id = _id
        self.line_room_id = line_room_id
        self.zoom_url = zoom_url
        self.mode = mode
        self.users = users

# TODO: 値オブジェクト化
# line_room_id は LINE Room ID, Rから始まる

# zoom_url: url

# mode: Enum

# users: User[], その LINE Room の参加者(不要)