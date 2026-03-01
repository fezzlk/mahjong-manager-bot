from dataclasses import dataclass
from datetime import datetime

from bson.objectid import ObjectId


@dataclass()
class UserHanchan:
    line_user_id: str
    hanchan_id: ObjectId
    point: int
    rank: int
    yakuman_count: int
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        line_user_id: str,
        hanchan_id: ObjectId,
        point: int,
        rank: int,
        yakuman_count: int = 0,
        created_at: datetime = None,
        updated_at: datetime = None,
        _id: ObjectId = None,
    ):
        self.line_user_id = line_user_id
        self.hanchan_id = hanchan_id
        self._id = _id
        self.point = point
        self.rank = rank
        self.yakuman_count = yakuman_count
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
