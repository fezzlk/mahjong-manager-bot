from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from bson.objectid import ObjectId


class UserMode(Enum):
    wait = "wait"


@dataclass()
class User:
    _id: ObjectId
    line_user_name: str
    line_user_id: str
    mode: str
    jantama_name: str
    original_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        line_user_id: str,
        line_user_name: str = None,
        mode: str = UserMode.wait.value,
        jantama_name: str = None,
        created_at: datetime = None,
        updated_at: datetime = None,
        _id: ObjectId = None,
        original_id: Optional[int] = None,
    ):
        if mode not in UserMode._member_names_:
            raise ValueError(f"UserMode の値({mode})が不適切です。")

        self._id = _id
        self.line_user_name = line_user_name
        self.line_user_id = line_user_id
        self.mode = mode
        self.jantama_name = jantama_name
        self.original_id = original_id
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
