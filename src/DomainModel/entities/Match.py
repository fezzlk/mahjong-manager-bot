from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
from bson.objectid import ObjectId

MATCH_STATUS = ['DISABLE', 'ACTIVE', 'ARCHIVE']


@dataclass()
class Match:
    _id: ObjectId
    line_group_id: str
    status: int
    tip_scores: Dict[str, int]
    created_at: datetime
    original_id: Optional[int]

    def __init__(
        self,
        line_group_id: str,
        status: int,
        created_at: datetime = datetime.now(),
        tip_scores: Dict[str, int] = {},
        _id: ObjectId = None,
        original_id: Optional[int] = None,
    ):
        self._id = _id
        self.line_group_id = line_group_id
        self.status = status
        self.tip_scores = tip_scores
        self.created_at = created_at
        self.original_id = original_id