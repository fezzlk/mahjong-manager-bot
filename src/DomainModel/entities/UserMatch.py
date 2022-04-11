from dataclasses import dataclass


@dataclass()
class UserMatch:
    user_id: int
    match_id: int

    def __init__(
        self,
        user_id: int,
        match_id: int,
    ):
        self.user_id = user_id
        self.match_id = match_id
