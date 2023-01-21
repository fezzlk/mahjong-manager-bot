from dataclasses import dataclass
import datetime
from typing import Dict, List


@dataclass()
class Match:
    _id: int
    line_group_id: str
    hanchan_ids: List[int]
    users: list
    status: int
    tip_scores: Dict[str, int]
    created_at: datetime.date

    def __init__(
        self,
        line_group_id: str,
        hanchan_ids: List[int],
        status: int,
        users: list = [],
        created_at: datetime.date = None,
        tip_scores: Dict[str, int] = {},
        _id: int = None,
    ):
        self._id = _id
        self.line_group_id = line_group_id
        self.hanchan_ids = hanchan_ids
        self.users = users
        self.status = status
        self.tip_scores = tip_scores
        self.created_at = created_at


# status は 0: disabled, 1: active, 2: archived

# created_at は対戦開始日
