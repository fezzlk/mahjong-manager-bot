from dataclasses import dataclass
from bson.objectid import ObjectId


@dataclass()
class UserHanchan:
    line_user_id: str
    hanchan_id: ObjectId
    point: int
    rank: int
    yakuman_count: int

    def __init__(
        self,
        line_user_id: str,
        hanchan_id: ObjectId,
        point: int,
        rank: int,
        yakuman_count: int = 0,
        _id: ObjectId = None,
    ):
        self.line_user_id = line_user_id
        self.hanchan_id = hanchan_id
        self._id = _id
        self.point = point
        self.rank = rank
        self.yakuman_count = yakuman_count
