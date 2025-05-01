from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from bson.objectid import ObjectId

HANCHAN_STATUS = ["DISABLE", "ACTIVE", "ARCHIVE"]


@dataclass()
class Hanchan:
    _id: ObjectId
    line_group_id: str
    # 素点
    # Dictionary(key: user_line_id, value: raw_score)
    raw_scores: Dict[str, int]
    # 計算後のスコア
    # Dictionary(key: user_line_id, value: converted_score)
    converted_scores: Dict[str, int]
    match_id: int
    status: int
    original_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        line_group_id: str,
        match_id: int,
        status: int = 2,
        raw_scores: Dict[str, int] = {},
        converted_scores: Dict[str, int] = {},
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
        _id: ObjectId = None,
        original_id: Optional[int] = None,
    ):
        self._id = _id
        self.line_group_id = line_group_id
        self.raw_scores = raw_scores
        self.converted_scores = converted_scores
        self.match_id = match_id
        self.status = status
        self.original_id = original_id
        self.created_at = created_at
        self.updated_at = updated_at
