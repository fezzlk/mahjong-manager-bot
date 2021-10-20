from dataclasses import dataclass
from typing import Dict


@dataclass()
class Hanchan:
    _id: int
    line_room_id: str
    raw_scores: Dict[str, int]
    converted_scores: Dict[str, int]
    match_id: int
    status: int

    def __init__(
        self,
        line_room_id: str,
        raw_scores: Dict[str, int],
        converted_scores: Dict[str, int],
        match_id: int,
        status: int,
        _id: int = None,
    ):
        self._id = _id
        self.line_room_id = line_room_id
        self.raw_scores = raw_scores
        self.converted_scores = converted_scores
        self.match_id = match_id
        self.status = status

# TODO: 値オブジェクト化
# line_room_id は対戦結果が投稿された LINE Room ID, Rから始まる

# raw_scores は計算前の1半荘のスコア
# 長さ 3 or 4 の Dictionary(key: User, value: raw_score)

# converted_scores は計算後の1半荘のスコア
# 長さ 3 or 4 の Dictionary(key: User, value: converted_score)

# match_id = Match.id

# status は Enum(0: disabled, 1: active, 2: archived)
