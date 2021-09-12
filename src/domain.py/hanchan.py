# flake8: noqa: E999
from dataclasses import dataclass


@dataclass(frozen=True)
class Hanchan:
    id: int
    room_id: str
    raw_scores: str
    converted_scores: str
    match_id: int
    status: int
