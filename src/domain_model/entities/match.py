from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from bson.objectid import ObjectId

MATCH_STATUS = ["DISABLE", "ACTIVE", "ARCHIVE"]


@dataclass()
class Match:
    _id: ObjectId
    line_group_id: str
    status: int
    chip_scores: Dict[str, int]
    chip_prices: Dict[str, int]
    sum_scores: Dict[str, int]
    sum_prices: Dict[str, int]
    sum_prices_with_chip: Dict[str, int]
    active_hanchan_id: ObjectId
    created_at: datetime
    updated_at: datetime
    original_id: Optional[int]

    def __init__(
        self,
        line_group_id: str,
        status: int = 2,
        created_at: datetime = None,
        updated_at: datetime = None,
        chip_scores: Dict[str, int] = None,
        chip_prices: Dict[str, int] = None,
        active_hanchan_id: ObjectId = None,
        sum_scores: Dict[str, int] = None,
        sum_prices: Dict[str, int] = None,
        sum_prices_with_chip: Dict[str, int] = None,
        _id: ObjectId = None,
        original_id: Optional[int] = None,
    ):
        self._id = _id
        self.line_group_id = line_group_id
        self.status = status
        self.chip_scores = chip_scores if chip_scores is not None else {}
        self.chip_prices = chip_prices if chip_prices is not None else {}
        self.sum_scores = sum_scores if sum_scores is not None else {}
        self.sum_prices = sum_prices if sum_prices is not None else {}
        self.sum_prices_with_chip = sum_prices_with_chip if sum_prices_with_chip is not None else {}
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
        self.active_hanchan_id = active_hanchan_id
        self.original_id = original_id
