from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from bson.objectid import ObjectId

from domain_model.entities.group_setting import EmbeddedGroupSettings


class MatchStatus(Enum):
    open = "open"
    settled = "settled"
    # _sim専用の使い捨てサンドボックス。実対戦の一覧・最新対戦検索からは
    # 常に除外する(FEZ-66 Phase C)。
    sim = "sim"


@dataclass
class Match:
    line_group_id: str
    is_deleted: bool = False
    status: str = MatchStatus.open.value
    name: Optional[str] = None
    settings: Optional[EmbeddedGroupSettings] = None
    chip_scores: Dict[str, int] = field(default_factory=dict)
    chip_prices: Dict[str, int] = field(default_factory=dict)
    sum_scores: Dict[str, int] = field(default_factory=dict)
    sum_prices: Dict[str, int] = field(default_factory=dict)
    sum_prices_with_chip: Dict[str, int] = field(default_factory=dict)
    active_hanchan_id: ObjectId = field(default=None)
    original_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: ObjectId = field(default=None)

    def __post_init__(self):  # noqa: D105
        if self.chip_scores is None:
            self.chip_scores = {}
        if self.chip_prices is None:
            self.chip_prices = {}
        if self.sum_scores is None:
            self.sum_scores = {}
        if self.sum_prices is None:
            self.sum_prices = {}
        if self.sum_prices_with_chip is None:
            self.sum_prices_with_chip = {}
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
