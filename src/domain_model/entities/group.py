from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from bson.objectid import ObjectId


class GroupMode(Enum):
    wait = "wait"
    input = "input"
    chip_input = "chip_input"
    chip_ok = "chip_ok"


@dataclass
class Group:
    line_group_id: str
    mode: str = GroupMode.wait.value
    active_match_id: ObjectId = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: ObjectId = field(default=None)

    def __post_init__(self):  # noqa: D105
        if self.mode not in GroupMode._member_names_:
            raise ValueError(f"GroupMode の値({self.mode})が不適切です。")
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
