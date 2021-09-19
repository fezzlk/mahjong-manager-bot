# flake8: noqa: E999
from dataclasses import dataclass
import datetime

from domains.user import User


@dataclass(frozen=True)
class Match:
    id: int
    room_id: str # -> line_room_id
    result_ids: str
    users: [User]
    status: int
    create_at: datetime.date

# TODO: 値オブジェクト化
# line_room_id は対戦結果が投稿された LINE Room ID, Rから始まる

# result_ids は Result.id: int の 配列をjson化した文字列

# status は Enum(0: disabled, 1: active, 2: archived)

# users は対戦参加ユーザーの配列

# create_at は対戦開始日
