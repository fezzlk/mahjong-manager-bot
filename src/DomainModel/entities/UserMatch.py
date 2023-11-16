from dataclasses import dataclass
from bson.objectid import ObjectId
from datetime import datetime


@dataclass()
class UserMatch:
    user_id: ObjectId
    match_id: ObjectId
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        user_id: ObjectId,
        match_id: ObjectId,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
        _id: ObjectId = None,
    ):
        self.user_id = user_id
        self.match_id = match_id
        self._id = _id
        self.created_at = created_at
        self.updated_at = updated_at