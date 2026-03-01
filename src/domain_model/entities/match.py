from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional

from bson.objectid import ObjectId


@dataclass
class Match:
    line_group_id: str
    is_deleted: bool = False
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

    def __post_init__(self):
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
