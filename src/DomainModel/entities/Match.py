from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

MATCH_STATUS = ['DISABLE', 'ACTIVE', 'ARCHIVE']


@dataclass()
class Match:
    id: Optional[int]
    line_group_id: str
    hanchan_ids: List[int]
    status: int
    tip_scores: Dict[str, int]
    created_at: datetime

    def __init__(
        self,
        line_group_id: str,
        status: int,
        hanchan_ids: List[int] = [],
        created_at: datetime = datetime.now(),
        tip_scores: Dict[str, int] = {},
        id: Optional[int] = None,
    ):
        self.id = id
        self.line_group_id = line_group_id
        self.hanchan_ids = hanchan_ids
        self.status = status
        self.tip_scores = tip_scores
        self.created_at = created_at
