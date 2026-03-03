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
    "CHIP_RATE_LIST",
    "EmbeddedGroupSettings",
    "NUM_OF_PLAYERS_LIST",
    "RANKING_PRIZE_LIST",
    "RATE_LIST",
    "ROUNDING_METHOD_LIST",
    "GroupSetting",
    "RoundingMethod",
]


@dataclass
class EmbeddedGroupSettings:
    """Group に embedded される設定（_id・line_group_id なし）"""
    rate: int = 0
    ranking_prize: List[int] = field(default=None)
    chip_rate: int = 0
    tobi_prize: int = 10
    num_of_players: int = 4
    rounding_method: int = RoundingMethod.go_san_roku

    def __post_init__(self):  # noqa: D105
        if self.ranking_prize is None:
            self.ranking_prize = [20, 10, -10, -20]

    def to_dict(self) -> dict:
        return {
            "rate": self.rate,
            "ranking_prize": self.ranking_prize,
            "chip_rate": self.chip_rate,
            "tobi_prize": self.tobi_prize,
            "num_of_players": self.num_of_players,
            "rounding_method": self.rounding_method,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "EmbeddedGroupSettings":
        return cls(
            rate=d.get("rate", 0),
            ranking_prize=d.get("ranking_prize"),
            chip_rate=d.get("chip_rate", 0),
            tobi_prize=d.get("tobi_prize", 10),
            num_of_players=d.get("num_of_players", 4),
            rounding_method=d.get("rounding_method", RoundingMethod.go_san_roku),
        )


@dataclass
class GroupSetting:
    """後方互換のため残す（migration 後に削除予定）"""
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

    def __post_init__(self):  # noqa: D105
        if self.ranking_prize is None:
            self.ranking_prize = [20, 10, -10, -20]
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
