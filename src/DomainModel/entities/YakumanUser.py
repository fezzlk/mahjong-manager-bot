from dataclasses import dataclass


@dataclass()
class Group:
    user_id: int
    hanchan_id: int

    def __init__(
        self,
        user_id: int,
        hanchan_id: int,
    ):
        self.user_id = user_id
        self.hanchan_id = hanchan_id
