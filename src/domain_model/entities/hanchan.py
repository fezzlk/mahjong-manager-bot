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
        raw_scores: Dict[str, int] = None,
        converted_scores: Dict[str, int] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
        _id: ObjectId = None,
        original_id: Optional[int] = None,
    ):
        self._id = _id
        self.line_group_id = line_group_id
        self.raw_scores = raw_scores if raw_scores is not None else {}
        self.converted_scores = converted_scores if converted_scores is not None else {}
        self.match_id = match_id
        self.status = status
        self.original_id = original_id
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
