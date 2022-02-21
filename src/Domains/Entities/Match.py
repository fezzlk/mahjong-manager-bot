from dataclasses import dataclass
import datetime
from typing import List


@dataclass()
class Match:
    _id: int
    line_group_id: str
    hanchan_ids: List[int]
    users: list
    status: int
    created_at: datetime.date

    def __init__(
        self,
        line_group_id: str,
        hanchan_ids: List[int],
        status: int,
        users: list = [],
        created_at: datetime.date = None,
        _id: int = None,
    ):
        self._id = _id
        self.line_group_id = line_group_id
        self.hanchan_ids = hanchan_ids
        self.users = users
        self.status = status
        self.created_at = created_at

# TODO: 値オブジェクト化
# line_group_id は対戦結果が投稿された LINE Group ID, Rから始まる

# hanchan_ids は Hanchan._id: int の 配列

# status は Enum(0: disabled, 1: active, 2: archived)

# users: User[] 対戦参加ユーザーの配列

# created_at は対戦開始日
