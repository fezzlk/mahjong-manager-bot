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
    active_hanchan_id: ObjectId
    created_at: datetime
    original_id: Optional[int]

    def __init__(
        self,
        line_group_id: str,
        status: int = 2,
        created_at: datetime = datetime.now(),
        tip_scores: Dict[str, int] = {},
        active_hanchan_id: ObjectId = None,
        _id: ObjectId = None,
        original_id: Optional[int] = None,
    ):
        self._id = _id
        self.line_group_id = line_group_id
        self.status = status
        self.tip_scores = tip_scores
        self.created_at = created_at
        self.active_hanchan_id = active_hanchan_id
        self.original_id = original_id