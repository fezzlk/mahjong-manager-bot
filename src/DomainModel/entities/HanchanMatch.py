from dataclasses import dataclass
from bson.objectid import ObjectId


@dataclass()
class HanchanMatch:
    _id: ObjectId
    hanchan_id: ObjectId
    match_id: ObjectId

    def __init__(
        self,
        hanchan_id: ObjectId,
        match_id: ObjectId,
        _id: ObjectId = None,
    ):
        self.hanchan_id = hanchan_id
        self.match_id = match_id
        self._id = _id
