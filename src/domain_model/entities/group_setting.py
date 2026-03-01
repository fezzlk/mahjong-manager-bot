from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from bson.objectid import ObjectId

from domain_model.constants import (
    CHIP_RATE_LIST,
    NUM_OF_PLAYERS_LIST,
    RANKING_PRIZE_LIST,
    RATE_LIST,
    ROUNDING_METHOD_LIST,
    RoundingMethod,
)

__all__ = [
    "GroupSetting",
    "RATE_LIST",
    "CHIP_RATE_LIST",
    "NUM_OF_PLAYERS_LIST",
    "RANKING_PRIZE_LIST",
    "ROUNDING_METHOD_LIST",
    "RoundingMethod",
]


@dataclass
class GroupSetting:
    line_group_id: str
    rate: int = 0
    ranking_prize: List[int] = field(default=None)
    chip_rate: int = 0
    tobi_prize: int = 10
    num_of_players: int = 4
    rounding_method: int = RoundingMethod.go_san_roku
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: ObjectId = field(default=None)

    def __post_init__(self):
        if self.ranking_prize is None:
            self.ranking_prize = [20, 10, -10, -20]
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
