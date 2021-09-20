# flake8: noqa: E999
from enum import Enum
from dataclasses import dataclass

class UserMode(Enum):
    wait = 'wait'


@dataclass()
class User:
    _id: int
    name: str
    line_user_id: str # unique
    zoom_url: str
    mode: UserMode
    jantama_name: str
    matches: list
    rooms: list

    def __init__(
        self,
        name: str,
        line_user_id: str,
        zoom_url: str,
        mode: UserMode,
        jantama_name: str,
        matches: list,
        _id: int = None,
    ):
        self._id = _id
        self.name = name
        self.line_user_id = line_user_id
        self.zoom_url = zoom_url
        self.mode = mode
        self.jantama_name = jantama_name
        self.matches = matches

# TODO: 値オブジェクト化
# name: LINE account name

# line_user_id は LINE Account の ID, Uから始まる

# zoom_url: url

# mode: Enum

# jantama_name は雀魂のアカウント名

# matches: Match[]
