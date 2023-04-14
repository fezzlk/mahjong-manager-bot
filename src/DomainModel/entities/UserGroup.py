from dataclasses import dataclass


@dataclass()
class UserGroup:
    line_user_id: int
    line_group_id: int

    def __init__(
        self,
        line_user_id: int,
        line_group_id: int,
    ):
        self.line_user_id = line_user_id
        self.line_group_id = line_group_id
