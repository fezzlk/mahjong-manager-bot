from dataclasses import dataclass
from datetime import datetime
from typing import List

from bson.objectid import ObjectId


@dataclass()
class CommandAlias:
    _id: ObjectId
    line_user_id: str
    line_group_id: str
    alias: str
    command: str
    mentionees: List[str]
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        line_user_id: str,
        line_group_id: str = None,
        alias: str = None,
        command: str = None,
        mentionees: List[str] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
        _id: ObjectId = None,
    ):
        self._id = _id
        self.line_user_id = line_user_id
        self.line_group_id = line_group_id
        self.alias = alias
        self.command = command
        self.mentionees = mentionees if mentionees is not None else []
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
