from dataclasses import dataclass


@dataclass()
class UserMatch:
    _id: int
    user_id: int
    match_id: int

    def __init__(
        self,
        user_id: int,
        match_id: int,
        _id: int = None,
    ):
        self._id = _id
        self.user_id = user_id
        self.match_id = match_id
