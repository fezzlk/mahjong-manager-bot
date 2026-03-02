from dataclasses import dataclass, field
from datetime import datetime

from bson.objectid import ObjectId


@dataclass
class UserHanchan:
    line_user_id: str
    hanchan_id: ObjectId
    point: int
    rank: int
    yakuman_count: int = field(default=0)
    _id: ObjectId = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):  # noqa: D105
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
