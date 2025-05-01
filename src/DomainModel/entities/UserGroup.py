from dataclasses import dataclass
from datetime import datetime

from bson.objectid import ObjectId


@dataclass()
class UserGroup:
    _id: ObjectId
    line_user_id: int
    line_group_id: int
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        line_user_id: int,
        line_group_id: int,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
        _id: ObjectId = None,
    ):
        self.line_user_id = line_user_id
        self.line_group_id = line_group_id
        self._id = _id
        self.created_at = created_at
        self.updated_at = updated_at
