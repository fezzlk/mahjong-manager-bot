from dataclasses import dataclass
from typing import Dict


@dataclass()
class Hanchan:
    _id: int
    line_group_id: str = ''
    raw_scores: Dict[str, int] = None
    converted_scores: Dict[str, int] = None
    match_id: int = 0
    status: int = 0

    def __init__(
        self,
        line_group_id: str,
        raw_scores: Dict[str, int],
        converted_scores: Dict[str, int],
        match_id: int,
        status: int,
        _id: int = None,
    ):
        self._id = _id
        self.line_group_id = line_group_id
        self.raw_scores = raw_scores
        self.converted_scores = converted_scores
        self.match_id = match_id
        self.status = status

# raw_scores は計算前の1半荘のスコア
# Dictionary(key: user_line_id, value: raw_score)

# converted_scores は計算後の1半荘のスコア
# Dictionary(key: user_line_id, value: converted_score)

# status は 0: disabled, 1: active, 2: archived
