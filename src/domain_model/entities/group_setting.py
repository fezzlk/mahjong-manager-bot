from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from domain_model.constants import (
    CHIP_RATE_LIST,
    NUM_OF_PLAYERS_LIST,
    RANKING_PRIZE_LIST,
    RANKING_PRIZE_LIST_3,
    RANKING_PRIZE_LIST_4,
    RATE_LIST,
    ROUNDING_METHOD_LIST,
    RoundingMethod,
)

__all__ = [
    "CHIP_RATE_LIST",
    "DEFAULT_STARTING_POINTS_BY_PLAYERS",
    "NUM_OF_PLAYERS_LIST",
    "RANKING_PRIZE_LIST",
    "RANKING_PRIZE_LIST_3",
    "RANKING_PRIZE_LIST_4",
    "RATE_LIST",
    "RETURN_POINTS_MARGIN",
    "ROUNDING_METHOD_LIST",
    "EmbeddedGroupSettings",
    "GroupSetting",
    "RoundingMethod",
]

# 人数ごとに独立して持つ、持ち点・返し点のデフォルト値
DEFAULT_STARTING_POINTS_BY_PLAYERS = {3: 35000, 4: 25000}
RETURN_POINTS_MARGIN = 5000


@dataclass
class EmbeddedGroupSettings:
    """Group に embedded される設定(_id・line_group_id なし)

    順位点(ranking_prize)・持ち点(starting_points)は3人麻雀・4人麻雀で
    使う数値がまったく異なるため、num_of_players で切り替えても互いの
    設定値を失わないよう人数ごとに別フィールドで保持する。呼び出し側は
    従来どおり ranking_prize / starting_points / return_points プロパティを
    参照すればよい(現在の num_of_players に応じたほうを自動的に返す)。
    """

    rate: int = 0
    ranking_prize_4: List[int] = field(default=None)
    ranking_prize_3: List[int] = field(default=None)
    chip_rate: int = 0
    tobi_prize: int = 10
    num_of_players: int = 4
    starting_points_4: int = None
    starting_points_3: int = None
    rounding_method: int = RoundingMethod.go_san_roku
    unit: str = "pt"

    def __post_init__(self):  # noqa: D105
        if self.ranking_prize_4 is None:
            self.ranking_prize_4 = [20, 10, -10, -20]
        if self.ranking_prize_3 is None:
            self.ranking_prize_3 = [30, 0, -30]
        if self.starting_points_4 is None:
            self.starting_points_4 = DEFAULT_STARTING_POINTS_BY_PLAYERS[4]
        if self.starting_points_3 is None:
            self.starting_points_3 = DEFAULT_STARTING_POINTS_BY_PLAYERS[3]

    @property
    def ranking_prize(self) -> List[int]:
        """現在の num_of_players に対応する順位点。"""
        return self.ranking_prize_3 if self.num_of_players == 3 else self.ranking_prize_4

    @property
    def starting_points(self) -> int:
        """現在の num_of_players に対応する持ち点。"""
        return self.starting_points_3 if self.num_of_players == 3 else self.starting_points_4

    @property
    def return_points(self) -> int:
        """持ち点+5,000で算出する返し点。"""
        return self.starting_points + RETURN_POINTS_MARGIN

    def to_dict(self) -> dict:
        return {
            "rate": self.rate,
            "ranking_prize_4": self.ranking_prize_4,
            "ranking_prize_3": self.ranking_prize_3,
            "chip_rate": self.chip_rate,
            "tobi_prize": self.tobi_prize,
            "num_of_players": self.num_of_players,
            "starting_points_4": self.starting_points_4,
            "starting_points_3": self.starting_points_3,
            "rounding_method": self.rounding_method,
            "unit": self.unit,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "EmbeddedGroupSettings":
        # 旧スキーマ(人数非依存の単一 ranking_prize)からの読み替え。
        # 既存グループは実質すべて4人麻雀運用だったため ranking_prize_4 として引き継ぐ。
        legacy_ranking_prize = d.get("ranking_prize")
        return cls(
            rate=d.get("rate", 0),
            ranking_prize_4=d.get("ranking_prize_4", legacy_ranking_prize),
            ranking_prize_3=d.get("ranking_prize_3"),
            chip_rate=d.get("chip_rate", 0),
            tobi_prize=d.get("tobi_prize", 10),
            num_of_players=d.get("num_of_players", 4),
            starting_points_4=d.get("starting_points_4"),
            starting_points_3=d.get("starting_points_3"),
            rounding_method=d.get("rounding_method", RoundingMethod.go_san_roku),
            unit=d.get("unit", "pt"),
        )


@dataclass
class GroupSetting:
    """後方互換のため残す(migration 後に削除予定)"""

    line_group_id: str
    rate: int = 0
    ranking_prize: List[int] = field(default=None)
    chip_rate: int = 0
    tobi_prize: int = 10
    num_of_players: int = 4
    rounding_method: int = RoundingMethod.go_san_roku
    unit: str = "pt"
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
