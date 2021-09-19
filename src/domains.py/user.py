# flake8: noqa: E999
from dataclasses import dataclass

from domains.match import Match
from domains.room import Room


@dataclass(frozen=True)
class User:
    id: int
    name: str
    user_id: str # -> line_user_id
    zoom_id: str # -> zoom_url 
    mode: str
    jantama_name: str
    matches: [Match]
    rooms: [Room]

# TODO: 値オブジェクト化
# name: LINE account name

# line_user_id は LINE Account の ID, Uから始まる

# zoom_url: url

# mode: Enum

# jantama_name は雀魂のアカウント名
