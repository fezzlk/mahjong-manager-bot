from dataclasses import dataclass
from datetime import datetime

from bson.objectid import ObjectId


@dataclass()
class WebUser:
    _id: ObjectId
    user_code: str
    name: str
    email: str
    linked_line_user_id: str
    is_approved_line_user: bool
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        user_code: str,
        name: str = None,
        email: str = None,
        linked_line_user_id: str = None,
        is_approved_line_user: bool = False,
        created_at: datetime = None,
        updated_at: datetime = None,
        _id: ObjectId = None,
    ):
        self._id = _id
        self.user_code = user_code
        self.name = name
        self.email = email
        self.linked_line_user_id = linked_line_user_id
        self.is_approved_line_user = is_approved_line_user
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
