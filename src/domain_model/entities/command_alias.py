from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from bson.objectid import ObjectId


@dataclass
class CommandAlias:
    line_user_id: str
    line_group_id: str = field(default=None)
    alias: str = field(default=None)
    command: str = field(default=None)
    mentionees: List[str] = field(default_factory=list)
    _id: ObjectId = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):  # noqa: D105
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
