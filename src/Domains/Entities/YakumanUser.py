from dataclasses import dataclass


@dataclass()
class YakumanUser:
    _id: int
    line_user_id: str
    hanchan_id: int

    def __init__(
        self,
        line_user_id: str,
        hanchan_id: int,
        _id: int = None,
    ):
        self._id = _id
        self.line_user_id = line_user_id
        self.hanchan_id = hanchan_id
