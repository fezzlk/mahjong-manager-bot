# flake8: noqa: E999
from dataclasses import dataclass


@dataclass(frozen=True)
class Hanchan:
    id: int
    room_id: str # -> line_room_id
    raw_scores: str
    converted_scores: str
    match_id: int
    status: int

# TODO: 値オブジェクト化
# line_room_id は対戦結果が投稿された LINE Room ID, Rから始まる

# raw_scores は計算前の1半荘のスコア
# 長さ 3 or 4 の Dictionary(key: User, value: raw_score)

# converted_scores は計算後の1半荘のスコア
# 長さ 3 or 4 の Dictionary(key: User, value: converted_score)

# match_id = Match.id

# status は Enum(0: disabled, 1: active, 2: archived)

