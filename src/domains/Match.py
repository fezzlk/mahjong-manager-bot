# flake8: noqa: E999
from dataclasses import dataclass
import datetime

from domains.User import User


@dataclass()
class Match:
    _id: int
    line_room_id: str
    result_ids: str
    users: list
    status: int
    create_at: datetime.date

    def __init__(
        self,
        line_room_id: str,
        result_ids: str,
        users: list,
        status: int,
        create_at: datetime.date = None,
        _id: int = None,
    ):
        self._id = _id
        self.line_room_id = line_room_id
        self.result_ids = result_ids
        self.users = users
        self.status = status
        self.create_at = create_at

# TODO: 値オブジェクト化
# line_room_id は対戦結果が投稿された LINE Room ID, Rから始まる

# result_ids は Result.id: int の 配列をjson化した文字列

# status は Enum(0: disabled, 1: active, 2: archived)

# users: User[] 対戦参加ユーザーの配列

# create_at は対戦開始日
