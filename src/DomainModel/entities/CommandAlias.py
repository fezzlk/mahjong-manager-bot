from enum import Enum
from dataclasses import dataclass
from bson.objectid import ObjectId
from typing import Optional, List
from datetime import datetime



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
        mentionees: List[str] = [],
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
        _id: ObjectId = None,
    ):
        self._id = _id
        self.line_user_id = line_user_id
        self.line_group_id = line_group_id
        self.alias = alias
        self.command = command
        self.mentionees = mentionees
        self.created_at = created_at
        self.updated_at = updated_at