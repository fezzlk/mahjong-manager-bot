from dataclasses import dataclass
from bson.objectid import ObjectId


@dataclass()
class UserGroup:
    _id: ObjectId
    line_user_id: int
    line_group_id: int

    def __init__(
        self,
        line_user_id: int,
        line_group_id: int,
        _id: ObjectId = None,
    ):
        self.line_user_id = line_user_id
        self.line_group_id = line_group_id
        self._id = _id
