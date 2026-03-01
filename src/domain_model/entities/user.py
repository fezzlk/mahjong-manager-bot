from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from bson.objectid import ObjectId


class UserMode(Enum):
    wait = "wait"
    # input: user is in the middle of entering data (reserved for future personal input flows)
    input = "input"


@dataclass
class User:
    line_user_id: str
    line_user_name: str = None
    mode: str = UserMode.wait.value
    jantama_name: str = None
    original_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: ObjectId = field(default=None)

    def __post_init__(self):
        if self.mode not in UserMode._member_names_:
            raise ValueError(f"UserMode の値({self.mode})が不適切です。")
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
