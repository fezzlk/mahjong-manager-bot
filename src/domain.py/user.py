# flake8: noqa: E999
from dataclasses import dataclass

from domain.match import Match
from domain.room import Room


@dataclass(frozen=True)
class User:
    id: int
    name: str
    user_id: str
    zoom_id: str
    mode: str
    jantama_name: str
    matches: [Match]
    rooms: [Room]
