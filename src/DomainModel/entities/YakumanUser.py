from dataclasses import dataclass


@dataclass()
class YakumanUser:
    _id: int
    user_id: int
    hanchan_id: int

    def __init__(
        self,
        user_id: int,
        hanchan_id: int,
        _id: int = None,
    ):
        self.user_id = user_id
        self.hanchan_id = hanchan_id
        self._id = _id