from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId


@dataclass()
class YakumanUser:
    _id: Optional[ObjectId] = None
    line_user_id: Optional[str] = None
    yakuman_name: Optional[str] = None
    count: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __setitem__(self, key: str, value: object) -> None:
        setattr(self, key, value)
