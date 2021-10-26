from enum import Enum
from dataclasses import dataclass


class UserMode(Enum):
    wait = 'wait'


@dataclass()
class User:
    _id: int
    name: str
    # line_user_id is unique
    line_user_id: str
    zoom_url: str
    mode: UserMode
    jantama_name: str
    matches: list
    groups: list

    def __init__(
        self,
        line_user_name: str,
        line_user_id: str,
        zoom_url: str,
        mode: UserMode,
        jantama_name: str,
        matches: list = [],
        groups: list = [],
        _id: int = None,
    ):
        self._id = _id
        self.line_user_name = line_user_name
        self.line_user_id = line_user_id
        self.zoom_url = zoom_url
        self.mode = mode
        self.jantama_name = jantama_name
        self.matches = matches
        self.groups = groups

# TODO: 値オブジェクト化
# line_user_name: LINE account name

# line_user_id は LINE Account の ID, Uから始まる

# zoom_url: url

# mode: Enum

# jantama_name は雀魂のアカウント名

# matches: Match[]
