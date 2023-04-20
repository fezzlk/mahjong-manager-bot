from dataclasses import dataclass
from typing import Dict, Optional

HANCHAN_STATUS = ['DISABLE', 'ACTIVE', 'ARCHIVE']


@dataclass()
class Hanchan:
    id: Optional[int]
    line_group_id: str
    # 素点
    # Dictionary(key: user_line_id, value: raw_score)
    raw_scores: Dict[str, int]
    # 計算後のスコア
    # Dictionary(key: user_line_id, value: converted_score)
    converted_scores: Dict[str, int]
    match_id: int
    status: int

    def __init__(
        self,
        line_group_id: str,
        match_id: int,
        status: int,
        raw_scores: Dict[str, int] = [],
        converted_scores: Dict[str, int] = [],
        id: Optional[int] = None,
    ):
        self.id = id
        self.line_group_id = line_group_id
        self.raw_scores = raw_scores
        self.converted_scores = converted_scores
        self.match_id = match_id
        self.status = status
