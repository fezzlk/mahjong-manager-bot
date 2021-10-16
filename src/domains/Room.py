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

    def __init__(
        self,
        line_room_id: str,
        mode: str,
        zoom_url: str = None,
        _id = None,
    ):
        self._id = _id
        self.line_room_id = line_room_id
        self.mode = mode
        self.zoom_url = zoom_url

# TODO: 値オブジェクト化
# line_room_id は LINE Room ID または LINE Group ID, R or Gから始まる

# zoom_url: url

# mode: Enum

# users: User[], その LINE Room の参加者(不要)
