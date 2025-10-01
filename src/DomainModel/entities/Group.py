from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from bson.objectid import ObjectId


class GroupMode(Enum):
    wait = "wait"
    input = "input"
    tip_input = "tip_input"
    tip_ok = "tip_ok"


@dataclass()
class Group:
    _id: ObjectId
    line_group_id: str
    mode: str
    active_match_id: ObjectId
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        line_group_id: str,
        mode: str = GroupMode.wait.value,
        active_match_id: ObjectId = None,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
        _id: ObjectId = None,
    ):
        if mode not in GroupMode._member_names_:
            raise ValueError(f"GroupMode の値({mode})が不適切です。")

        self._id = _id
        self.line_group_id = line_group_id
        self.mode = mode
        self.active_match_id = active_match_id
        self.created_at = created_at
        self.updated_at = updated_at
