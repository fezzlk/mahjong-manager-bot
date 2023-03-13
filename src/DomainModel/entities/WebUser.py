
from dataclasses import dataclass
from datetime import datetime


@dataclass()
class WebUser:
    _id: str
    user_code: str
    name: str
    email: str
    linked_line_user_id: str
    is_approved_line_user: bool
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        _id: str = None,
        user_code: str = None,
        name: str = None,
        email: str = None,
        linked_line_user_id: str = None,
        is_approved_line_user: bool = False,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        self._id = _id
        self.user_code = user_code
        self.name = name
        self.email = email
        self.linked_line_user_id = linked_line_user_id
        self.is_approved_line_user = is_approved_line_user
        self.created_at = created_at
        self.updated_at = updated_at
