from dataclasses import dataclass
from bson.objectid import ObjectId


@dataclass()
class UserMatch:
    user_id: ObjectId
    match_id: ObjectId

    def __init__(
        self,
        user_id: ObjectId,
        match_id: ObjectId,
        _id: ObjectId = None,
    ):
        self.user_id = user_id
        self.match_id = match_id
        self._id = _id
