from dataclasses import dataclass
from datetime import datetime

from bson.objectid import ObjectId


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
        created_at: datetime = None,
        updated_at: datetime = None,
        _id: ObjectId = None,
    ):
        self.user_id = user_id
        self.match_id = match_id
        self._id = _id
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
