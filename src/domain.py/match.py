# flake8: noqa: E999
from dataclasses import dataclass
import datetime

from domain.user import User


@dataclass(frozen=True)
class Match:
    id: int
    room_id: str
    result_ids: str
    status: int
    users: [User]
    status: int
    create_at: datetime.date
