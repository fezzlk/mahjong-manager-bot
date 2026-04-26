from dataclasses import dataclass, field
from datetime import datetime

from bson.objectid import ObjectId


@dataclass
class UserMatch:
    user_id: ObjectId
    match_id: ObjectId
    _id: ObjectId = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):  # noqa: D105
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
